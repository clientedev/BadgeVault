# Sistema de Controle de Badges

<div align="center">

![Badge](https://img.shields.io/badge/SENAI-Morvan%20Figueiredo-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Flask](https://img.shields.io/badge/Flask-3.1+-red)
![License](https://img.shields.io/badge/License-Educational-yellow)

Sistema para acompanhamento de certificações e badges conquistadas por alunos nas plataformas Google Cloud Skills Boost. Monitore o progresso dos estudantes em tempo real.

</div>

---

## 📋 Sobre o Projeto

Este sistema foi desenvolvido para o **SENAI "Morvan Figueiredo" 1.03** pelos professores **[Gabriel Eduardo](https://www.linkedin.com/in/gabriel-eduardo-almeida/)** e **[Johnny Braga](https://www.linkedin.com/in/johnny-braga-1b3b1148/)**, com o objetivo de facilitar o acompanhamento do progresso dos alunos em certificações técnicas do Google Cloud.

## ✨ Funcionalidades

- 🎯 **Dashboard com Métricas em Tempo Real**
  - Total de badges conquistadas
  - Número total de alunos cadastrados
  - Média de badges por aluno
  - Maior pontuação individual

- 🔍 **Scraping Automático Inteligente**
  - Extração automática de dados de perfis do Google Cloud Skills Boost
  - Suporte para múltiplos métodos de scraping (requests, BeautifulSoup, Trafilatura)
  - Detecção automática de plataforma

- 📊 **Visualização de Dados**
  - Gráfico de Top 10 alunos por badges
  - Distribuição de badges por faixas
  - Análise de badges por aluno
  - Gráficos interativos com Chart.js

- 🎨 **Interface Moderna**
  - Design baseado em Material Design 3
  - Ícone de badge no cabeçalho
  - Borda colorida com as cores do Google
  - Descrição do sistema integrada
  - Totalmente responsivo para mobile e desktop

- 📄 **Paginação Inteligente**
  - 10 alunos por página
  - Navegação intuitiva entre páginas
  - Controles de página anterior/próxima

- 🔧 **Filtros e Ordenação**
  - Ordenar por: Mais recentes, Mais badges, Menos badges, Nome (A-Z)
  - Interface amigável para seleção de filtros

## 🚀 Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.11+ | Linguagem principal |
| Flask | 3.1+ | Framework web |
| SQLAlchemy | 2.0+ | ORM para banco de dados |
| BeautifulSoup4 | 4.14+ | Parser HTML |
| Trafilatura | 2.0+ | Extração de conteúdo |
| Requests | 2.32+ | Cliente HTTP |
| Gunicorn | 23.0+ | Servidor WSGI |

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript ES6+** - Interatividade
- **Chart.js 4.4.0** - Gráficos e visualizações
- **Material Icons** - Ícones do Google
- **Google Fonts** - Roboto e JetBrains Mono

### Banco de Dados
- **PostgreSQL** (Produção) - Via Replit Database
- **SQLite** (Desenvolvimento) - Fallback automático

## 📦 Instalação

### Pré-requisitos
```bash
Python 3.11 ou superior
uv ou pip (gerenciador de pacotes)
```

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/sistema-badges.git
cd sistema-badges
```

2. **Instale as dependências**
```bash
# Usando uv (recomendado)
uv sync

# Ou usando pip
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
# Gere uma chave secreta
export SESSION_SECRET=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Configure o banco de dados (opcional - usa SQLite se não definido)
export DATABASE_URL="postgresql://user:password@host:port/database"
```

4. **Execute a aplicação**
```bash
# Modo desenvolvimento
python main.py

# Modo produção
gunicorn main:app
```

5. **Acesse no navegador**
```
http://localhost:5000
```

## 🎯 Como Usar

### Adicionar um Aluno

1. Acesse o sistema no navegador
2. Localize o campo "Link do Perfil"
3. Cole o URL completo do perfil do Google Cloud Skills Boost
   - Exemplo: `https://www.cloudskillsboost.google/public_profiles/xxxxxxx`
4. Clique em "Adicionar"
5. Aguarde o processamento (10-15 segundos)
6. O aluno aparecerá automaticamente na lista

### Visualizar Métricas

- **Dashboard Superior**: Métricas gerais em cards coloridos
- **Gráficos**: Análises visuais com diferentes perspectivas
- **Lista de Alunos**: Cards individuais com informações detalhadas

### Filtrar e Ordenar

1. Use o menu "Ordenar por" para escolher o critério
2. Clique em "Limpar filtros" para resetar
3. Use a paginação para navegar entre páginas

### Acessar Perfil Original

- Clique em qualquer card de aluno
- O perfil original abrirá em nova aba

## 📁 Estrutura do Projeto

```
sistema-badges/
├── 📄 app.py                    # Configuração Flask e banco de dados
├── 📄 main.py                   # Rotas e lógica da aplicação
├── 📄 models.py                 # Modelos SQLAlchemy
├── 📄 scraper.py                # Web scraping do Google Cloud Skills
├── 📂 static/
│   └── 📂 css/
│       └── 📄 style.css         # Estilos personalizados
├── 📂 templates/
│   └── 📄 index.html            # Template principal (dashboard)
├── 📄 pyproject.toml            # Dependências e metadados
├── 📄 uv.lock                   # Lock file de dependências
├── 📄 nixpacks.toml             # Configuração Nixpacks
├── 📄 replit.md                 # Documentação do projeto
├── 📄 design_guidelines.md      # Diretrizes de design
├── 📄 RAILWAY_DEPLOYMENT.md     # Guia de deploy Railway
└── 📄 README.md                 # Este arquivo
```

## ⚙️ Configuração Avançada

### Variáveis de Ambiente

| Variável | Obrigatório | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `SESSION_SECRET` | ✅ Sim | - | Chave para criptografia de sessões Flask |
| `DATABASE_URL` | ❌ Não | SQLite | URL de conexão PostgreSQL |

### PostgreSQL no Replit

1. Abra a aba **Database** no painel lateral
2. Clique em **"Create a database"**
3. Selecione **PostgreSQL**
4. Aguarde o provisionamento
5. A variável `DATABASE_URL` será configurada automaticamente
6. Reinicie a aplicação

### SQLite (Desenvolvimento)

Se `DATABASE_URL` não estiver definido, o sistema usará automaticamente:
```python
database_url = "sqlite:///students.db"
```

## 🌐 Deploy e Hospedagem

### Replit (Recomendado ✅)

**Recursos:**
- ✅ Google Cloud Skills Boost - Funciona perfeitamente
- ✅ PostgreSQL integrado
- ✅ Deploy automático
- ✅ SSL/HTTPS incluído

**Passos:**
1. Importe o projeto no Replit
2. Configure PostgreSQL (opcional)
3. Clique em "Run"
4. Acesse via URL do Replit

### Railway (Limitado ⚠️)

**Recursos:**
- ✅ Google Cloud Skills Boost - Funciona
- ⚠️ Requer configuração adicional

**Consulte:** [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) para instruções detalhadas

## 📊 Plataformas Suportadas

| Plataforma | URL | Status | Observações |
|------------|-----|--------|-------------|
| Google Cloud Skills Boost | `cloudskillsboost.google` | ✅ Suportado | Totalmente funcional |
| Google Cloud Skills | `skills.google` | ✅ Suportado | Redirecionamento automático |

## 🐛 Resolução de Problemas

### "Apenas perfis do Google Cloud Skills são suportados"
**Causa:** URL não reconhecida  
**Solução:** Verifique se a URL contém `cloudskillsboost.google` ou `skills.google`

### "Este perfil já foi adicionado"
**Causa:** URL duplicada no banco de dados  
**Solução:** O perfil já existe. URLs são únicas no sistema.

### "SESSION_SECRET environment variable is not set"
**Causa:** Variável obrigatória não configurada  
**Solução:** Configure `SESSION_SECRET` conforme instruções de instalação

### Scraping muito lento
**Causa:** Normal - extração de dados da web  
**Solução:** Aguarde 10-15 segundos por perfil. É esperado.

## 👥 Equipe

<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/gabriel-eduardo-almeida/" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-Gabriel%20Eduardo-0077B5?style=for-the-badge&logo=linkedin" alt="LinkedIn Gabriel Eduardo">
      </a><br>
      <strong>Gabriel Eduardo</strong><br>
      Professor Instrutor<br>
      SENAI "Morvan Figueiredo" 1.03
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/johnny-braga-1b3b1148/" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-Johnny%20Braga-0077B5?style=for-the-badge&logo=linkedin" alt="LinkedIn Johnny Braga">
      </a><br>
      <strong>Johnny Braga</strong><br>
      Professor Instrutor<br>
      SENAI "Morvan Figueiredo" 1.03
    </td>
  </tr>
</table>

## 🏫 Instituição

**SENAI "Morvan Figueiredo" 1.03**  
Formação técnica em tecnologia da informação

## 📝 Licença

Este projeto é de uso educacional exclusivo para o SENAI "Morvan Figueiredo".  
Desenvolvido como ferramenta pedagógica para acompanhamento de alunos.

## 🤝 Contribuindo

Este é um projeto educacional fechado. Para sugestões de melhorias:

1. Entre em contato com os professores responsáveis
2. Ou abra uma issue descrevendo a sugestão

## 📧 Suporte

Para dúvidas, problemas ou sugestões:
- Contate os professores [Gabriel Eduardo](https://www.linkedin.com/in/gabriel-eduardo-almeida/) ou [Johnny Braga](https://www.linkedin.com/in/johnny-braga-1b3b1148/)
- SENAI "Morvan Figueiredo" 1.03

---

<div align="center">

**Desenvolvido com ❤️ para o SENAI "Morvan Figueiredo" 1.03**

![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Skills%20Boost-4285F4?logo=google-cloud)
![Flask](https://img.shields.io/badge/Flask-Framework-000000?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)

</div>
