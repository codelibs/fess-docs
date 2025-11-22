#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0);pwd)

DOCLANG="ko"
AUTHOR="CodeLibs"
RELEASE="15.3"

CONFDIR="${SCRIPT_DIR}/../conf"
BUILDDIR="${SCRIPT_DIR}/_build/pdf/${RELEASE}"

PROJECT="FessConfig"
TITLE="Fess 설정 가이드"
TYPE="config"
echo "Processing ${SCRIPT_DIR}/${RELEASE}/${TYPE}"
cd ${SCRIPT_DIR}/${RELEASE}/${TYPE}
make SPHINXOPTS="-c ${CONFDIR}" BUILDDIR="${BUILDDIR}/${TYPE}" SPHINX_LANG="${DOCLANG}" SPHINX_PROJECT="${PROJECT}" SPHINX_TITLE="${TITLE}" SPHINX_AUTHOR="${AUTHOR}" SPHINX_RELEASE="${RELEASE}" -f ${CONFDIR}/Makefile latexpdfja
