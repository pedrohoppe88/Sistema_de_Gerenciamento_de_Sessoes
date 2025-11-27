# Projeto Django - Sistema de Gestão de Usuários e Sessões

Este é um projeto Django que implementa um sistema de gestão de usuários, sessões, itens e retiradas. O sistema permite o cadastro de usuários, criação de sessões, gerenciamento de itens e controle de retiradas com geração de PDFs de cautela.

## Funcionalidades

- **Gerenciamento de Usuários**: Cadastro, login, edição e exclusão de usuários com diferentes graduações.
- **Sessões**: Criação de sessões protegidas por senha para organizar itens.
- **Itens**: Adição e gerenciamento de itens dentro de sessões, com controle de quantidade.
- **Retiradas e Devoluções**: Controle de retirada e devolução de itens, com geração automática de PDFs de cautela.
- **Painel Administrativo**: Usuários administradores podem gerenciar todos os usuários e visualizar estatísticas.
- **Testes Automatizados**: Testes end-to-end com Cypress para validar funcionalidades.

## Tecnologias Utilizadas

- **Backend**: Django 5.2.5
- **Banco de Dados**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Testes**: Cypress
- **Geração de PDFs**: xhtml2pdf

## Pré-requisitos

- Python 3.8 ou superior
- Node.js (para Cypress)
- MySQL Server
- Git

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone <https://github.com/pedrohoppe88/projeto_django/>
   cd projeto_django
   ```

2. **Instale as dependências do Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o banco de dados**:
   - Crie um banco de dados MySQL chamado `djangoaula`.
   - Atualize as configurações de banco em `project/settings.py` se necessário.

4. **Execute as migrações**:
   ```bash
   python manage.py migrate
   ```

5. **Instale as dependências do Cypress**:
   ```bash
   npm install
   ```

## Como Rodar

1. **Inicie o servidor Django**:
   ```bash
   python manage.py runserver
   ```
   Acesse em: http://localhost:8000

2. **Execute os testes com Cypress**:
   ```bash
   npx cypress run
   ```
   Ou para modo interativo:
   ```bash
   npx cypress open
   ```

## Estrutura do Projeto

- `project/`: Configurações principais do Django
- `usuarios/`: App principal com modelos, views, templates e lógica de negócio
- `cypress/`: Testes end-to-end
- `static/`: Arquivos estáticos (CSS, JS)
- `templates/`: Templates HTML

## Uso

1. Acesse a página inicial e cadastre um usuário.
2. Faça login no sistema.
3. Usuários administradores podem criar sessões e gerenciar usuários.
4. Dentro de uma sessão, adicione itens e controle retiradas/devoluções.
5. PDFs de cautela são gerados automaticamente para cada retirada/devolução.

## Licença

Este projeto é de uso pessoal
