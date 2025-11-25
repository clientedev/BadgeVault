# Deploying to Railway

Este guia explica como fazer o deploy da aplicação no Railway.

## Pré-requisitos

1. Conta no [Railway](https://railway.app/)
2. Projeto conectado ao repositório Git

## Configuração do Ambiente

### 1. Instalar Chrome/ChromeDriver

O arquivo `nixpacks.toml` já está configurado para instalar automaticamente o Chromium e ChromeDriver no Railway.

### 2. Variáveis de Ambiente

Configure as seguintes variáveis de ambiente no painel do Railway:

#### Obrigatórias:
- `SESSION_SECRET` - Chave secreta para sessões Flask
  - Gere uma chave aleatória: `python -c "import secrets; print(secrets.token_hex(32))"`

#### Recomendadas (PostgreSQL):
- `DATABASE_URL` - String de conexão do banco de dados PostgreSQL
  - O Railway pode provisionar automaticamente um banco PostgreSQL
  - Vá em "New" → "Database" → "Add PostgreSQL"
  - A variável `DATABASE_URL` será configurada automaticamente

**Nota:** Se `DATABASE_URL` não estiver configurada, a aplicação usará SQLite (não recomendado para produção).

### 3. Configurações do Build

O Railway detectará automaticamente que é um projeto Python e usará o arquivo `nixpacks.toml` para configurar o ambiente.

**Comando de Start:** `gunicorn main:app`

Isso já está configurado no arquivo `nixpacks.toml`.

### 4. Deploy

1. Faça commit e push do código para o repositório
2. O Railway fará o deploy automaticamente
3. Verifique os logs para confirmar que o Chrome/ChromeDriver foram instalados corretamente

## Verificação

Após o deploy:

1. Acesse a URL fornecida pelo Railway
2. Tente adicionar um perfil de aluno
3. Verifique os logs se houver erros

## Troubleshooting

### Erro: "Chrome WebDriver não encontrado"

**Solução:** Verifique se o arquivo `nixpacks.toml` está presente no repositório e contém:
```toml
[phases.setup]
nixPkgs = ["chromium", "chromedriver"]
```

### Erro: "Internal Server Error" ao adicionar aluno

**Possíveis causas:**
1. Chrome/ChromeDriver não instalados → Verifique logs do Railway
2. URL inválida ou plataforma não suportada
3. Timeout na requisição → Algumas páginas podem demorar para carregar

**Logs:** Sempre verifique os logs do Railway para mensagens de erro detalhadas.

### Erro de Banco de Dados

**Solução:** Certifique-se de que:
1. O PostgreSQL está provisionado no Railway
2. A variável `DATABASE_URL` está configurada
3. A aplicação foi reiniciada após configurar o banco

## Plataformas Suportadas

A aplicação suporta scraping de:
- Google Cloud Skills Boost (`cloudskillsboost.google` ou `skills.google`)
- Credly (`credly.com`)

## Recursos do Railway

- **Auto-deploy:** Push para o repositório Git
- **Logs em tempo real:** Monitore a aplicação
- **Escalabilidade:** Ajuste recursos conforme necessário
- **Banco de dados gerenciado:** PostgreSQL com backups automáticos
