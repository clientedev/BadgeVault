# Como Resolver Erro 502 Bad Gateway no Railway

## O que é o erro 502?

O erro **502 Bad Gateway** significa que o Railway consegue se conectar ao seu servidor, mas a aplicação não está respondendo corretamente. Isso geralmente acontece quando:

1. A aplicação está crashando durante a inicialização
2. A aplicação não está escutando na porta correta
3. Faltam variáveis de ambiente obrigatórias
4. Há problemas com dependências

## ✅ Checklist de Solução (Siga nesta ordem)

### 1. Verifique o SESSION_SECRET

**MUITO IMPORTANTE:** O `SESSION_SECRET` precisa ser uma string aleatória e segura.

❌ **ERRADO:**
```
SESSION_SECRET=12345
```

✅ **CORRETO:**
```
SESSION_SECRET=a8f5f167f44f4964e6c998dee827110c8bd99c17fc07e3d3c3fc2c89b13b7a3d
```

**Como gerar:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Passos no Railway:**
1. Vá no painel do seu projeto no Railway
2. Clique em "Variables" (Variáveis)
3. Adicione ou edite `SESSION_SECRET` com um valor gerado pelo comando acima
4. Salve e aguarde o redeploy automático

---

### 2. Verifique os Logs do Deploy

**No painel do Railway:**
1. Clique na aba "Deployments"
2. Clique no deployment mais recente
3. Verifique a aba "Build Logs" e "Deploy Logs"

**Procure por:**
- ❌ `ModuleNotFoundError` - falta alguma dependência
- ❌ `RuntimeError: SESSION_SECRET environment variable is not set` - SESSION_SECRET não configurado
- ❌ `Address already in use` - problema com porta
- ❌ Qualquer linha com `ERROR` ou `FAILED`

---

### 3. Confirme que o arquivo nixpacks.toml está correto

O arquivo deve ter **exatamente** este conteúdo:

```toml
[phases.setup]
nixPkgs = ["chromium", "chromedriver"]
nixLibs = ["glib", "nss", "nspr", "atk", "cups", "gtk3", "pango", "cairo", "dbus", "libdrm", "mesa", "xorg.libX11", "xorg.libXcomposite", "xorg.libXdamage", "xorg.libXext", "xorg.libXfixes", "xorg.libXrandr", "xorg.libxcb", "expat"]

[phases.install]
cmds = ["uv sync"]

[start]
cmd = "gunicorn --bind=0.0.0.0:$PORT --timeout=120 --workers=1 main:app"
```

**Atenção:**
- ✅ Use `$PORT` (não `5000` ou qualquer porta fixa)
- ✅ Use `--workers=1` (não 2, 3 ou 4)
- ✅ Binding deve ser `0.0.0.0:$PORT`

---

### 4. Verifique se todas as dependências estão no pyproject.toml

O arquivo `pyproject.toml` deve ter:

```toml
dependencies = [
    "beautifulsoup4>=4.14.2",
    "email-validator>=2.3.0",
    "flask>=3.1.2",
    "flask-sqlalchemy>=3.1.1",
    "gunicorn>=23.0.0",
    "lxml>=6.0.2",
    "psycopg2-binary>=2.9.11",
    "requests>=2.32.5",
    "selenium>=4.38.0",
    "sqlalchemy>=2.0.44",
    "trafilatura>=2.0.0",
    "werkzeug>=3.1.3",
]
```

---

### 5. Configure o Banco de Dados (Opcional mas Recomendado)

**Se você quer usar PostgreSQL:**

1. No painel do Railway, clique em "+ New"
2. Selecione "Database" → "Add PostgreSQL"
3. Aguarde a criação do banco
4. A variável `DATABASE_URL` será configurada automaticamente
5. Faça um novo deploy (push um commit ou clique em "Redeploy")

**Se NÃO quer usar PostgreSQL:**
- A aplicação funcionará com SQLite (arquivo local)
- Os dados podem ser perdidos ao fazer redeploy

---

### 6. Force um Novo Deploy

Depois de fazer as correções acima:

**Opção 1: Push um commit**
```bash
git add .
git commit -m "Fix Railway deployment configuration"
git push
```

**Opção 2: Redeploy manual**
1. No painel do Railway
2. Clique nos três pontinhos (...) do deployment
3. Selecione "Redeploy"

---

### 7. Aguarde o Deploy Completar

- O deploy pode levar **2-5 minutos**
- Você verá "Deployment succeeded" quando terminar
- O domínio público será gerado automaticamente

---

## 🔍 Ainda não funciona?

Se após seguir todos os passos acima o erro persistir:

### Verifique a versão do Python

O Railway deve estar usando Python 3.11+. Você pode forçar a versão criando um arquivo `.python-version`:

```bash
echo "3.11" > .python-version
git add .python-version
git commit -m "Add Python version"
git push
```

### Teste localmente com Gunicorn

```bash
# No terminal do Replit ou local:
export SESSION_SECRET="teste123456"
gunicorn --bind=0.0.0.0:5000 --timeout=120 --workers=1 main:app
```

Se funcionar localmente mas não no Railway, o problema é específico do ambiente Railway.

### Simplifique temporariamente

Remova temporariamente as dependências do Chromium do `nixpacks.toml`:

```toml
[phases.install]
cmds = ["uv sync"]

[start]
cmd = "gunicorn --bind=0.0.0.0:$PORT --timeout=120 --workers=1 main:app"
```

Isso remove o Chromium mas mantém o app funcionando (você não poderá fazer scraping de Credly, mas Google Cloud Skills ainda funciona).

---

## 📊 Como Saber se Funcionou

✅ **Sucesso:**
- Deployment status: "SUCCESS" (verde)
- Você consegue acessar o domínio público sem erro
- A página carrega mostrando "Sistema de Controle de Badges"

❌ **Ainda com problemas:**
- Status: "FAILED" ou "CRASHED" (vermelho)
- Erro 502 Bad Gateway ao acessar
- Erro 503 Service Unavailable

---

## 💡 Dicas Importantes

1. **Sempre verifique os logs primeiro** - eles mostram o erro exato
2. **SESSION_SECRET é obrigatório** - a aplicação não inicia sem ele
3. **Use workers=1 no plano gratuito** - o Railway tem limites de memória
4. **Aguarde alguns minutos** - deploys não são instantâneos
5. **Um commit por vez** - não faça múltiplas mudanças de uma vez

---

## 🆘 Precisa de Ajuda?

Se ainda tiver problemas:
1. Copie os logs do Railway (Build Logs e Deploy Logs)
2. Tire um screenshot do erro
3. Compartilhe as variáveis de ambiente que você configurou (sem mostrar os valores secretos)
