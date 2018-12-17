#!/bin/bash
#python classify.py --features ../data/features/ --world closed --k 15 --out res_closed_k15
python classify.py --features ../data/features --train 0.8 --world open --k 10 --out res_open_k10_1800
