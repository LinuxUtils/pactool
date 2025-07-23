#!/bin/bash
# ==> AUTOMATED AUR RELEASE SCRIPT FOR PACTOOL

set -e

# ==> CHECK ARGUMENT
if [ -z "$1" ]; then
    echo "Usage: ./release-to-aur.sh <new-version>"
    exit 1
fi

NEW_VERSION="$1"
PKGNAME="pactool"
TARBALL="$PKGNAME-$NEW_VERSION.tar.gz"
URL="https://github.com/LinuxUtils/$PKGNAME/archive/refs/tags/v$NEW_VERSION.tar.gz"

echo "==> Updating AUR package to version $NEW_VERSION..."

# ==> ENSURE WE ARE IN A GIT REPO
if [ ! -d ".git" ]; then
    echo "ERROR: This directory is not a git repository. Clone from AUR first:"
    echo "  git clone ssh://aur@aur.archlinux.org/pactool.git"
    exit 1
fi

# ==> CLEAN OLD TARBALLS
echo "==> Cleaning old tarballs..."
rm -f $PKGNAME-*.tar.gz

# ==> UPDATE PKGBUILD VERSION
echo "==> Updating pkgver in PKGBUILD..."
sed -i "s/^pkgver=.*/pkgver=$NEW_VERSION/" PKGBUILD

# ==> DOWNLOAD NEW TARBALL
echo "==> Downloading $TARBALL..."
curl -L -o "$TARBALL" "$URL"

# ==> GENERATE SHA256SUM
echo "==> Generating sha256sum..."
sha256=$(sha256sum "$TARBALL" | awk '{print $1}')
sed -i "s/^sha256sums=.*/sha256sums=('$sha256')/" PKGBUILD
echo "    -> New sha256sum: $sha256"

# ==> REGENERATE .SRCINFO
echo "==> Generating .SRCINFO..."
makepkg --printsrcinfo > .SRCINFO

# ==> TEST BUILD LOCALLY
echo "==> Testing local build..."
makepkg -si --noconfirm

# ==> COMMIT CHANGES
echo "==> Committing changes..."
git add PKGBUILD .SRCINFO
git commit -m "Release $PKGNAME v$NEW_VERSION"

# ==> PUSH TO AUR
echo "==> Pushing to AUR..."
git push

echo "==> AUR release completed for $PKGNAME v$NEW_VERSION."
