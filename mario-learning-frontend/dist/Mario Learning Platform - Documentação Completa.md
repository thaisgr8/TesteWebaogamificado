# Mario Learning Platform - Documentação Completa

## Visão Geral

A Mario Learning Platform é uma plataforma web gamificada de aprendizado inspirada no clássico jogo Super Mario World. A plataforma oferece uma experiência de aprendizado interativa e envolvente, combinando elementos de gamificação com conteúdo educacional estruturado.

## Características Principais

### 🎮 Interface Gamificada
- Design inspirado no Super Mario World com paleta de cores retrô
- Avatares personalizados (Mario, Luigi, Princesa Peach, Yoshi)
- Sistema de pontuação e progresso visual
- HUD (Heads-Up Display) com informações em tempo real

### 🔐 Sistema de Autenticação
- Autenticação via LDAP (modo desenvolvimento disponível)
- Gerenciamento de usuários e permissões
- Sistema de administradores e usuários regulares

### 🌍 Estrutura de Conteúdo
- **Mundos**: Representam grandes áreas temáticas de aprendizado
- **Módulos**: Lições individuais dentro de cada mundo
- **Atividades**: Mini-jogos interativos para testar conhecimentos

### 🎯 Mini-Jogos Interativos
- Controles de teclado (setas direcionais + barra de espaço)
- Personagem controlável que se move pela tela
- Sistema de perguntas e respostas com duas alternativas
- Feedback visual imediato

### 📊 Sistema de Ranking
- Classificação global de usuários
- Métricas de pontuação e tempo dedicado
- Identificação de usuários por LDAP

### ⚙️ Painel Administrativo
- Gerenciamento completo de usuários
- Criação e edição de mundos e módulos
- Sistema de envio de e-mails em massa
- Relatórios e estatísticas de uso

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados (desenvolvimento)
- **Flask-CORS**: Suporte a requisições cross-origin
- **Python-LDAP**: Integração com servidores LDAP

### Frontend
- **React**: Biblioteca JavaScript para interface
- **Vite**: Build tool e servidor de desenvolvimento
- **CSS3**: Estilos customizados com tema Mario
- **JavaScript ES6+**: Lógica de interação

### Assets Visuais
- Avatares pixelados personalizados
- Elementos visuais inspirados no Super Mario World
- Ícones e sprites temáticos

## Arquitetura do Sistema

### Estrutura do Backend
```
mario_learning_platform/
├── src/
│   ├── main.py              # Aplicação principal Flask
│   ├── models/
│   │   └── user.py          # Modelos de dados
│   ├── routes/
│   │   ├── auth.py          # Rotas de autenticação
│   │   ├── avatars.py       # Gerenciamento de avatares
│   │   ├── worlds.py        # Mundos e módulos
│   │   ├── ranking.py       # Sistema de ranking
│   │   └── admin.py         # Painel administrativo
│   ├── database/
│   │   └── app.db           # Banco de dados SQLite
│   └── static/
│       └── assets/          # Assets visuais
├── venv/                    # Ambiente virtual Python
└── requirements.txt         # Dependências Python
```

### Estrutura do Frontend
```
mario-learning-frontend/
├── src/
│   ├── App.jsx              # Componente principal
│   ├── App.css              # Estilos customizados
│   └── components/
│       ├── LoginPage.jsx    # Página de login
│       ├── WorldMap.jsx     # Mapa de mundos
│       ├── AvatarSelection.jsx # Seleção de avatar
│       ├── ModuleList.jsx   # Lista de módulos
│       ├── ModuleContent.jsx # Conteúdo do módulo
│       ├── MiniGame.jsx     # Mini-jogo interativo
│       ├── Ranking.jsx      # Ranking de usuários
│       └── AdminPanel.jsx   # Painel administrativo
├── public/
│   └── assets/              # Assets públicos
└── package.json             # Dependências Node.js
```

## Modelos de Dados

### Usuário (User)
- `id`: Identificador único
- `ldap_username`: Nome de usuário LDAP
- `email`: E-mail do usuário
- `avatar_id`: Avatar selecionado
- `score`: Pontuação total
- `progress`: Progresso em porcentagem
- `time_spent`: Tempo dedicado (segundos)
- `is_admin`: Permissão de administrador
- `created_at`: Data de criação

### Avatar
- `id`: Identificador único
- `name`: Nome do avatar
- `image_url`: URL da imagem

### Mundo (World)
- `id`: Identificador único
- `name`: Nome do mundo
- `description`: Descrição
- `image_url`: URL da imagem
- `order`: Ordem de exibição

### Módulo (Module)
- `id`: Identificador único
- `world_id`: Mundo pai
- `title`: Título do módulo
- `content`: Conteúdo textual
- `order`: Ordem dentro do mundo

### Atividade (Activity)
- `id`: Identificador único
- `module_id`: Módulo pai
- `question`: Pergunta
- `correct_answer`: Resposta correta
- `incorrect_answer`: Resposta incorreta
- `score_value`: Pontos por acerto

### Progresso do Usuário (UserProgress)
- `id`: Identificador único
- `user_id`: Usuário
- `module_id`: Módulo
- `completed`: Status de conclusão
- `score`: Pontuação obtida
- `completed_at`: Data de conclusão




## Manual do Usuário

### Como Começar

#### 1. Acesso à Plataforma
1. Acesse a URL da plataforma no seu navegador
2. Na tela de login, insira suas credenciais LDAP
3. Clique em "ENTRAR" para acessar a plataforma

#### 2. Primeira Configuração
1. Após o primeiro login, você será direcionado para a seleção de avatar
2. Escolha entre Mario, Luigi, Princesa Peach ou Yoshi
3. Confirme sua seleção para prosseguir

#### 3. Navegação Principal
- **Mapa de Mundos**: Tela principal com todos os mundos disponíveis
- **HUD**: Canto superior direito mostra sua pontuação e progresso
- **Menu Superior**: Acesso rápido a Avatar, Ranking e outras funções

### Estudando na Plataforma

#### Explorando Mundos
1. Na tela principal, clique em um mundo disponível
2. Visualize a descrição e os módulos disponíveis
3. Clique em um módulo para começar a estudar

#### Lendo Conteúdo
1. Cada módulo apresenta conteúdo textual estruturado
2. Leia atentamente todo o material
3. Use a barra de rolagem para navegar pelo conteúdo
4. Ao final, clique em "Iniciar Atividade" para o mini-jogo

#### Jogando Mini-Jogos
1. **Controles**:
   - ⬅️ ➡️ Setas direcionais: Mover personagem
   - ⬆️ Seta para cima ou Espaço: Pular
2. **Objetivo**: Mover seu personagem até a resposta correta
3. **Pontuação**: Ganhe pontos por respostas corretas
4. **Progresso**: Seu progresso é salvo automaticamente

### Recursos Adicionais

#### Sistema de Ranking
1. Clique em "RANKING" no menu superior
2. Visualize sua posição entre todos os usuários
3. Compare pontuação e tempo dedicado
4. Identifique outros usuários pelo LDAP

#### Alteração de Avatar
1. Clique em "AVATAR" no menu superior
2. Selecione um novo avatar
3. Confirme a alteração

#### Logout
1. Clique em "SAIR" no menu superior
2. Confirme para encerrar a sessão

### Dicas de Uso

#### Maximizando o Aprendizado
- Leia todo o conteúdo antes de fazer a atividade
- Pratique os mini-jogos várias vezes
- Acompanhe seu progresso regularmente
- Compete de forma saudável no ranking

#### Navegação Eficiente
- Use as setas do teclado para navegação rápida nos jogos
- Mantenha o foco na janela do navegador durante os mini-jogos
- Verifique regularmente seu progresso no HUD

#### Resolução de Problemas
- Se encontrar dificuldades técnicas, atualize a página
- Verifique sua conexão com a internet
- Entre em contato com os administradores se necessário

## Manual do Administrador

### Acesso Administrativo

#### Login como Administrador
1. Faça login normalmente com suas credenciais LDAP
2. Se você tem permissões de administrador, verá o botão "ADMIN"
3. Clique em "IR PARA PAINEL ADMIN" para acessar as funções administrativas

### Gerenciamento de Usuários

#### Visualizar Usuários
1. No painel admin, clique na aba "Usuários"
2. Visualize lista completa de usuários cadastrados
3. Veja informações como LDAP, e-mail, pontuação e progresso

#### Gerenciar Permissões
1. Na lista de usuários, use o botão "Remover Admin" para revogar permissões
2. Para conceder permissões de admin, edite diretamente no banco de dados

### Gerenciamento de Conteúdo

#### Criando Mundos
1. Clique na aba "Conteúdo"
2. Preencha o formulário "Criar Novo Mundo":
   - **Nome**: Título descritivo do mundo
   - **Ordem**: Número para ordenação (1, 2, 3...)
   - **Descrição**: Texto explicativo sobre o mundo
3. Clique em "Criar Mundo"

#### Criando Módulos
1. Após criar um mundo, ele aparecerá na lista "Mundos Existentes"
2. Clique no mundo para adicionar módulos
3. Preencha as informações do módulo:
   - **Título**: Nome da lição
   - **Ordem**: Sequência dentro do mundo
   - **Conteúdo**: Material de estudo (texto formatado)
4. Salve o módulo

#### Criando Atividades
1. Para cada módulo, adicione uma atividade
2. Configure:
   - **Pergunta**: Questão a ser respondida
   - **Resposta Correta**: Alternativa verdadeira
   - **Resposta Incorreta**: Alternativa falsa
   - **Pontuação**: Pontos por acerto (padrão: 10)

### Sistema de Comunicação

#### Enviando E-mails em Massa
1. Clique na aba "E-mails"
2. Compose sua mensagem:
   - **Assunto**: Título do e-mail
   - **Mensagem**: Conteúdo do e-mail
3. Clique em "Enviar para Todos"
4. Todos os usuários cadastrados receberão o e-mail

#### Tipos de E-mails Recomendados
- **Motivacionais**: Incentive o estudo e progresso
- **Informativos**: Novos conteúdos ou funcionalidades
- **Lembretes**: Encoraje usuários inativos a retornar

### Relatórios e Estatísticas

#### Métricas Disponíveis
1. **Usuários Totais**: Número de pessoas cadastradas
2. **Usuários Ativos**: Pessoas que acessaram recentemente
3. **Módulos**: Quantidade de conteúdo disponível
4. **Progresso Médio**: Porcentagem média de conclusão

#### Análise de Dados
- Monitore o engajamento dos usuários
- Identifique conteúdos mais populares
- Acompanhe a evolução do aprendizado
- Tome decisões baseadas em dados

### Manutenção da Plataforma

#### Backup de Dados
- Faça backup regular do banco de dados
- Mantenha cópias dos assets visuais
- Documente mudanças importantes

#### Monitoramento
- Verifique logs de erro regularmente
- Monitore performance da plataforma
- Acompanhe feedback dos usuários

#### Atualizações
- Mantenha dependências atualizadas
- Teste novas funcionalidades em ambiente de desenvolvimento
- Comunique mudanças aos usuários


## Guia de Instalação e Deploy

### Requisitos do Sistema

#### Servidor
- **Sistema Operacional**: Ubuntu 20.04+ ou CentOS 7+
- **RAM**: Mínimo 2GB, recomendado 4GB
- **Armazenamento**: Mínimo 10GB livres
- **CPU**: 2 cores recomendados
- **Rede**: Conexão estável com a internet

#### Software
- **Python**: 3.8 ou superior
- **Node.js**: 18.0 ou superior
- **npm**: 8.0 ou superior
- **Git**: Para clonagem do repositório

### Instalação Local (Desenvolvimento)

#### 1. Preparação do Ambiente
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3 python3-pip python3-venv nodejs npm git sqlite3

# Verificar versões
python3 --version
node --version
npm --version
```

#### 2. Configuração do Backend
```bash
# Navegar para o diretório do backend
cd mario_learning_platform

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar diretório do banco de dados
mkdir -p src/database

# Inicializar banco de dados
python init_db.py

# Iniciar servidor Flask
python src/main.py
```

#### 3. Configuração do Frontend
```bash
# Em um novo terminal, navegar para o frontend
cd mario-learning-frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev -- --host
```

#### 4. Acesso à Aplicação
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Login de teste**: admin / 123456

### Deploy em Produção

#### 1. Preparação do Servidor
```bash
# Instalar nginx e supervisor
sudo apt install -y nginx supervisor

# Configurar firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

#### 2. Deploy do Backend
```bash
# Clonar repositório
git clone <repositorio> /var/www/mario-learning

# Configurar ambiente
cd /var/www/mario-learning/mario_learning_platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn

# Configurar banco de dados para produção
# Editar src/main.py para usar PostgreSQL ou MySQL

# Criar arquivo de configuração do Gunicorn
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
EOF

# Configurar supervisor
sudo cat > /etc/supervisor/conf.d/mario-learning.conf << EOF
[program:mario-learning]
command=/var/www/mario-learning/mario_learning_platform/venv/bin/gunicorn -c gunicorn.conf.py src.main:app
directory=/var/www/mario-learning/mario_learning_platform
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/mario-learning.log
EOF

# Reiniciar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start mario-learning
```

#### 3. Deploy do Frontend
```bash
# Build do frontend
cd /var/www/mario-learning/mario-learning-frontend
npm install
npm run build

# Configurar nginx
sudo cat > /etc/nginx/sites-available/mario-learning << EOF
server {
    listen 80;
    server_name seu-dominio.com;
    
    root /var/www/mario-learning/mario-learning-frontend/dist;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /assets {
        proxy_pass http://127.0.0.1:5000;
    }
}
EOF

# Ativar site
sudo ln -s /etc/nginx/sites-available/mario-learning /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Configuração HTTPS (Opcional)
```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com

# Configurar renovação automática
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Configuração LDAP

#### 1. Configuração Básica
```python
# No arquivo src/routes/auth.py, configure:
LDAP_SERVER = 'ldap://seu-servidor-ldap.com'
LDAP_BASE_DN = 'dc=empresa,dc=com'
LDAP_USER_DN = 'ou=users,dc=empresa,dc=com'
```

#### 2. Teste de Conexão
```bash
# Testar conexão LDAP
ldapsearch -x -H ldap://seu-servidor-ldap.com -D "cn=admin,dc=empresa,dc=com" -W -b "dc=empresa,dc=com"
```

### Monitoramento e Logs

#### 1. Logs do Sistema
```bash
# Logs do Flask
tail -f /var/log/mario-learning.log

# Logs do nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Logs do sistema
journalctl -u nginx -f
```

#### 2. Monitoramento de Performance
```bash
# Instalar htop para monitoramento
sudo apt install -y htop

# Verificar uso de recursos
htop
df -h
free -h
```

### Backup e Recuperação

#### 1. Backup do Banco de Dados
```bash
# SQLite (desenvolvimento)
cp src/database/app.db backup/app_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL (produção)
pg_dump mario_learning > backup/mario_learning_$(date +%Y%m%d_%H%M%S).sql
```

#### 2. Backup dos Assets
```bash
# Backup dos arquivos estáticos
tar -czf backup/assets_$(date +%Y%m%d_%H%M%S).tar.gz src/static/assets/
```

#### 3. Script de Backup Automático
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/var/backups/mario-learning"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup do banco
cp /var/www/mario-learning/mario_learning_platform/src/database/app.db $BACKUP_DIR/app_$DATE.db

# Backup dos assets
tar -czf $BACKUP_DIR/assets_$DATE.tar.gz /var/www/mario-learning/mario_learning_platform/src/static/assets/

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Solução de Problemas

#### Problemas Comuns

**1. Erro de Conexão com o Banco**
```bash
# Verificar permissões
ls -la src/database/
chmod 664 src/database/app.db
chown www-data:www-data src/database/app.db
```

**2. Erro 502 Bad Gateway**
```bash
# Verificar se o Gunicorn está rodando
sudo supervisorctl status mario-learning
sudo supervisorctl restart mario-learning
```

**3. Assets não Carregam**
```bash
# Verificar permissões dos assets
chmod -R 644 src/static/assets/
chown -R www-data:www-data src/static/assets/
```

**4. Erro de CORS**
```python
# Verificar configuração CORS no Flask
from flask_cors import CORS
CORS(app, supports_credentials=True, origins=['http://seu-dominio.com'])
```

#### Logs de Debug
```bash
# Ativar modo debug no Flask (apenas desenvolvimento)
export FLASK_DEBUG=1
python src/main.py

# Verificar logs detalhados
tail -f /var/log/mario-learning.log | grep ERROR
```

### Manutenção

#### Atualizações Regulares
```bash
# Atualizar dependências Python
source venv/bin/activate
pip list --outdated
pip install -U package_name

# Atualizar dependências Node.js
npm outdated
npm update
```

#### Limpeza de Logs
```bash
# Rotacionar logs automaticamente
sudo cat > /etc/logrotate.d/mario-learning << EOF
/var/log/mario-learning.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        supervisorctl restart mario-learning
    endscript
}
EOF
```

## Suporte Técnico

### Contato
- **E-mail**: suporte@empresa.com
- **Documentação**: Consulte este documento
- **Issues**: Reporte problemas no repositório Git

### Recursos Adicionais
- **Logs**: Sempre inclua logs relevantes ao reportar problemas
- **Versão**: Especifique a versão da plataforma
- **Ambiente**: Descreva o ambiente (desenvolvimento/produção)

### Contribuições
- Fork o repositório
- Crie uma branch para sua feature
- Faça commit das mudanças
- Abra um Pull Request

---

**Mario Learning Platform** - Desenvolvido com ❤️ para tornar o aprendizado mais divertido e envolvente!

