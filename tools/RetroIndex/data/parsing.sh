#!/bin/bash
echo "Sina"
python3 ../retroindex_news_sequential.py --raw-data-tsv rawdata/HH-sina.tsv --output-file result/parsed-HH-sina.json --news-type sina
echo "Tencent QQ"
python3 ../retroindex_news_sequential.py --raw-data-tsv rawdata/HH-qq.tsv --output-file result/parsed-HH-qq.json --news-type tencent
echo "NetEase 163"
python3 ../retroindex_news_sequential.py --raw-data-tsv rawdata/HH-163.tsv --output-file result/parsed-HH-163.json --news-type netease
echo "CCTV"
python3 ../retroindex_news_sequential.py --raw-data-tsv rawdata/HH-cctv.tsv --output-file result/parsed-HH-cctv.json --news-type cctv
