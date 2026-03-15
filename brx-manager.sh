#!/bin/bash

# BRX AI - Gerenciador de Ciclo de Vida (Professional Edition)
# Comandos: install, remove, update

ACTION=$1
REPO_URL="https://github.com/dragonbrxos/BRX_AI.git"
INSTALL_DIR="/opt/brx-ai"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/scalable/apps"

echo "------------------------------------------------------------"
echo "           BRX AI - GERENCIADOR DE CICLO DE VIDA            "
echo "------------------------------------------------------------"

install_brx() {
    echo "[+] Iniciando instalação do BRX AI..."
    
    # Verificar Arch Linux
    if [ ! -f /etc/arch-release ]; then
        echo "[!] Aviso: Este sistema não parece ser Arch Linux. A instalação pode falhar."
    fi

    # Instalar dependências
    echo "[+] Instalando dependências via pacman..."
    sudo pacman -S --needed --noconfirm python python-requests python-beautifulsoup4 tk git

    # Criar diretório de instalação
    echo "[+] Configurando diretório /opt/brx-ai..."
    sudo mkdir -p $INSTALL_DIR
    sudo cp -r ./* $INSTALL_DIR/
    sudo chmod +x $INSTALL_DIR/*.py $INSTALL_DIR/*.sh

    # Criar comandos globais
    echo "[+] Criando comandos globais 'brx' e 'brx-gui'..."
    echo -e "#!/bin/bash\npython3 $INSTALL_DIR/cli.py \"\$@\"" | sudo tee $BIN_DIR/brx > /dev/null
    echo -e "#!/bin/bash\npython3 $INSTALL_DIR/gui.py \"\$@\"" | sudo tee $BIN_DIR/brx-gui > /dev/null
    sudo chmod +x $BIN_DIR/brx $BIN_DIR/brx-gui

    # Configurar Ícone e Desktop
    echo "[+] Configurando integração com o Desktop..."
    sudo mkdir -p $ICON_DIR
    sudo cp $INSTALL_DIR/brx-icon.svg $ICON_DIR/ 2>/dev/null || echo "[!] Ícone não encontrado, pulando..."
    sudo cp $INSTALL_DIR/brx.desktop $DESKTOP_DIR/
    
    # Inicializar cérebro
    cd $INSTALL_DIR && python3 seed_brain.py

    echo "[OK] BRX AI instalado com sucesso!"
}

remove_brx() {
    echo "[+] Removendo BRX AI do sistema..."
    sudo rm -rf $INSTALL_DIR
    sudo rm -f $BIN_DIR/brx $BIN_DIR/brx-gui
    sudo rm -f $DESKTOP_DIR/brx.desktop
    sudo rm -f $ICON_DIR/brx-icon.svg
    echo "[OK] BRX AI removido completamente."
}

update_brx() {
    echo "[+] Atualizando BRX AI para a versão mais recente..."
    TEMP_DIR=$(mktemp -d)
    git clone $REPO_URL $TEMP_DIR
    cd $TEMP_DIR
    ./brx-manager.sh install
    rm -rf $TEMP_DIR
    echo "[OK] BRX AI atualizado com sucesso!"
}

case $ACTION in
    install)
        install_brx
        ;;
    remove)
        remove_brx
        ;;
    update)
        update_brx
        ;;
    *)
        echo "Uso: sudo ./brx-manager.sh [install|remove|update]"
        exit 1
        ;;
esac
