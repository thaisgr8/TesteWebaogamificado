# Guia de Deploy da Mario Learning Platform em Plataformas Gratuitas

Este guia detalha como fazer o deploy do frontend (React) e do backend (Flask) da Mario Learning Platform em serviços de hospedagem gratuitos.

## 1. Deploy do Frontend (React) - Sugestão: Vercel ou Netlify

O frontend é uma aplicação React estática que pode ser facilmente hospedada em serviços como Vercel ou Netlify.

### Preparação dos Arquivos

Você já tem o arquivo `mario-learning-frontend.zip` que contém o build de produção do frontend (`dist/` folder).

### Passos para Deploy (Exemplo com Vercel)

1.  **Crie uma conta na Vercel**: Acesse [vercel.com](https://vercel.com/) e crie uma conta (você pode usar seu GitHub, GitLab ou Bitbucket).
2.  **Instale a Vercel CLI (Opcional, mas recomendado)**:
    ```bash
    npm install -g vercel
    ```
3.  **Faça login na Vercel CLI**:
    ```bash
    vercel login
    ```
4.  **Descompacte o arquivo do frontend**: Crie uma pasta para o frontend e descompacte o `mario-learning-frontend.zip` nela. Certifique-se de que a pasta `dist` esteja no diretório raiz do seu projeto.
    ```bash
    mkdir mario-learning-frontend-deploy
    cd mario-learning-frontend-deploy
    unzip /path/to/mario-learning-frontend.zip # Substitua pelo caminho real
    ```
5.  **Faça o deploy**: Navegue até a pasta `mario-learning-frontend-deploy` (onde está a pasta `dist`) e execute:
    ```bash
    vercel
    ```
    - Quando perguntado sobre o diretório do projeto, selecione `.` (o diretório atual).
    - Quando perguntado sobre o diretório de build, especifique `dist`.
    - A Vercel irá detectar que é uma aplicação estática e fará o deploy.
6.  **Configure as variáveis de ambiente**: Após o deploy, você precisará configurar a URL do seu backend no frontend. Na Vercel, vá para as configurações do seu projeto, seção "Environment Variables", e adicione:
    - `VITE_API_BASE_URL`: A URL do seu backend (ex: `https://seu-backend.render.com`)

## 2. Deploy do Backend (Flask) - Sugestão: Render ou Railway

O backend Flask requer um ambiente que suporte Python e um banco de dados. Render e Railway são boas opções gratuitas (com algumas limitações).

### Preparação dos Arquivos

Você já tem o arquivo `mario-learning-backend.zip` que contém todo o código-fonte do backend, exceto o ambiente virtual e o banco de dados local.

### Passos para Deploy (Exemplo com Render)

1.  **Crie uma conta na Render**: Acesse [render.com](https://render.com/) e crie uma conta (você pode usar seu GitHub).
2.  **Crie um novo Web Service**: No dashboard da Render, clique em "New" -> "Web Service".
3.  **Conecte seu repositório Git**: Se você ainda não tem o código do backend em um repositório Git (GitHub, GitLab, Bitbucket), crie um e faça o upload do conteúdo descompactado de `mario-learning-backend.zip` para ele. Conecte a Render a este repositório.
4.  **Configurações do Web Service**:
    - **Name**: `mario-learning-backend` (ou outro nome de sua escolha)
    - **Region**: Escolha a região mais próxima de seus usuários
    - **Branch**: `main` (ou a branch que contém seu código)
    - **Root Directory**: `/` (se o código estiver na raiz do repositório)
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.main:app`
        - *Nota*: A Render injeta a porta via variável de ambiente `$PORT`.
    - **Health Check Path**: `/api/health` (você pode adicionar uma rota simples no Flask para isso)
5.  **Variáveis de Ambiente**: Adicione as seguintes variáveis de ambiente na Render:
    - `SECRET_KEY`: Uma chave secreta forte para sua aplicação Flask (gere uma aleatoriamente)
    - `SQLALCHEMY_DATABASE_URI`: A URL de conexão com seu banco de dados. Para produção, **não use SQLite**. A Render oferece PostgreSQL gratuito. Crie um novo serviço de banco de dados PostgreSQL na Render e use a URL de conexão fornecida.
        - Exemplo de URL PostgreSQL: `postgresql://user:password@host:port/database`
    - `LDAP_SERVER`: Seu servidor LDAP (ex: `ldap://seu-servidor-ldap.com`)
    - `LDAP_BASE_DN`: Seu Base DN (ex: `dc=empresa,dc=com`)
    - `LDAP_USER_DN`: Seu User DN (ex: `ou=users,dc=empresa,dc=com`)
    - `ENVIRONMENT`: `production`
6.  **Deploy**: Clique em "Create Web Service". A Render irá construir e implantar sua aplicação.
7.  **Inicialização do Banco de Dados em Produção**: Após o deploy, você precisará executar o script `init_db.py` uma vez para criar as tabelas e dados iniciais no seu banco de dados PostgreSQL. Você pode fazer isso via shell na Render ou criar um endpoint temporário no Flask para isso (e removê-lo depois).

### Considerações Importantes

-   **Banco de Dados**: Para produção, é **altamente recomendado** usar um banco de dados persistente como PostgreSQL ou MySQL, e não SQLite, que é para desenvolvimento. A Render oferece PostgreSQL gratuito.
-   **LDAP**: Certifique-se de que seu servidor LDAP seja acessível publicamente ou que a plataforma de deploy tenha acesso à sua rede interna (o que é mais complexo).
-   **Limitações de Serviços Gratuitos**: Serviços gratuitos podem ter limites de tempo de atividade, recursos e tráfego. Para uso em produção com 200+ usuários, considere planos pagos.
-   **Atualizações**: Para atualizar a aplicação, basta fazer um `git push` para o seu repositório, e a Render (ou Vercel/Netlify) irá automaticamente reconstruir e implantar as mudanças.

Espero que este guia detalhado ajude você a colocar a Mario Learning Platform no ar!

