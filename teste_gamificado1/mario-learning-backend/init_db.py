#!/usr/bin/env python3
"""
Script para inicializar o banco de dados da plataforma Mario Learning
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import app
from models.user import db, User, Avatar, World, Module, Activity, UserProgress

def init_database():
    """Inicializa o banco de dados com dados de exemplo"""
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existem dados
        if Avatar.query.first():
            print("Banco de dados já inicializado!")
            return
        
        print("Inicializando banco de dados...")
        
        # Criar avatares
        avatars = [
            Avatar(name="Mario", image_url="/assets/avatar_mario.png"),
            Avatar(name="Luigi", image_url="/assets/avatar_luigi.png"),
            Avatar(name="Princesa Peach", image_url="/assets/avatar_peach.png"),
            Avatar(name="Yoshi", image_url="/assets/avatar_yoshi.png")
        ]
        
        for avatar in avatars:
            db.session.add(avatar)
        
        # Criar usuário administrador
        admin_user = User(
            ldap_username="admin",
            email="admin@example.com",
            avatar_id=1,
            is_admin=True,
            score=0,
            progress=0.0
        )
        db.session.add(admin_user)
        
        # Criar usuário de teste
        test_user = User(
            ldap_username="usuario",
            email="usuario@example.com",
            avatar_id=2,
            is_admin=False,
            score=150,
            progress=25.0
        )
        db.session.add(test_user)
        
        # Criar mundo de exemplo
        world1 = World(
            name="Mundo 1: Fundamentos",
            description="Aprenda os conceitos básicos",
            image_url="/assets/world_background.png",
            order=1
        )
        db.session.add(world1)
        
        # Commit para obter IDs
        db.session.commit()
        
        # Criar módulos de exemplo
        module1 = Module(
            world_id=world1.id,
            title="Introdução aos Conceitos",
            content="""Bem-vindo ao primeiro módulo da nossa plataforma de aprendizado!

Neste módulo, você aprenderá os conceitos fundamentais que serão a base para todo o seu aprendizado.

Os conceitos básicos incluem:
- Definições importantes
- Princípios fundamentais
- Aplicações práticas

Ao final deste módulo, você terá uma compreensão sólida dos fundamentos e estará pronto para avançar para tópicos mais complexos.

Lembre-se: a prática leva à perfeição! Complete a atividade no final para testar seus conhecimentos.""",
            order=1
        )
        db.session.add(module1)
        
        module2 = Module(
            world_id=world1.id,
            title="Aplicações Práticas",
            content="""Agora que você aprendeu os conceitos básicos, vamos ver como aplicá-los na prática!

Este módulo aborda:
- Exemplos do mundo real
- Exercícios práticos
- Casos de uso comuns

A aplicação prática dos conceitos é essencial para consolidar o aprendizado e desenvolver habilidades que você poderá usar no dia a dia.

Prepare-se para o desafio final deste módulo!""",
            order=2
        )
        db.session.add(module2)
        
        # Commit para obter IDs dos módulos
        db.session.commit()
        
        # Criar atividades de exemplo
        activity1 = Activity(
            module_id=module1.id,
            question="Qual é o conceito mais importante abordado neste módulo?",
            correct_answer="Princípios fundamentais",
            incorrect_answer="Aplicações avançadas",
            score_value=10
        )
        db.session.add(activity1)
        
        activity2 = Activity(
            module_id=module2.id,
            question="Como aplicamos os conceitos na prática?",
            correct_answer="Através de exercícios práticos",
            incorrect_answer="Apenas estudando teoria",
            score_value=15
        )
        db.session.add(activity2)
        
        # Criar progresso de exemplo para o usuário de teste
        progress1 = UserProgress(
            user_id=test_user.id,
            module_id=module1.id,
            completed=True,
            score=10
        )
        db.session.add(progress1)
        
        # Commit final
        db.session.commit()
        
        print("Banco de dados inicializado com sucesso!")
        print(f"Avatares criados: {len(avatars)}")
        print("Usuários criados: admin (administrador), usuario (teste)")
        print("Mundo criado: Mundo 1 com 2 módulos")
        print("Atividades criadas: 2")

if __name__ == "__main__":
    init_database()

