#!/bin/bash
PROJECT="Fess"
TITLE="Fess"
LANG="ja"
AUTHOR="CodeLibs"
RELEASE="9.3"

HTMLCOMPRESSOR_JAR=~/lib/htmlcompressor-1.5.3.jar
YUICOMPRESSOR_JAR=~/lib/yuicompressor-2.4.8.jar
TARGET=./_build/html

SCRIPT_DIR=$(cd $(dirname $0);pwd)

CONFDIR="${SCRIPT_DIR}/../conf"
BUILDDIR="${SCRIPT_DIR}/_build"

# Build html
make SPHINXOPTS="-c ${CONFDIR}" BUILDDIR="${BUILDDIR}/${TYPE}" SPHINX_LANG="${LANG}" SPHINX_PROJECT="${PROJECT}" SPHINX_TITLE="${TITLE}" SPHINX_AUTHOR="${AUTHOR}" SPHINX_RELEASE="${RELEASE}" -f ${CONFDIR}/Makefile clean html

# Minify html
#java -jar ${HTMLCOMPRESSOR_JAR} --type html --compress-js --compress-css --recursive -o ./_build/html_compressed/ ./_build/html/
java -jar ${HTMLCOMPRESSOR_JAR} --compress-js --compress-css --recursive -o ${TARGET} ${TARGET}

# Minify js and css
while read file; do
  if [[ ! "${file##*/}" =~ ^.*\.min\..*$ ]]; then
    echo "Compressing $file.."
    java -jar ${YUICOMPRESSOR_JAR} -o $file $file
  fi
done < <(find "${TARGET}" \( -name "*.js" -o -name "*.css" \))
