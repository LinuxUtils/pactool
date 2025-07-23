pkgname=pactool
pkgver=1.0.4.1
pkgrel=1
pkgdesc="A versatile package management helper for Arch and Debian-based systems."
arch=('any')
url="https://github.com/LinuxUtils/pactool"
license=('Apache')
depends=('python')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('561f850b7652086cb0cda89fe17ccbbb9ca4dc1bb05e7d7887d45f4fb2327fc7')


package() {
    cd "$srcdir/$pkgname-$pkgver/src"
    install -Dm755 pactool.py "$pkgdir/usr/share/$pkgname/pactool.py"
    cp -r core "$pkgdir/usr/share/$pkgname/core"
    cp -r operations "$pkgdir/usr/share/$pkgname/operations"
    install -Dm755 /dev/stdin "$pkgdir/usr/bin/$pkgname" << EOF
#!/bin/bash
PYTHONPATH="/usr/share/$pkgname" exec python /usr/share/$pkgname/pactool.py "\$@"
EOF
}
