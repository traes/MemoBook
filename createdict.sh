#!/bin/bash

rm -- words.txt
aspell -d en dump master | aspell -l en expand | uniq >> words.txt
aspell -d nl dump master | aspell -l nl expand | uniq >> words.txt
aspell -d de dump master | aspell -l de expand | uniq >> words.txt

