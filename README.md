# 🪖 Sistema de Cautelas Militares

Um sistema completo de gerenciamento de inventário militar desenvolvido em Django, projetado para controlar retiradas e devoluções de equipamentos em sessões organizadas.

## 📋 Sobre o Projeto

Este é um sistema web robusto para gestão de cautelas militares, desenvolvido com Django Framework. O sistema permite que militares de diferentes graduações gerenciem equipamentos de forma segura e organizada, com autenticação obrigatória via PIN para todas as operações de retirada.

### ✨ Funcionalidades Principais

- **👥 Gerenciamento de Usuários**: Cadastro de militares com hierarquia completa do Exército Brasileiro
- **🔐 Autenticação Segura**: Sistema de login com PIN obrigatório para validação de retiradas
- **📦 Controle de Sessões**: Criação de sessões organizadas para diferentes contextos operacionais
- **📊 Painel Administrativo**: Dashboard moderno com gráficos e estatísticas em tempo real
- **📋 Gestão de Itens**: Controle completo de inventário com retiradas e devoluções
- **📄 Relatórios PDF**: Geração automática de relatórios de cautelas
- **📈 Analytics**: Gráficos interativos com Chart.js para visualização de dados

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.5** - Framework web Python
- **SQLite** - Banco de dados (desenvolvimento)
- **Python 3.11+** - Linguagem de programação

### Frontend
- **Bootstrap 5.3** - Framework CSS responsivo
- **Chart.js** - Biblioteca de gráficos interativos
- **Font Awesome** - Ícones vetoriais
- **HTML5/CSS3** - Estrutura e estilos

### Outras Dependências
- **xhtml2pdf** - Geração de PDFs
- **Pillow** - Processamento de imagens
- **django-crispy-forms** - Formulários elegantes

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- Git
- Virtualenv (recomendado)

### Passos para Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/sistema-cautelas-militares.git
cd sistema-cautelas-militares
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário (opcional):**
```bash
python manage.py createsuperuser
```

6. **Execute o servidor:**
```bash
python manage.py runserver
```

7. **Acesse no navegador:**
```
http://127.0.0.1:8000/
```

## 📁 Estrutura do Projeto

```
projeto_django/
├── project/                 # Configurações principais do Django
│   ├── settings.py         # Configurações do projeto
│   ├── urls.py             # URLs principais
│   └── wsgi.py             # Configuração WSGI
├── usuarios/                # App principal
│   ├── models.py           # Modelos de dados (Usuario, Sessao, Item, Retirada)
│   ├── views.py            # Lógica de negócio
│   ├── forms.py            # Formulários Django
│   ├── urls.py             # URLs do app
│   ├── templates/          # Templates HTML
│   │   └── usuarios/       # Templates específicos
│   └── migrations/         # Migrações do banco
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
├── media/                  # Arquivos de mídia (uploads)
├── db.sqlite3              # Banco de dados SQLite
├── manage.py               # Script de gerenciamento Django
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🎯 Modelos de Dados

### Usuario
- **Campos**: nome, email, senha, pin, graduacao, is_admin
- **Graduações**: Completa hierarquia do Exército Brasileiro (Soldado a Marechal)
- **PIN**: Obrigatório para validação de retiradas

### Sessao
- **Campos**: nome, senha, criador, criada_em
- **Função**: Agrupar itens relacionados a uma operação específica

### Item
- **Campos**: sessao, nome, quantidade, criado_em
- **Função**: Representar equipamentos/materiais disponíveis

### Retirada
- **Campos**: item, usuario, quantidade, data_retirada
- **Função**: Registrar empréstimos de itens

## 🔐 Sistema de Segurança

### Autenticação
- Login baseado em sessão
- Controle de acesso por roles (admin/normal)
- PIN obrigatório para todas as retiradas

### Validação de Retiradas
```python
# Exemplo de validação PIN
if not pin_confirmacao or pin_confirmacao != usuario.pin:
    messages.error(request, f"PIN incorreto para {usuario.nome}. A retirada não foi autorizada.")
```

## 📊 Dashboard Administrativo

### Estatísticas Disponíveis
- Total de itens cadastrados
- Total de retiradas realizadas
- Porcentagem de itens cautelados
- Sessões ativas
- Itens mais cautelados

### Gráficos Interativos
- **Bar Chart**: Sessões com mais retiradas
- **Pie Chart**: Usuários por graduação
- **Bar Chart**: Itens por sessão

## 🧪 Testes

O projeto inclui testes automatizados com Cypress para validação end-to-end:

```bash
# Instalar dependências de teste
npm install

# Executar testes
npx cypress run
```

## 📱 Responsividade

O sistema é totalmente responsivo e otimizado para:
- 📱 Dispositivos móveis
- 💻 Tablets
- 🖥️ Desktops

## 🚀 Deploy em Produção

### Configurações Recomendadas
1. **Banco de Dados**: PostgreSQL/MySQL
2. **Servidor Web**: Nginx + Gunicorn
3. **Cache**: Redis (opcional)
4. **SSL**: Certificado HTTPS obrigatório
5. **Backup**: Automação diária do banco

### Variáveis de Ambiente
```bash
DEBUG=False
SECRET_KEY=sua-chave-secreta
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=seu-dominio.com
```

## 👨‍💻 Autor

**Pedro Henrique Hoppe Tavares**
- 📧 pedrohenriquehoppe6@gmail.com
- 🔗 [LinkedIn](https://www.linkedin.com/in/pedro-henrique-hoppe-tavares-5b0344276/)


⭐ **Dê uma estrela se este projeto te ajudou!**

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</div>
