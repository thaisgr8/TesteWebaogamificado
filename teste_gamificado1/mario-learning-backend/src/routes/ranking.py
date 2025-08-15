from flask import Blueprint, jsonify, session
from src.models.user import db, User
from sqlalchemy import desc

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/ranking', methods=['GET'])
def get_ranking():
    """Retorna o ranking geral dos usuários"""
    try:
        # Buscar usuários ordenados por pontuação (decrescente) e depois por tempo dedicado (crescente)
        users = User.query.order_by(desc(User.score), User.time_spent).all()
        
        ranking_data = []
        for index, user in enumerate(users, 1):
            user_data = {
                'position': index,
                'ldap_username': user.ldap_username,
                'score': user.score,
                'time_spent': user.time_spent,
                'progress': user.progress,
                'is_current_user': False
            }
            
            # Marcar se é o usuário atual
            if 'user_id' in session and user.id == session['user_id']:
                user_data['is_current_user'] = True
            
            ranking_data.append(user_data)

        return jsonify({
            'ranking': ranking_data,
            'total_users': len(ranking_data)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ranking_bp.route('/ranking/top/<int:limit>', methods=['GET'])
def get_top_ranking(limit):
    """Retorna o top N do ranking"""
    try:
        if limit <= 0 or limit > 100:
            return jsonify({'error': 'Limite deve estar entre 1 e 100'}), 400

        users = User.query.order_by(desc(User.score), User.time_spent).limit(limit).all()
        
        ranking_data = []
        for index, user in enumerate(users, 1):
            user_data = {
                'position': index,
                'ldap_username': user.ldap_username,
                'score': user.score,
                'time_spent': user.time_spent,
                'progress': user.progress,
                'is_current_user': False
            }
            
            if 'user_id' in session and user.id == session['user_id']:
                user_data['is_current_user'] = True
            
            ranking_data.append(user_data)

        return jsonify({
            'ranking': ranking_data,
            'limit': limit
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ranking_bp.route('/user/position', methods=['GET'])
def get_user_position():
    """Retorna a posição do usuário atual no ranking"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        # Contar quantos usuários têm pontuação maior
        users_above = User.query.filter(
            (User.score > user.score) | 
            ((User.score == user.score) & (User.time_spent < user.time_spent))
        ).count()
        
        position = users_above + 1
        total_users = User.query.count()

        return jsonify({
            'position': position,
            'total_users': total_users,
            'score': user.score,
            'time_spent': user.time_spent,
            'progress': user.progress
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

