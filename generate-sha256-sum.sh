#!/bin/bash


PKGNAME="pactool"


# ==> CLEANING
if [[ "$1" == "--clean" ]]; then
    if [ -z "$2" ]; then
        echo "Usage: ./generate-sha256.sh --clean <version>"
        exit 1
    fi
    FILE="$PKGNAME-$2.tar.gz"
    if [ -f "$FILE" ]; then
        echo "==> Removing $FILE..."
        rm -f "$FILE"
        echo "==> Cleaned."
    else
        echo "==> No file found: $FILE"
    fi
    exit 0
fi


# ==> GENERATE CHECKSUM
VERSION="$1"
if [ -z "$VERSION" ]; then
    echo "Usage: ./generate-sha256.sh <version> or ./generate-sha256.sh --clean <version>"
    exit 1
fi


URL="https://github.com/LinuxUtils/$PKGNAME/archive/refs/tags/v$VERSION.tar.gz"
FILE="$PKGNAME-$VERSION.tar.gz"


echo "==> Downloading $URL..."
curl -L -o "$FILE" "$URL"


echo "==> Generating SHA256SUM for $FILE..."
sha256sum "$FILE"
