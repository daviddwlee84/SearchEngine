import os
import sys
from typing import Dict, Any

curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curr_dir, '../Crawler'))
sys.path.append(os.path.join(curr_dir, '../..'))

from crawler.crawler.news import TencentNewsCrawler, NetEaseNewsCrawler, SinaNewsCrawler
from crawler.data.data_helper import tsv_parallel_processing
# TODO: import index builder


import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--raw-data-tsv', type=str,
                    help='Raw TSV downloaded from RetroIndex.')
parser.add_argument('--output-file', type=str,
                    help='Output file name (json format).')
parser.add_argument('--news-type', type=str,
                    choices=['tencent', 'netease', 'sina'],
                    help='News parser to use.')
parser.add_argument('--num-processes', type=int, default=None,
                    help='Number of processes, default cpu cores.')
# TODO: specify processes number
args = parser.parse_args()

store_in_memory = False
store_in_file = None

# if args.news_type == 'tencent':
#     crawler = TencentNewsCrawler(store_in_memory, store_in_file)
# elif args.news_type == 'netease':
#     crawler = NetEaseNewsCrawler(store_in_memory, store_in_file)
# elif args.news_type == 'sina':
#     crawler = SinaNewsCrawler(store_in_memory, store_in_file)
# def retro_index_func(parsed_dict: Dict[str, Any]):
#     return crawler.crawl_html(parsed_dict['DocHtmlBody'], url=parsed_dict['Url'])

if args.news_type == 'tencent':
    crawler_obj = TencentNewsCrawler
elif args.news_type == 'netease':
    crawler_obj = NetEaseNewsCrawler
elif args.news_type == 'sina':
    crawler_obj = SinaNewsCrawler
def retro_index_func(parsed_dict: Dict[str, Any]):
    # Beautiful Soup multithread problem
    # RecursionError: maximum recursion depth exceeded in comparison
    # [python - Maximum recursion depth exceeded. Multiprocessing and bs4 - Stack Overflow](https://stackoverflow.com/questions/52021254/maximum-recursion-depth-exceeded-multiprocessing-and-bs4)
    global crawler_obj
    crawler = crawler_obj(False, None)
    return crawler.crawl_html(parsed_dict['DocHtmlBody'], url=parsed_dict['Url'])


def retro_index_and_es_index_build_func():
    # TODO
    pass


# TODO: THIS FUNCTION HAVEN't COMPLETED (NEED TO SOLVE THE RECURSION ERROR)
sys.setrecursionlimit(25000 * 4)

tsv_parallel_processing(
    args.raw_data_tsv, args.output_file, retro_index_func, numprocesses=args.num_processes)
