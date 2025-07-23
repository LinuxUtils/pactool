pkgname=pactool
pkgver=1.0.4
pkgrel=1
pkgdesc="A versatile package management helper for Arch and Debian-based systems."
arch=('any')
url="https://github.com/LinuxUtils/pactool"
license=('Apache')
depends=('python')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('e6fc9400cc4261656f71bd298d7c341b20487197da7abed33f01d7fe1c1c4719')


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
