# 🚨 ERRO: Container Parando Imediatamente no Railway

## O que está acontecendo?

Seu log mostra:
```
Starting Container
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:8080 (1)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 2
Stopping Container  ← AQUI ESTÁ O PROBLEMA
```

O container **inicia mas para imediatamente** porque a aplicação está **crashando** durante a inicialização.

## 🎯 Causa do Problema

A variável `SESSION_SECRET` **NÃO está sendo reconhecida** pelo Railway, mesmo que você tenha configurado.

### Possíveis razões:

1. ❌ Nome da variável digitado errado (com espaço, letra minúscula, etc.)
2. ❌ Variável configurada em lugar errado
3. ❌ Redeploy não foi feito após configurar a variável
4. ❌ Variável configurada em "service" errado (se você tem múltiplos services)

## ✅ SOLUÇÃO PASSO A PASSO

### Passo 1: Verifique as Variáveis de Ambiente

1. Acesse o painel do Railway: https://railway.app
2. Selecione seu projeto
3. Clique no **service/serviço** correto (aquele que tem o código Python)
4. Vá na aba **"Variables"**

### Passo 2: Verifique o Nome Exato da Variável

**IMPORTANTE:** O nome deve ser **EXATAMENTE**:
```
SESSION_SECRET
```

**NÃO pode ser:**
- ❌ `session_secret` (minúscula)
- ❌ `Session_Secret` (capitalização errada)
- ❌ `SESSION SECRET` (com espaço)
- ❌ `SESSION-SECRET` (com hífen)

### Passo 3: Gere um Valor Seguro

Execute este comando no terminal do Replit ou localmente:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Você vai receber algo como:
```
a8f5f167f44f4964e6c998dee827110c8bd99c17fc07e3d3c3fc2c89b13b7a3d
```

### Passo 4: Configure no Railway

No Railway, na aba "Variables":

1. **Se a variável JÁ existe:**
   - Clique no ícone de editar (lápis)
   - Cole o novo valor gerado
   - Clique em "Update" ou pressione Enter

2. **Se a variável NÃO existe:**
   - Clique em "+ New Variable"
   - Nome: `SESSION_SECRET`
   - Valor: Cole o valor gerado no Passo 3
   - Clique em "Add"

### Passo 5: CRÍTICO - Force um Redeploy

**Apenas salvar a variável NÃO é suficiente!** Você precisa forçar um redeploy:

**Opção A - Redeploy Manual (Mais Rápido):**
1. Na aba "Deployments"
2. Clique nos 3 pontinhos (...) do último deployment
3. Selecione "Redeploy"
4. Aguarde 2-3 minutos

**Opção B - Commit Vazio:**
```bash
git commit --allow-empty -m "Trigger redeploy"
git push
```

### Passo 6: Monitore os Logs

Enquanto faz o redeploy:
1. Vá na aba "Deployments"
2. Clique no deployment em andamento
3. Veja os logs em tempo real

**Procure por:**
- ✅ `Starting gunicorn` → Bom sinal
- ✅ `Listening at: http://0.0.0.0:XXXX` → Bom sinal
- ✅ `Booting worker with pid: X` → Bom sinal
- ✅ **NÃO deve ter "Stopping Container" logo depois**

**Se ainda aparecer "Stopping Container":**
- Procure por mensagens de erro ANTES dessa linha
- Copie TODOS os logs e me envie

## 🔍 Verificação Final

Depois do redeploy bem-sucedido:

1. ✅ Status do deployment: **"SUCCESS"** (verde)
2. ✅ Você consegue acessar o domínio público
3. ✅ A página carrega mostrando o sistema

## 💡 Dica de Debug

Para ver se a variável está sendo reconhecida, você pode temporariamente adicionar um `print` no código:

**Temporariamente, adicione isso no `app.py` (linha 15):**
```python
import os
print(f"DEBUG: SESSION_SECRET exists: {bool(os.environ.get('SESSION_SECRET'))}")
print(f"DEBUG: All env vars: {list(os.environ.keys())}")
app.secret_key = os.environ.get("SESSION_SECRET")
```

Depois do redeploy, você verá nos logs se a variável está sendo reconhecida.

**NÃO esqueça de remover** essas linhas de debug depois!

## 🆘 Ainda não funciona?

Se após seguir TODOS os passos acima ainda não funcionar:

1. **Tire screenshot da aba Variables** (pode tampar o valor, só mostre o nome)
2. **Copie os logs completos** do deployment
3. **Verifique se tem múltiplos services** no projeto Railway
4. Me envie essas informações

## 📝 Checklist Rápido

- [ ] Variável chamada exatamente `SESSION_SECRET` (maiúsculas)
- [ ] Valor gerado com `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Variável salva no service correto (o que tem o código Python)
- [ ] Redeploy forçado (manual ou via commit)
- [ ] Aguardado 2-3 minutos para deploy completar
- [ ] Verificado logs de deploy para mensagens de erro
