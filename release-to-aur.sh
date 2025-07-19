#!/bin/bash
# ==> AUTOMATED AUR RELEASE SCRIPT FOR PACTOOL

set -e

# ==> CHECK ARGUMENT
if [ -z "$1" ]; then
    echo "Usage: ./release.sh <new-version>"
    exit 1
fi

NEW_VERSION="$1"

echo "==> Updating AUR package to version $NEW_VERSION..."

# ==> ENSURE WE ARE IN A GIT REPO
if [ ! -d ".git" ]; then
    echo "ERROR: This directory is not a git repository. Clone from AUR first:"
    echo "  git clone ssh://aur@aur.archlinux.org/pactool.git"
    exit 1
fi

# ==> UPDATE PKGBUILD VERSION
echo "==> Updating pkgver in PKGBUILD..."
sed -i "s/^pkgver=.*/pkgver=$NEW_VERSION/" PKGBUILD

# ==> REGENERATE SHA256SUMS
echo "==> Generating new sha256sums..."
sha256=$(makepkg -g 2>/dev/null | tail -n 1 | tr -d "'")
sed -i "s/^sha256sums=.*/sha256sums=('$sha256')/" PKGBUILD

# ==> REGENERATE .SRCINFO
echo "==> Generating .SRCINFO..."
makepkg --printsrcinfo > .SRCINFO

# ==> TEST BUILD LOCALLY
echo "==> Testing local build..."
makepkg -si --noconfirm

# ==> COMMIT CHANGES
echo "==> Committing changes..."
git add PKGBUILD .SRCINFO
git commit -m "Release pactool v$NEW_VERSION"

# ==> PUSH TO AUR
echo "==> Pushing to AUR..."
git push

echo "==> AUR release completed for pactool v$NEW_VERSION."