from flask import Blueprint, request, jsonify, session
from src.models.user import db, World, Module, Activity, User, UserProgress
from datetime import datetime

worlds_bp = Blueprint('worlds', __name__)

@worlds_bp.route('/worlds', methods=['GET'])
def get_worlds():
    """Retorna todos os mundos ordenados"""
    worlds = World.query.order_by(World.order).all()
    return jsonify({
        'worlds': [world.to_dict() for world in worlds]
    }), 200

@worlds_bp.route('/worlds', methods=['POST'])
def create_world():
    """Cria um novo mundo (apenas administradores)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        image_url = data.get('image_url', '')
        order = data.get('order', 1)

        if not name:
            return jsonify({'error': 'Nome é obrigatório'}), 400

        world = World(
            name=name,
            description=description,
            image_url=image_url,
            order=order
        )
        db.session.add(world)
        db.session.commit()

        return jsonify({
            'message': 'Mundo criado com sucesso',
            'world': world.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@worlds_bp.route('/worlds/<int:world_id>/modules', methods=['GET'])
def get_world_modules(world_id):
    """Retorna todos os módulos de um mundo"""
    world = World.query.get(world_id)
    if not world:
        return jsonify({'error': 'Mundo não encontrado'}), 404

    modules = Module.query.filter_by(world_id=world_id).order_by(Module.order).all()
    
    # Se o usuário estiver logado, incluir informações de progresso
    modules_data = []
    for module in modules:
        module_dict = module.to_dict()
        
        if 'user_id' in session:
            progress = UserProgress.query.filter_by(
                user_id=session['user_id'],
                module_id=module.id
            ).first()
            
            module_dict['user_progress'] = {
                'completed': progress.completed if progress else False,
                'score': progress.score if progress else 0
            }
        
        modules_data.append(module_dict)

    return jsonify({
        'world': world.to_dict(),
        'modules': modules_data
    }), 200

@worlds_bp.route('/worlds/<int:world_id>/modules', methods=['POST'])
def create_module(world_id):
    """Cria um novo módulo em um mundo (apenas administradores)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    world = World.query.get(world_id)
    if not world:
        return jsonify({'error': 'Mundo não encontrado'}), 404

    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        order = data.get('order', 1)

        if not title or not content:
            return jsonify({'error': 'Título e conteúdo são obrigatórios'}), 400

        module = Module(
            world_id=world_id,
            title=title,
            content=content,
            order=order
        )
        db.session.add(module)
        db.session.commit()

        return jsonify({
            'message': 'Módulo criado com sucesso',
            'module': module.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@worlds_bp.route('/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
    """Retorna um módulo específico"""
    module = Module.query.get(module_id)
    if not module:
        return jsonify({'error': 'Módulo não encontrado'}), 404

    module_dict = module.to_dict()
    
    # Incluir atividade do módulo
    activity = Activity.query.filter_by(module_id=module_id).first()
    if activity:
        module_dict['activity'] = activity.to_dict()

    return jsonify({'module': module_dict}), 200

@worlds_bp.route('/modules/<int:module_id>/activities', methods=['POST'])
def create_activity(module_id):
    """Cria uma atividade para um módulo (apenas administradores)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'error': 'Acesso negado'}), 403

    module = Module.query.get(module_id)
    if not module:
        return jsonify({'error': 'Módulo não encontrado'}), 404

    try:
        data = request.get_json()
        question = data.get('question')
        correct_answer = data.get('correct_answer')
        incorrect_answer = data.get('incorrect_answer')
        score_value = data.get('score_value', 10)

        if not question or not correct_answer or not incorrect_answer:
            return jsonify({'error': 'Pergunta e respostas são obrigatórias'}), 400

        activity = Activity(
            module_id=module_id,
            question=question,
            correct_answer=correct_answer,
            incorrect_answer=incorrect_answer,
            score_value=score_value
        )
        db.session.add(activity)
        db.session.commit()

        return jsonify({
            'message': 'Atividade criada com sucesso',
            'activity': activity.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@worlds_bp.route('/modules/<int:module_id>/complete', methods=['POST'])
def complete_module(module_id):
    """Marca um módulo como concluído pelo usuário"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    module = Module.query.get(module_id)
    if not module:
        return jsonify({'error': 'Módulo não encontrado'}), 404

    try:
        data = request.get_json()
        score = data.get('score', 0)

        user_id = session['user_id']
        
        # Buscar ou criar progresso do usuário
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            module_id=module_id
        ).first()

        if not progress:
            progress = UserProgress(
                user_id=user_id,
                module_id=module_id
            )
            db.session.add(progress)

        progress.completed = True
        progress.score = score
        progress.completed_at = datetime.utcnow()

        # Atualizar pontuação total do usuário
        user = User.query.get(user_id)
        user.score += score

        # Calcular progresso geral (porcentagem de módulos concluídos)
        total_modules = Module.query.count()
        completed_modules = UserProgress.query.filter_by(
            user_id=user_id,
            completed=True
        ).count()
        
        user.progress = (completed_modules / total_modules) * 100 if total_modules > 0 else 0

        db.session.commit()

        return jsonify({
            'message': 'Módulo concluído com sucesso',
            'progress': progress.to_dict(),
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

