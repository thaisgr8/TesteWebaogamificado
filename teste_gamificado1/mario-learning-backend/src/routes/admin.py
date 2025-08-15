from flask import Blueprint, request, jsonify, session
from src.models.user import db, User
from flask_mail import Mail, Message
import os

admin_bp = Blueprint('admin', __name__)

# Configuração do Flask-Mail (deve ser configurado no main.py)
mail = Mail()

@admin_bp.route('/admin/users', methods=['GET'])
def get_all_users():
    """Retorna todos os usuários (apenas administradores)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@admin_bp.route('/admin/users/<int:user_id>/admin', methods=['PUT'])
def toggle_admin_status(user_id):
    """Alterna o status de administrador de um usuário"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    current_user = User.query.get(session['user_id'])
    if not current_user or not current_user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        # Não permitir que o usuário remova seu próprio status de admin
        if user_id == session['user_id']:
            return jsonify({'error': 'Não é possível alterar seu próprio status de administrador'}), 400

        user.is_admin = not user.is_admin
        db.session.commit()

        return jsonify({
            'message': f'Status de administrador {"ativado" if user.is_admin else "desativado"} com sucesso',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@admin_bp.route('/admin/send-email', methods=['POST'])
def send_bulk_email():
    """Envia e-mail em massa para todos os usuários"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        data = request.get_json()
        subject = data.get('subject')
        body = data.get('body')
        send_to_all = data.get('send_to_all', True)
        user_ids = data.get('user_ids', [])

        if not subject or not body:
            return jsonify({'error': 'Assunto e corpo do e-mail são obrigatórios'}), 400

        # Determinar destinatários
        if send_to_all:
            recipients = User.query.all()
        else:
            if not user_ids:
                return jsonify({'error': 'Lista de usuários é obrigatória quando send_to_all é False'}), 400
            recipients = User.query.filter(User.id.in_(user_ids)).all()

        if not recipients:
            return jsonify({'error': 'Nenhum destinatário encontrado'}), 400

        # Enviar e-mails (simulação - em produção, usar um serviço de e-mail real)
        sent_count = 0
        failed_emails = []

        for recipient in recipients:
            try:
                # Aqui você implementaria o envio real do e-mail
                # Por exemplo, usando Flask-Mail:
                # msg = Message(
                #     subject=subject,
                #     recipients=[recipient.email],
                #     body=body
                # )
                # mail.send(msg)
                
                # Para demonstração, apenas simular o envio
                print(f"E-mail enviado para {recipient.email}: {subject}")
                sent_count += 1
                
            except Exception as e:
                failed_emails.append({
                    'email': recipient.email,
                    'error': str(e)
                })

        return jsonify({
            'message': f'E-mail enviado com sucesso para {sent_count} usuários',
            'sent_count': sent_count,
            'total_recipients': len(recipients),
            'failed_emails': failed_emails
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@admin_bp.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    """Retorna estatísticas gerais da plataforma"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        from src.models.user import World, Module, Activity, UserProgress
        
        total_users = User.query.count()
        total_worlds = World.query.count()
        total_modules = Module.query.count()
        total_activities = Activity.query.count()
        
        # Usuários ativos (com pelo menos um módulo concluído)
        active_users = db.session.query(UserProgress.user_id).filter(
            UserProgress.completed == True
        ).distinct().count()
        
        # Progresso médio dos usuários
        avg_progress = db.session.query(db.func.avg(User.progress)).scalar() or 0
        
        # Top 5 usuários por pontuação
        top_users = User.query.order_by(User.score.desc()).limit(5).all()

        return jsonify({
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'total_worlds': total_worlds,
                'total_modules': total_modules,
                'total_activities': total_activities,
                'average_progress': round(avg_progress, 2)
            },
            'top_users': [
                {
                    'ldap_username': user.ldap_username,
                    'score': user.score,
                    'progress': user.progress
                } for user in top_users
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

