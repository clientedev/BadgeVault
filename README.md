# Sistema de Rastreamento de Badges - SENAI Morvan Figueiredo

Sistema web para rastreamento de certificações e badges de alunos das plataformas Google Cloud Skills Boost e Credly.

## 🚀 Funcionalidades

- ✅ Adicionar perfis de alunos via URL
- ✅ Scraping automático de contagem de badges
- ✅ Dashboard com métricas agregadas
- ✅ Suporte para Google Cloud Skills Boost
- ✅ Suporte para Credly (apenas no Replit)
- ✅ Interface Material Design responsiva
- ✅ Banco de dados PostgreSQL ou SQLite

## 🖥️ Hospedagem

### Replit (Recomendado - Suporte Completo)
- ✅ Google Cloud Skills Boost - Funciona
- ✅ Credly - Funciona
- ✅ Chromium/ChromeDriver pré-configurados
- ✅ PostgreSQL integrado
- ✅ Deploy automático

**Para executar no Replit:**
1. Clone este projeto no Replit
2. (Opcional) Crie um banco PostgreSQL via Database tool
3. Clique em "Run"

### Railway (Limitado - Apenas Google Cloud Skills)
- ✅ Google Cloud Skills Boost - Funciona
- ❌ Credly - NÃO funciona (limitação do ChromeDriver)

**Para deploy no Railway, consulte:** [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

## 📋 Requisitos

### Sistema
- Python 3.11+
- Chromium/ChromeDriver (para scraping do Credly)
- PostgreSQL (recomendado) ou SQLite (desenvolvimento)

### Python Packages
- Flask
- SQLAlchemy
- BeautifulSoup4
- Selenium
- Gunicorn

Todas as dependências estão listadas em `pyproject.toml`.

## ⚙️ Configuração

### Variáveis de Ambiente

**SESSION_SECRET** - Chave secreta para sessões Flask (OBRIGATÓRIA)
- No Replit: Configurado automaticamente
- Outros: DEVE ser configurada. Gere com `python -c "import secrets; print(secrets.token_hex(32))"`
- A aplicação não iniciará sem esta variável por segurança

**DATABASE_URL** - String de conexão do banco de dados
- Formato PostgreSQL: `postgresql://user:password@host:port/database`
- Se não configurado: usa SQLite automaticamente

### Banco de Dados

#### Replit:
1. Abra o Database tool
2. Clique em "Create a database"
3. Selecione PostgreSQL
4. Pronto! A variável `DATABASE_URL` é configurada automaticamente

#### Outros ambientes:
Configure manualmente a variável `DATABASE_URL` com sua connection string PostgreSQL.

## 🎯 Como Usar

1. Acesse a aplicação
2. Cole o URL do perfil do aluno (Google Cloud Skills ou Credly)
3. Clique em "Adicionar Aluno"
4. Visualize as estatísticas no dashboard

## 🔧 Desenvolvimento

```bash
# Instalar dependências
uv sync

# Executar localmente
python main.py

# Ou com gunicorn (produção)
gunicorn main:app
```

## 📝 Estrutura do Projeto

```
.
├── app.py              # Configuração Flask e banco de dados
├── main.py             # Rotas e lógica principal
├── models.py           # Modelo de dados (Student)
├── scraper.py          # Lógica de web scraping
├── templates/          # Templates HTML
│   └── index.html      # Dashboard principal
├── static/             # Arquivos estáticos
│   └── css/
│       └── style.css   # Estilos customizados
├── pyproject.toml      # Dependências Python
└── nixpacks.toml       # Configuração para Railway
```

## ⚠️ Limitações Conhecidas

### Railway + Credly
O scraping de perfis do Credly não funciona no Railway devido a limitações do ChromeDriver em ambientes Nixpacks. Soluções:
1. Use apenas Google Cloud Skills no Railway
2. Hospede no Replit para suporte completo
3. Considere Render.com ou Heroku com buildpacks

### Timeout
- Scraping pode demorar 10-15 segundos por perfil
- Páginas muito grandes podem exceder o timeout

## 🐛 Troubleshooting

### Erro: "Chrome WebDriver não encontrado"
- **Replit**: Verifique se chromium está instalado (já vem por padrão)
- **Railway**: Esperado para Credly. Use apenas Google Cloud Skills

### Erro: "Este perfil já foi adicionado"
- O sistema impede duplicatas baseado na URL do perfil
- Use URLs diferentes ou delete o perfil existente do banco

### Erro: "Plataforma não suportada"
- Verifique se a URL é do Google Cloud Skills ou Credly
- URLs aceitas:
  - `cloudskillsboost.google`
  - `skills.google`
  - `credly.com`

## 👥 Desenvolvido para

SENAI "Morvan Figueiredo"
Instrutores: Gabriel Eduardo e Johnny Braga

## 📄 Licença

Este projeto foi desenvolvido para uso interno do SENAI.
