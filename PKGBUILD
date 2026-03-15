# PKGBUILD para o BRX AI no Arch Linux

pkgname=brx-ai
pkgver=1.0.0
pkgrel=1
pkgdesc="Modelo de IA leve baseado em JSON para Arch Linux, analisando caracteres e palavras."
arch=('any')
url="https://github.com/dragonbrxos/BRX_AI"
license=('MIT')
depends=('python')
source=("git+https://github.com/dragonbrxos/BRX_AI.git")
md5sums=('SKIP')

package() {
  cd "$srcdir/BRX_AI"
  
  # Criar diretórios necessários
  install -dm755 "$pkgdir/opt/brx-ai"
  install -dm755 "$pkgdir/usr/bin"

  # Copiar arquivos do projeto
  cp -r . "$pkgdir/opt/brx-ai/"

  # Criar link simbólico para o executável
  ln -s "/opt/brx-ai/cli.py" "$pkgdir/usr/bin/brx"
  
  # Dar permissão de execução ao script CLI
  chmod +x "$pkgdir/opt/brx-ai/cli.py"
}
