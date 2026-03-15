#!/bin/bash

# BRX AI - Script de Instalação Automatizada (Desktop Edition)
# Este script instala as dependências, configura o ambiente e cria os comandos globais.

echo "------------------------------------------------------------"
echo "           BRX AI - INSTALADOR DESKTOP (ARCH LINUX)         "
echo "------------------------------------------------------------"

# 1. Verificar se é Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo "[!] Aviso: Este sistema não parece ser Arch Linux. A instalação pode falhar."
fi

# 2. Instalar dependências do sistema via pacman
echo "[+] Instalando dependências (Python, Requests, BS4, Tkinter)..."
sudo pacman -S --needed --noconfirm python python-requests python-beautifulsoup4 tk git

# 3. Configurar permissões dos scripts
echo "[+] Configurando permissões..."
chmod +x brx.py cli.py gui.py

# 4. Criar o comando global 'brx' (Terminal)
echo "[+] Criando comando global 'brx' (Terminal)..."
cat <<EOF | sudo tee /usr/local/bin/brx > /dev/null
#!/bin/bash
python3 $(pwd)/cli.py "\$@"
EOF
sudo chmod +x /usr/local/bin/brx

# 5. Criar o comando global 'brx-gui' (Interface Gráfica)
echo "[+] Criando comando global 'brx-gui' (GUI)..."
cat <<EOF | sudo tee /usr/local/bin/brx-gui > /dev/null
#!/bin/bash
python3 $(pwd)/gui.py "\$@"
EOF
sudo chmod +x /usr/local/bin/brx-gui

# 6. Instalar o atalho de Desktop (.desktop)
echo "[+] Instalando atalho de Desktop..."
mkdir -p ~/.local/share/applications
cp brx.desktop ~/.local/share/applications/

# 7. Inicializar o cérebro se necessário
if [ ! -d "brain/knowledge" ]; then
    echo "[+] Inicializando cérebro atômico..."
    python3 seed_brain.py
fi

echo "------------------------------------------------------------"
echo "[OK] BRX AI Desktop Edition instalado com sucesso!"
echo "[!] Você pode iniciar pelo menu de aplicativos ou digitar 'brx-gui'."
echo "[!] O comando de terminal 'brx' também continua disponível."
echo "------------------------------------------------------------"
