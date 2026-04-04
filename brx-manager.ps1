
<#
.SYNOPSIS
    BRX AI Manager for Windows.
    Installs and updates the BRX AI system.
.DESCRIPTION
    This script provides functionalities to install and update the BRX AI system
    on Windows environments, ensuring all dependencies are met and the system
    is ready for use.
.NOTES
    File Name: brx-manager.ps1
    Author: Manus AI
    Version: 1.0
    Date: 2026-04-04
#>

function Install-BRXAI {
    Write-Host "Iniciando instalação do BRX AI..."

    # Check for Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Python não encontrado. Por favor, instale Python 3.9+ e adicione-o ao PATH." -ForegroundColor Yellow
        Write-Host "Você pode baixar em https://www.python.org/downloads/windows/" -ForegroundColor Yellow
        exit 1
    }

    # Install/Update pip
    Write-Host "Atualizando pip..."
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip

    # Install dependencies from requirements.txt
    if (Test-Path "requirements.txt") {
        Write-Host "Instalando dependências do requirements.txt..."
        pip install -r requirements.txt
    } else {
        Write-Host "requirements.txt não encontrado. Pulando instalação de dependências." -ForegroundColor Yellow
    }

    Write-Host "Instalação do BRX AI concluída!" -ForegroundColor Green
}

function Update-BRXAI {
    Write-Host "Atualizando BRX AI..."

    # Pull latest changes from Git (assuming BRX_AI is a git repo)
    if (Test-Path ".git") {
        Write-Host "Puxando últimas alterações do repositório Git..."
        git pull
    } else {
        Write-Host "Repositório Git não encontrado. Não é possível puxar atualizações." -ForegroundColor Yellow
    }

    # Re-install dependencies in case they changed
    if (Test-Path "requirements.txt") {
        Write-Host "Atualizando dependências do requirements.txt..."
        pip install -r requirements.txt
    }

    Write-Host "Atualização do BRX AI concluída!" -ForegroundColor Green
}

function Show-Help {
    Write-Host "BRX AI Manager"
    Write-Host "Uso: .\brx-manager.ps1 [comando]"
    Write-Host "Comandos disponíveis:"
    Write-Host "  install   - Instala o BRX AI e suas dependências."
    Write-Host "  update    - Atualiza o BRX AI para a versão mais recente."
    Write-Host- "  help      - Mostra esta mensagem de ajuda."
}

# Main script logic
if ($args.Count -eq 0) {
    Show-Help
} else {
    switch ($args[0]) {
        "install" { Install-BRXAI }
        "update"  { Update-BRXAI }
        "help"    { Show-Help }
        Default   { Write-Host "Comando inválido. Use 'help' para ver os comandos disponíveis." -ForegroundColor Red }
    }
}
