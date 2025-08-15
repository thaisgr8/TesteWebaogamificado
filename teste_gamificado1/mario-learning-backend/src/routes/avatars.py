from flask import Blueprint, request, jsonify, session
from src.models.user import db, Avatar, User

avatars_bp = Blueprint('avatars', __name__)

@avatars_bp.route('/avatars', methods=['GET'])
def get_avatars():
    """Retorna todos os avatares disponíveis"""
    avatars = Avatar.query.all()
    return jsonify({
        'avatars': [avatar.to_dict() for avatar in avatars]
    }), 200

@avatars_bp.route('/avatars', methods=['POST'])
def create_avatar():
    """Cria um novo avatar (apenas administradores)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        data = request.get_json()
        name = data.get('name')
        image_url = data.get('image_url')

        if not name or not image_url:
            return jsonify({'error': 'Nome e URL da imagem são obrigatórios'}), 400

        avatar = Avatar(name=name, image_url=image_url)
        db.session.add(avatar)
        db.session.commit()

        return jsonify({
            'message': 'Avatar criado com sucesso',
            'avatar': avatar.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@avatars_bp.route('/users/<int:user_id>/avatar', methods=['PUT'])
def update_user_avatar(user_id):
    """Atualiza o avatar do usuário"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    # Usuário só pode alterar seu próprio avatar, exceto administradores
    current_user = User.query.get(session['user_id'])
    if session['user_id'] != user_id and not current_user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        data = request.get_json()
        avatar_id = data.get('avatar_id')

        if not avatar_id:
            return jsonify({'error': 'ID do avatar é obrigatório'}), 400

        # Verificar se o avatar existe
        avatar = Avatar.query.get(avatar_id)
        if not avatar:
            return jsonify({'error': 'Avatar não encontrado'}), 404

        # Atualizar o usuário
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        user.avatar_id = avatar_id
        db.session.commit()

        return jsonify({
            'message': 'Avatar atualizado com sucesso',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

