# 🚀 Guia Completo de Deploy - Sistema de Badges

## ⚠️ IMPORTANTE: Onde NÃO Fazer Deploy

### ❌ Netlify
**Por que não funciona:**
- Netlify é para sites **estáticos apenas** (HTML, CSS, JS)
- **NÃO executa código Python** no servidor
- Esta aplicação precisa de Flask (Python) rodando no backend

**Resultado:** Erro "Page not found" ou "404"

### ❌ GitHub Pages
**Por que não funciona:**
- Mesma razão do Netlify
- Apenas arquivos estáticos
- Sem suporte a Python/Flask

---

## ✅ Plataformas Recomendadas para Flask

### 🥇 Opção 1: Railway (Recomendado)

**Vantagens:**
- ✅ Suporta Python/Flask perfeitamente
- ✅ Deploy automático via Git
- ✅ PostgreSQL integrado
- ✅ Plano gratuito disponível
- ✅ SSL/HTTPS automático

**Como fazer deploy:**

#### A) Deploy Automatizado (Mais Fácil)
```bash
# Execute o script que criamos
python setup_railway.py
```

#### B) Deploy Manual

1. **Crie conta no Railway:**
   - Acesse: https://railway.app
   - Faça login com GitHub

2. **Crie um novo projeto:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Autorize o Railway a acessar seus repositórios
   - Selecione o repositório do projeto

3. **Configure as variáveis:**
   - Clique em "Variables"
   - Adicione:
     ```
     SESSION_SECRET=<gere com: python -c 'import secrets; print(secrets.token_hex(32))'>
     ```
   - (Opcional) Adicione PostgreSQL:
     - Clique em "+ New"
     - Selecione "Database" → "Add PostgreSQL"
     - A variável `DATABASE_URL` será criada automaticamente

4. **Deploy:**
   - O Railway fará deploy automaticamente
   - Aguarde 2-5 minutos
   - Acesse o domínio gerado

**Problemas comuns:**
- **502 Bad Gateway:** SESSION_SECRET não configurado → Veja `QUICK_FIX_RAILWAY.md`
- **Container para:** Siga o guia `TROUBLESHOOTING_RAILWAY_502.md`

---

### 🥈 Opção 2: Render.com

**Vantagens:**
- ✅ Interface muito simples
- ✅ Plano gratuito generoso
- ✅ PostgreSQL incluído
- ✅ SSL automático
- ⚠️ Apps gratuitos "dormem" após 15 min de inatividade

**Como fazer deploy:**

1. **Crie conta no Render:**
   - Acesse: https://render.com
   - Faça login com GitHub

2. **Novo Web Service:**
   - Dashboard → "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório do projeto

3. **Configure o serviço:**
   ```
   Name: sistema-badges (ou qualquer nome)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind=0.0.0.0:$PORT --timeout=120 --workers=1 main:app
   ```

4. **Variáveis de ambiente:**
   - Na seção "Environment Variables"
   - Adicione:
     ```
     SESSION_SECRET=<valor gerado>
     ```

5. **PostgreSQL (Opcional):**
   - Dashboard → "New +" → "PostgreSQL"
   - Copie a "Internal Database URL"
   - Adicione como `DATABASE_URL` nas variáveis do web service

6. **Deploy:**
   - Clique em "Create Web Service"
   - Aguarde 3-5 minutos

**Criar requirements.txt:**
```bash
# Gere o arquivo de dependências
pip freeze > requirements.txt

# Ou crie manualmente:
cat > requirements.txt << EOF
beautifulsoup4>=4.14.2
email-validator>=2.3.0
flask>=3.1.2
flask-sqlalchemy>=3.1.1
gunicorn>=23.0.0
lxml>=6.0.2
psycopg2-binary>=2.9.11
requests>=2.32.5
sqlalchemy>=2.0.44
trafilatura>=2.0.0
werkzeug>=3.1.3
EOF
```

---

### 🥉 Opção 3: Replit (Mais Fácil de Todas)

**Vantagens:**
- ✅ Tudo já configurado neste projeto
- ✅ PostgreSQL com 1 clique
- ✅ Deploy instantâneo
- ✅ Desenvolvimento e produção no mesmo lugar
- ✅ SSL automático

**Como fazer deploy:**

1. **Você já está no Replit!**
   - O projeto já está configurado
   - Basta clicar em "Run"

2. **Para deploy público:**
   - Clique no botão "Deploy" no topo
   - Escolha um plano (Autoscale ou VM)
   - Configure o domínio
   - Pronto!

3. **PostgreSQL (Opcional):**
   - Aba lateral → "Tools" → "Database"
   - Clique em "Create database"
   - Selecione PostgreSQL
   - Variável `DATABASE_URL` configurada automaticamente

---

### Opção 4: Heroku (Pago)

**Nota:** Heroku **não tem mais plano gratuito** desde 2022.

**Como fazer deploy:**

1. **Instale Heroku CLI:**
   ```bash
   # Linux/Mac
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Crie o app:**
   ```bash
   heroku create nome-do-seu-app
   ```

4. **Configure variáveis:**
   ```bash
   heroku config:set SESSION_SECRET=$(python -c 'import secrets; print(secrets.token_hex(32))')
   ```

5. **Adicione PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

6. **Crie Procfile:**
   ```bash
   echo "web: gunicorn --bind=0.0.0.0:\$PORT --timeout=120 --workers=1 main:app" > Procfile
   ```

7. **Deploy:**
   ```bash
   git push heroku main
   ```

8. **Abrir app:**
   ```bash
   heroku open
   ```

---

## 📊 Comparação das Plataformas

| Plataforma | Gratuito | Facilidade | PostgreSQL | SSL | Recomendação |
|------------|----------|------------|------------|-----|--------------|
| **Railway** | ✅ Sim | ⭐⭐⭐⭐ | ✅ Sim | ✅ Sim | 🥇 Melhor opção |
| **Render** | ✅ Sim* | ⭐⭐⭐⭐⭐ | ✅ Sim | ✅ Sim | 🥈 Muito bom |
| **Replit** | ✅ Sim | ⭐⭐⭐⭐⭐ | ✅ Sim | ✅ Sim | 🥇 Já configurado! |
| **Heroku** | ❌ Não | ⭐⭐⭐⭐ | ✅ Sim | ✅ Sim | Apenas se pagar |
| Netlify | ❌ | - | - | - | ❌ NÃO FUNCIONA |
| GitHub Pages | ❌ | - | - | - | ❌ NÃO FUNCIONA |

*Apps gratuitos no Render "dormem" após inatividade

---

## 🎯 Recomendação Final

### Para este projeto específico:

1. **🥇 Replit** - Você já está aqui, tudo já funciona!
   - Clique em "Deploy" no topo
   - Escolha o plano
   - Pronto!

2. **🥈 Railway** - Se quer hospedar fora do Replit
   - Execute `python setup_railway.py`
   - Ou siga o guia manual acima

3. **🥉 Render** - Alternativa ao Railway
   - Interface mais simples
   - Processo similar

---

## 🔧 Arquivos Necessários para Deploy

Certifique-se de que seu repositório tem:

✅ `main.py` - Aplicação Flask  
✅ `app.py` - Configuração Flask/DB  
✅ `models.py` - Modelos do banco  
✅ `scraper.py` - Web scraping  
✅ `requirements.txt` ou `pyproject.toml` - Dependências  
✅ `templates/` - Templates HTML  
✅ `static/` - CSS/JS/Imagens  

**Para Railway:**
✅ `nixpacks.toml` - Configuração de build (já criado)

**Para Render/Heroku:**
✅ `Procfile` - Comando de start
```
web: gunicorn --bind=0.0.0.0:$PORT --timeout=120 --workers=1 main:app
```

✅ `requirements.txt` - Dependências
```bash
pip freeze > requirements.txt
```

---

## 🆘 Ajuda com Problemas

### Railway
- Erro 502: Veja `QUICK_FIX_RAILWAY.md`
- Container para: Veja `TROUBLESHOOTING_RAILWAY_502.md`
- Configuração: Veja `RAILWAY_DEPLOYMENT.md`

### Render
- App "sleeping": Plano gratuito normal, apps dormem após 15min
- Erro 500: Verifique logs no dashboard
- Build falha: Verifique `requirements.txt`

### Geral
- **SESSION_SECRET obrigatório** em todas plataformas
- Use PostgreSQL em produção (não SQLite)
- Sempre verifique os logs de deploy

---

## 💡 Dica de Ouro

**Não tente fazer deploy no Netlify ou GitHub Pages!** 

Essas plataformas são para sites estáticos (apenas frontend). Sua aplicação precisa de Python rodando no servidor.

Use Railway, Render ou Replit! 🚀
