#!/bin/sh

set -e

PACKAGES_PATH=dist/packages/macos
APP=dist/Cells.app
APPDIR=$APP/Contents/MacOS
APPRESOURCES=$APP/Contents/Resources

# init virtual environment
poetry install


echo "Cleaning up dist/ and build/"
rm -rf dist/*
rm -rf build/*

echo "Making app structure"
mkdir -p $APPDIR
mkdir -p $APPRESOURCES

# pyinstaller packaging/Cells.spec -y

echo "Copying sources"
cp -R cells $APPDIR

echo "Copying python"
cp -R ./packaging/macos/python $APPDIR

echo "Copying dependencies"
cp -n -R .venv/lib/python3.7/site-packages/ ${APPDIR}/python/lib/python3.7/site-packages/ || true

echo "Copying resources"
cp -R resources $APPDIR

echo "Copying icons"
cp packaging/macos/*.icns $APPRESOURCES/

echo "Copying executable scripts"
cp packaging/macos/runner $APPDIR
cp packaging/macos/run $APPDIR

echo "Writing defaults"
defaults write $PWD/$APP/Contents/Info.plist CFBundleName -string Cells
defaults write $PWD/$APP/Contents/Info.plist CFBundleDisplayName -string Cells
defaults write $PWD/$APP/Contents/Info.plist CFBundleIdentifier -string by.alestsurko.cells
defaults write $PWD/$APP/Contents/Info.plist CFBundleVersion -string "1.0.0"
defaults write $PWD/$APP/Contents/Info.plist CFBundleExecutable -string runner
defaults write $PWD/$APP/Contents/Info.plist NSPrincipalClass -string NSApplication
defaults write $PWD/$APP/Contents/Info.plist CFBundleIconFile -string "AppIcon"
plutil -insert CFBundleDocumentTypes -json '[{ 
    "CFBundleTypeName": "Cells Document Format", 
    "CFBundleTypeIconFile": "DocumentIcon.icns", 
    "CFBundleTypeOSTypes": [".cls"],
    "CFBundleTypeExtensions": ["cells"],
    "CFBundleTypeRole": "Editor", 
    "LSHandlerRank": "Owner", 
    "LSItemContentTypes": ["by.alestsurko.cells.document"],
    "LSTypeIsPackage": false
}, { 
    "CFBundleTypeName": "Cells Track Template Format",
    "CFBundleTypeRole": "Viewer",
    "CFBundleTypeIconFile": "TrackTemplateIcon.icns", 
    "LSHandlerRank": "Owner", 
    "LSItemContentTypes": ["by.alestsurko.cells.ctt"],
    "CFBundleTypeExtensions": ["ctt"],
    "CFBundleTypeOSTypes": [".ctt"],
    "LSTypeIsPackage": false
}]' $PWD/$APP/Contents/Info.plist

echo "Setting permissions"
chmod -R 755 $APP

# Packaging
mkdir -p $PACKAGES_PATH

echo "Packaging application"
pkgbuild --identifier by.alestsurko.cells \
         --install-location /Applications \
         --component dist/Cells.app \
         $PACKAGES_PATH/_cells.pkg

echo "Packaging templates"
mkdir -p /tmp/track_templates
pkgbuild --identifier by.alestsurko.cells.ctt \
         --install-location /tmp/track_templates \
         --scripts packaging/macos/scripts/ \
         --root track_templates \
         $PACKAGES_PATH/_templates.pkg

echo "Synthesizing Distribution.xml"
productbuild --synthesize \
             --package $PACKAGES_PATH/_cells.pkg \
             --package $PACKAGES_PATH/_templates.pkg \
             $PACKAGES_PATH/Distribution.xml

echo "Generating final package"
productbuild --distribution $PACKAGES_PATH/Distribution.xml \
             --package-path $PACKAGES_PATH \
             $PACKAGES_PATH/Cells.pkg

echo "Archiving"
zip -jrX $PACKAGES_PATH/Cells.pkg.zip $PACKAGES_PATH/Cells.pkg

echo "Cleaning up"
rm -f $PACKAGES_PATH/_cells.pkg
rm -f $PACKAGES_PATH/_templates.pkg
rm -rf dist/Cells.app
