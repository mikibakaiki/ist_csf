#!/bin/bash
python fextractor.py --traces ../data/cells/ --out ../data/features
python classify.py --features ../data/features/ --world closed --k 5 --out res_closed_k5
python classify.py --features ../data/features --train 0.8 --world open --k 5 --out res_open_k5_1800

