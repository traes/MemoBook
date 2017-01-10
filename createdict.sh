#!/bin/bash

rm -- words.txt tmp.txt
aspell -d en dump master | aspell -l en expand | uniq >> tmp.txt
aspell -d nl dump master | aspell -l nl expand | uniq >> tmp.txt
aspell -d de dump master | aspell -l de expand | uniq >> tmp.txt
aspell -d es dump master | aspell -l es expand | uniq >> tmp.txt

cat tmp.txt | awk '{print $1}' | iconv -f utf8 -t ascii//TRANSLIT | uniq > words.txt

