# BRX AI - Windows Installer (v8.0.0)
# Compatível com Windows 10 e 11

Write-Host "🧬 Inicializando instalador do BRX AI para Windows..." -ForegroundColor Cyan

# 1. Verificar se o Python está instalado
try {
    $pythonVersion = python --version 2>$null
    if ($null -eq $pythonVersion) {
        Write-Host "❌ Python não encontrado! Por favor, instale o Python 3.10+ do site oficial (python.org) ou da Microsoft Store." -ForegroundColor Red
        exit
    }
    Write-Host "✅ Python detectado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao verificar Python." -ForegroundColor Red
    exit
}

# 2. Criar diretórios necessários
$installDir = "$HOME\BRX_AI"
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
    Write-Host "📂 Diretório criado em: $installDir" -ForegroundColor Yellow
}

# 3. Instalar dependências
Write-Host "📦 Instalando dependências do Python..." -ForegroundColor Cyan
pip install requests beautifulsoup4 colorama --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Algumas dependências podem ter falhado. Verifique sua conexão." -ForegroundColor Yellow
} else {
    Write-Host "✅ Dependências instaladas com sucesso." -ForegroundColor Green
}

# 4. Configurar atalho (Opcional)
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktopPath\BRX AI.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "`"$installDir\brx.py`""
$Shortcut.WorkingDirectory = $installDir
$Shortcut.Description = "BRX AI - Advanced Reasoning"
$Shortcut.Save()

Write-Host "🚀 Instalação concluída!" -ForegroundColor Green
Write-Host "💡 Você pode iniciar o BRX AI pelo atalho na Área de Trabalho ou digitando 'python brx.py' no terminal." -ForegroundColor Cyan
