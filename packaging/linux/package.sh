#!/bin/sh

set -e

# check if CELLS_VERSION is set
if [ -z "${CELLS_VERSION}" ] || [ -z "${CELLS_REVISION_NUMBER}" ]; then
    echo "\$CELLS_VERSION and \$CELLS_REVISION_NUMBER have to be set before running this script."
    exit 1
fi

PACKAGE_DIR=dist/package/linux
DEB_PACK_DIR=$PACKAGE_DIR/cells-$CELLS_VERSION

poetry install
poetry shell

echo "Cleaning up build/ and dist/"
rm -rf build/*
rm -rf dist/*

echo "Compiling binary"
pyinstaller packaging/Cells.spec -y

echo "Copying app icon"
cp ./packaging/linux/AppIcon.png ./dist/Cells/

echo "Creating debian package structure"
mkdir -p $DEB_PACK_DIR
mkdir -p $DEB_PACK_DIR/DEBIAN

echo "Creating debian control file"
echo "Package: cells\n\
Version: ${CELLS_VERSION}\n\
Maintainer: Ales Tsurko <ales.tsurko@gmail.com>\n\
Description: Live coding environment.\n\
Homepage: https://github.com/AlesTsurko/cells\n\
Recommends: \
chezscheme9.5, \
haskell-platform, \
lua | lua5.3, \
nodejs, \
python | python3 | python3.7, \
ruby-full, \
sbcl, \
supercollider-ide | supercollider\n\
Architecture: amd64" > $DEB_PACK_DIR/DEBIAN/control

echo "Copying postinst"
cp packaging/linux/postinst $DEB_PACK_DIR/DEBIAN/

echo "Copying track templates"
mkdir -p $DEB_PACK_DIR/tmp/track_templates
cp -R ./track_templates/* $DEB_PACK_DIR/tmp/track_templates

echo "Generating cells.desktop"
echo "\
[Desktop Entry]
Version=${CELLS_VERSION}
Name=Cells
Coment=Live coding environment
Exec=/usr/share/Cells/Cells
Icon=/usr/share/Cells/AppIcon.png
Terminal=false
Type=Application
Categories=Utility;Application;\
" > $DEB_PACK_DIR/tmp/cells.desktop
chmod +x $DEB_PACK_DIR/tmp/cells.desktop

echo "Packaging binaries"
mkdir -p $DEB_PACK_DIR/usr/share/Cells
mv dist/Cells/* $DEB_PACK_DIR/usr/share/Cells

echo "Building package"
dpkg -b $DEB_PACK_DIR $PACKAGE_DIR/cells-${CELLS_VERSION}-${CELLS_REVISION_NUMBER}_amd64.deb

echo "Archiving"
zip -jrX $PACKAGE_DIR/cells-${CELLS_VERSION}-${CELLS_REVISION_NUMBER}_amd64.deb.zip \
    $PACKAGE_DIR/cells-${CELLS_VERSION}-${CELLS_REVISION_NUMBER}_amd64.deb

echo "Cleaning up"
rm -rf $DEB_PACK_DIR
rm -rf dist/Cells
