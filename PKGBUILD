pkgname=pactool
pkgver=1.0.3
pkgrel=1
pkgdesc="A versatile package management helper for Arch and Debian-based systems."
arch=('any')
url="https://github.com/LinuxUtils/pactool"
license=('MIT')
depends=('python')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed')


package() {
    cd "$srcdir/$pkgname-$pkgver"
    install -Dm755 pactool.py "$pkgdir/usr/share/$pkgname/pactool.py"
    cp -r core "$pkgdir/usr/share/$pkgname/core"
    cp -r operations "$pkgdir/usr/share/$pkgname/operations"
    install -Dm755 /dev/stdin "$pkgdir/usr/bin/$pkgname" << EOF
#!/bin/bash
PYTHONPATH="/usr/share/$pkgname" exec python /usr/share/$pkgname/pactool.py "\$@"
EOF
}
