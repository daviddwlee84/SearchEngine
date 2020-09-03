#!/bin/bash

# Still have bug
# python3 retroindex_news_parallel.py --raw-data-tsv netease_test.tsv --output-file netease_output.json --news-type netease --num-processes 1

python3 retroindex_news_sequential.py --raw-data-tsv netease_test.tsv --output-file netease_output.json --news-type netease
