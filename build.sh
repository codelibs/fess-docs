#!/bin/bash

langs="
ja
en
de
es
fr
zh-cn
"

for lang in $langs ; do
  cd $lang
  bash ./build_html.sh
  cd ..
done

