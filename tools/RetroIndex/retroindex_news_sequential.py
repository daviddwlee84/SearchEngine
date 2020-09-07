import os
import sys
from typing import Dict, Any

curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curr_dir, '../Crawler'))
sys.path.append(os.path.join(curr_dir, '../..'))

from crawler.crawler.news import TencentNewsCrawler, NetEaseNewsCrawler, SinaNewsCrawler, CCTVNewsCrawler
from crawler.data.data_helper import tsv_sequential_processing
# TODO: import index builder


import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--raw-data-tsv', type=str,
                    help='Raw TSV downloaded from RetroIndex.')
parser.add_argument('--output-file', type=str,
                    help='Output file name (json format).')
parser.add_argument('--news-type', type=str,
                    choices=['tencent', 'netease', 'sina', 'cctv'],
                    help='News parser to use.')
# TODO: specify processes number
args = parser.parse_args()

store_in_memory = False
store_in_file = args.output_file

if args.news_type == 'tencent':
    crawler = TencentNewsCrawler(store_in_memory, store_in_file)
elif args.news_type == 'netease':
    crawler = NetEaseNewsCrawler(store_in_memory, store_in_file)
elif args.news_type == 'sina':
    crawler = SinaNewsCrawler(store_in_memory, store_in_file)
elif args.news_type == 'cctv':
    crawler = CCTVNewsCrawler(store_in_memory, store_in_file)


def retro_index_func(parsed_dict: Dict[str, Any]):
    return crawler.crawl_html(parsed_dict['DocHtmlBody'], url=parsed_dict['Url'])


tsv_sequential_processing(
    args.raw_data_tsv, None, retro_index_func)
