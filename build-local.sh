#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export JAVA_HOME="${JAVA_HOME:-/tmp/krishna-jdk/usr/lib/jvm/java-17-openjdk-amd64}"
export PATH="$JAVA_HOME/bin:$PATH"
BT="${ANDROID_BUILD_TOOLS:-/tmp/madhava-sdk/build-tools/android-15}"
AJ="${ANDROID_JAR:-/tmp/madhava-sdk/platform/android-35/android.jar}"
mkdir -p build/classes build/dex
node_modules/.bin/esbuild web/app.js --bundle --minify --target=chrome100 --outfile=app/src/main/assets/app.js
cp web/index.html web/style.css web/pcm-worklet.js app/src/main/assets/
"$BT/aapt2" compile --dir app/src/main/res -o build/resources.zip
"$BT/aapt2" link -o build/unsigned.apk --manifest app/src/main/AndroidManifest.xml -I "$AJ" -A app/src/main/assets build/resources.zip --auto-add-overlay
javac -source 8 -target 8 -classpath "$AJ" -d build/classes app/src/main/java/in/madhava/companion/MainActivity.java
"$BT/d8" --lib "$AJ" --min-api 26 --output build/dex $(find build/classes -name '*.class')
python3 - <<'PY'
from zipfile import ZipFile,ZIP_DEFLATED
with ZipFile('build/unsigned.apk','a',ZIP_DEFLATED) as z:z.write('build/dex/classes.dex','classes.dex')
PY
"$BT/zipalign" -f 4 build/unsigned.apk build/aligned.apk
if [ ! -f development.jks ]; then
 keytool -genkeypair -keystore development.jks -storepass android -keypass android -alias madhava -dname 'CN=Madhava Personal Build' -keyalg RSA -keysize 2048 -validity 10000 >/dev/null 2>&1
fi
"$BT/apksigner" sign --ks development.jks --ks-key-alias madhava --ks-pass pass:android --key-pass pass:android --out build/Madhava-v1.31.apk build/aligned.apk
"$BT/apksigner" verify --verbose build/Madhava-v1.31.apk
