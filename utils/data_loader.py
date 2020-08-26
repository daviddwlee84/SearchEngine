from typing import List
import pandas as pd
import json
from datetime import datetime

default_data_type = {
    # 'url': 'str',
    # 'domain': 'str',
    # 'html_title': 'str',
    # 'html_body': 'str',
    # 'title': 'str',
    # 'author': 'str',
    'date': 'datetime64[ns]',
    # 'content': 'str',
    'parse_date': 'datetime64[ns]',
    # 'meta': 'object',  # there is some problem of storing dict in pandas
}


def load_tsv(tsv_path: str):
    """
    Load tsv file and recover its data type (especially the datetime)

    For more detail, checkout tools/Crawler/crawler/manager/combine_results
    """
    data = pd.read_csv(tsv_path, sep='\t')
    data_type = {key: value
                 for key, value in default_data_type.items()
                 if key in data.columns.to_list()}
    return data.astype(data_type)


import os
import sys

curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curr_dir, '../tools/Crawler'))
from crawler.manager.combine_results import CombineResult


def load_json(json_path: str, simplify: bool = False, simplify_columns: List[str] = ['title', 'author', 'date', 'content']):
    """
    Load json file and recover its data type (especially the datetime)

    For more detail, checkout tools/Crawler/crawler/manager/combine_results

    The file should be the format of "each line one json object"

    (use crawler's function)
    TODO: not sure if we have to delete the manager object manually
    """
    manager = CombineResult(
        simplify=simplify, default_data_type=default_data_type)
    manager.load_from_json(json_path)
    return manager.data.copy()


# TODO

# def _to_datetime(date_str: str):
#     pass
#
# data_func = {
#     'datetime64[ns]': _to_datetime
# }
#
# def load_json(json_path: str):
#     """
#     Load json file and recover its data type (especially the datetime)
#
#     For more detail, checkout tools/Crawler/crawler/manager/combine_results
#
#     The file should be the format of "each line one json object"
#     """
#     data = []
#     with open(json_path, 'r', encoding='utf8') as stream:
#         for line in stream:
#             raw_data = json.loads(line.strip(), encoding='utf-8')
#
#             data.append({})
