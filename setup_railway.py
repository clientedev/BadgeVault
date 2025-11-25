#!/usr/bin/env python3
import secrets
import subprocess
import sys
import os

print("=" * 60)
print("🚂 Script de Configuração Automática para Railway")
print("=" * 60)
print()

session_secret = secrets.token_hex(32)

print("✅ SESSION_SECRET gerado com sucesso!")
print()
print("📋 Valores das Variáveis de Ambiente:")
print("-" * 60)
print(f"SESSION_SECRET={session_secret}")
print("-" * 60)
print()

try:
    result = subprocess.run(['railway', '--version'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    railway_installed = result.returncode == 0
except (subprocess.TimeoutExpired, FileNotFoundError):
    railway_installed = False

if railway_installed:
    print("✅ Railway CLI detectado!")
    print()
    response = input("🤔 Deseja configurar automaticamente via Railway CLI? (s/n): ").lower().strip()
    
    if response == 's':
        print()
        print("🔗 Vinculando ao projeto Railway...")
        try:
            link_result = subprocess.run(['railway', 'link'], timeout=30)
            if link_result.returncode == 0:
                print()
                print("⚙️ Configurando variáveis de ambiente...")
                
                env_commands = [
                    ['railway', 'variables', '--set', f'SESSION_SECRET={session_secret}']
                ]
                
                for cmd in env_commands:
                    result = subprocess.run(cmd, timeout=10)
                    if result.returncode != 0:
                        print(f"❌ Erro ao executar: {' '.join(cmd)}")
                        sys.exit(1)
                
                print()
                print("✅ Variáveis configuradas com sucesso!")
                print()
                print("🚀 Fazendo deploy...")
                deploy_result = subprocess.run(['railway', 'up'], timeout=300)
                
                if deploy_result.returncode == 0:
                    print()
                    print("=" * 60)
                    print("✅ Deploy concluído com sucesso!")
                    print("=" * 60)
                    print()
                    print("🌐 Para ver a URL do seu app:")
                    print("   railway open")
                else:
                    print("❌ Erro durante o deploy")
                    sys.exit(1)
            else:
                print("❌ Erro ao vincular projeto")
                sys.exit(1)
        except subprocess.TimeoutExpired:
            print("❌ Timeout durante a operação")
            sys.exit(1)
    else:
        print()
        print("📝 Configure manualmente no painel do Railway:")
        print()
        print("1. Acesse: https://railway.app")
        print("2. Selecione seu projeto")
        print("3. Vá em 'Variables'")
        print("4. Adicione a variável abaixo:")
        print()
        print(f"   SESSION_SECRET={session_secret}")
        print()
        print("5. Salve e aguarde o redeploy automático")
else:
    print("ℹ️ Railway CLI não instalado")
    print()
    print("📝 Opção 1: Configuração Manual (Recomendado)")
    print("-" * 60)
    print("1. Acesse: https://railway.app")
    print("2. Selecione seu projeto")
    print("3. Vá em 'Variables'")
    print("4. Adicione a variável abaixo:")
    print()
    print(f"   SESSION_SECRET={session_secret}")
    print()
    print("5. Salve e aguarde o redeploy automático")
    print()
    print("📝 Opção 2: Instalar Railway CLI e Automatizar")
    print("-" * 60)
    print("npm i -g @railway/cli")
    print("railway login")
    print("python setup_railway.py")
    print()

print()
print("=" * 60)
print("💾 Valores salvos em: .railway_config.env (para referência)")
print("=" * 60)

with open('.railway_config.env', 'w') as f:
    f.write(f"# Configuração gerada em: {os.popen('date').read().strip()}\n")
    f.write(f"# Use estes valores no painel do Railway\n\n")
    f.write(f"SESSION_SECRET={session_secret}\n")
    f.write(f"\n# Opcional (PostgreSQL):\n")
    f.write(f"# DATABASE_URL=<será configurado automaticamente pelo Railway>\n")

print()
print("✅ Script concluído!")
print()
