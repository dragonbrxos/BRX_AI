#!/bin/bash

# Script de instalação do BRX AI para Arch Linux (v2.1)

echo "Iniciando instalação do BRX AI com suporte a Pesquisa Web..."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado. Por favor, instale o python com 'sudo pacman -S python'."
    exit 1
fi

# Instalar dependências necessárias para pesquisa web
echo "Instalando dependências (requests, beautifulsoup4)..."
sudo pacman -S --noconfirm python-requests python-beautifulsoup4

# Definir diretório de instalação
INSTALL_DIR="/opt/brx-ai"
BIN_DIR="/usr/local/bin"

echo "Criando diretório de instalação em $INSTALL_DIR..."
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r . "$INSTALL_DIR"

# Criar link simbólico para o executável
echo "Criando comando 'brx' em $BIN_DIR..."
sudo ln -sf "$INSTALL_DIR/cli.py" "$BIN_DIR/brx"
sudo chmod +x "$INSTALL_DIR/cli.py"

# Popular cérebro inicial se necessário
echo "Populando cérebro inicial..."
cd "$INSTALL_DIR" && python3 seed_brain.py

echo "--------------------------------------------------"
echo "Instalação concluída com sucesso!"
echo "Agora você pode iniciar o BRX digitando 'brx' no seu terminal."
echo "Use o comando 'web' dentro do chat para ativar a pesquisa online."
echo "--------------------------------------------------"
