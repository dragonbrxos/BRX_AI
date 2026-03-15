#!/bin/bash

# BRX AI - Script de Instalação Automatizada (Arch Linux)
# Este script instala as dependências, configura o ambiente e cria o comando global 'brx'.

echo "------------------------------------------------------------"
echo "           BRX AI - INSTALADOR NATIVO (ARCH LINUX)          "
echo "------------------------------------------------------------"

# 1. Verificar se é Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo "[!] Aviso: Este sistema não parece ser Arch Linux. A instalação pode falhar."
fi

# 2. Instalar dependências do sistema via pacman
echo "[+] Instalando dependências do sistema (Python, Requests, BS4)..."
sudo pacman -S --needed --noconfirm python python-requests python-beautifulsoup4 git

# 3. Configurar permissões dos scripts
echo "[+] Configurando permissões..."
chmod +x brx.py cli.py

# 4. Criar o comando global 'brx' no sistema
echo "[+] Criando comando global 'brx' em /usr/local/bin/brx..."
cat <<EOF | sudo tee /usr/local/bin/brx > /dev/null
#!/bin/bash
python3 $(pwd)/cli.py "\$@"
EOF

sudo chmod +x /usr/local/bin/brx

# 5. Inicializar o cérebro se necessário
if [ ! -d "brain/knowledge" ]; then
    echo "[+] Inicializando cérebro atômico..."
    python3 seed_brain.py
fi

echo "------------------------------------------------------------"
echo "[OK] BRX AI instalado com sucesso!"
echo "[!] Agora você pode apenas digitar 'brx' em qualquer terminal."
echo "------------------------------------------------------------"
