#!/usr/bin/env bash


set -euo pipefail


################################# CONFIG #################################
PKGNAME="pactool"
AUR_REMOTE_NAME="aur"
AUR_URL="ssh://aur@aur.archlinux.org/${PKGNAME}.git"
##########################################################################


usage() { echo "Usage: $0 <new-version>"; exit 1; }
[[ $# -eq 1 ]] || usage
NEW_VER="$1"


TARBALL="${PKGNAME}-${NEW_VER}.tar.gz"
TARBALL_URL="https://github.com/LinuxUtils/${PKGNAME}/archive/refs/tags/v${NEW_VER}.tar.gz"


echo "==> Releasing ${PKGNAME} v${NEW_VER} to AUR…"


[[ -d .git ]] || { echo "Run inside a git repo cloned from anywhere."; exit 1; }


if ! git remote | grep -qx "${AUR_REMOTE_NAME}"; then
  git remote add "${AUR_REMOTE_NAME}" "${AUR_URL}"
else
  git remote set-url "${AUR_REMOTE_NAME}" "${AUR_URL}"
fi


echo "==> Syncing with AUR…"
git fetch "${AUR_REMOTE_NAME}" master
git rebase "${AUR_REMOTE_NAME}/master"


# ------------------------------------------------------------------------------
# Update PKGBUILD
# ------------------------------------------------------------------------------
echo "==> Updating PKGBUILD…"
sed -i "s/^pkgver=.*/pkgver=${NEW_VER}/" PKGBUILD


echo "==> Cleaning old tarballs…"
rm -f "${PKGNAME}-"*.tar.gz


echo "==> Downloading ${TARBALL}…"
curl -Lf -o "${TARBALL}" "${TARBALL_URL}"


echo "==> Generating sha256sum…"
SHA=$(sha256sum "${TARBALL}" | awk '{print $1}')
sed -i "s/^sha256sums=.*/sha256sums=('${SHA}')/" PKGBUILD
echo "    -> ${SHA}"


echo "==> Regenerating .SRCINFO…"
makepkg --printsrcinfo > .SRCINFO


echo "==> Local build test…"
makepkg -si --noconfirm


git add PKGBUILD .SRCINFO
git commit -m "AUR release ${PKGNAME} v${NEW_VER}" || echo "No new changes to commit."


echo "==> Pushing to AUR…"
git push "${AUR_REMOTE_NAME}" HEAD:master


echo "==> Done! AUR now has ${PKGNAME} v${NEW_VER}"
