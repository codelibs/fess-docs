#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0);pwd)

PROJECT="Fess"
TITLE="Fess"
DOCLANG="ja"
AUTHOR="CodeLibs"
RELEASE="14.12"

HTMLCOMPRESSOR_JAR="${SCRIPT_DIR}/../libs/htmlcompressor-1.5.3.jar"
YUICOMPRESSOR_JAR="${SCRIPT_DIR}/../libs/yuicompressor-2.4.8.jar"
TARGET=./_build/html

CONFDIR="${SCRIPT_DIR}/../conf"
BUILDDIR="${SCRIPT_DIR}/_build"

# Build html
make SPHINXOPTS="-c ${CONFDIR}" BUILDDIR="${BUILDDIR}/${TYPE}" SPHINX_LANG="${DOCLANG}" SPHINX_PROJECT="${PROJECT}" SPHINX_TITLE="${TITLE}" SPHINX_AUTHOR="${AUTHOR}" SPHINX_RELEASE="${RELEASE}" -f ${CONFDIR}/Makefile clean html

# Minify html
#java -jar ${HTMLCOMPRESSOR_JAR} --type html --compress-js --compress-css --recursive -o ./_build/html_compressed/ ./_build/html/
java -jar ${HTMLCOMPRESSOR_JAR} --compress-js --compress-css --recursive -o ${TARGET} ${TARGET}

# Minify js and css
#while read file; do
#  if [[ ! "${file##*/}" =~ ^.*\.min\..*$ ]]; then
#    echo "Compressing $file.."
#    java -jar ${YUICOMPRESSOR_JAR} -o $file $file
#  fi
#done < <(find "${TARGET}" \( -name "*.js" -o -name "*.css" \))
