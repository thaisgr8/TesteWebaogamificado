from flask import Blueprint, request, jsonify, session
from src.models.user import db, User
import ldap3
import os

auth_bp = Blueprint('auth', __name__)

# Configurações LDAP (devem ser definidas como variáveis de ambiente em produção)
LDAP_SERVER = os.getenv('LDAP_SERVER', 'ldap://localhost:389')
LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'dc=example,dc=com')
LDAP_USER_DN = os.getenv('LDAP_USER_DN', 'cn=users,dc=example,dc=com')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autenticação via LDAP"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username e password são obrigatórios'}), 400

        # Tentativa de autenticação LDAP
        if authenticate_ldap(username, password):
            # Buscar ou criar usuário no banco de dados
            user = User.query.filter_by(ldap_username=username).first()
            
            if not user:
                # Criar novo usuário
                user_info = get_ldap_user_info(username)
                user = User(
                    ldap_username=username,
                    email=user_info.get('email', f'{username}@example.com')
                )
                db.session.add(user)
                db.session.commit()

            # Criar sessão
            session['user_id'] = user.id
            session['username'] = user.ldap_username
            session['is_admin'] = user.is_admin

            return jsonify({
                'message': 'Login realizado com sucesso',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout do usuário"""
    session.clear()
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Retorna informações do usuário logado"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    return jsonify({'user': user.to_dict()}), 200

def authenticate_ldap(username, password):
    """
    Autentica usuário via LDAP
    Em ambiente de desenvolvimento, aceita qualquer senha para facilitar testes
    """
    # Para desenvolvimento/demonstração, aceitar qualquer senha
    # Em produção, implementar autenticação LDAP real
    if os.getenv('ENVIRONMENT') == 'development':
        return True
    
    try:
        # Configuração do servidor LDAP
        server = ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL)
        
        # Tentar conectar com as credenciais do usuário
        user_dn = f'uid={username},{LDAP_USER_DN}'
        conn = ldap3.Connection(server, user_dn, password, auto_bind=True)
        
        # Se chegou até aqui, a autenticação foi bem-sucedida
        conn.unbind()
        return True
        
    except ldap3.core.exceptions.LDAPBindError:
        return False
    except Exception as e:
        print(f"Erro na autenticação LDAP: {e}")
        return False

def get_ldap_user_info(username):
    """
    Busca informações do usuário no LDAP
    Em ambiente de desenvolvimento, retorna informações mock
    """
    if os.getenv('ENVIRONMENT') == 'development':
        return {
            'email': f'{username}@example.com',
            'name': username.title()
        }
    
    try:
        server = ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, auto_bind=True)
        
        search_filter = f'(uid={username})'
        conn.search(LDAP_USER_DN, search_filter, attributes=['mail', 'cn'])
        
        if conn.entries:
            entry = conn.entries[0]
            return {
                'email': str(entry.mail) if entry.mail else f'{username}@example.com',
                'name': str(entry.cn) if entry.cn else username.title()
            }
        
        conn.unbind()
        return {'email': f'{username}@example.com', 'name': username.title()}
        
    except Exception as e:
        print(f"Erro ao buscar informações do usuário: {e}")
        return {'email': f'{username}@example.com', 'name': username.title()}

