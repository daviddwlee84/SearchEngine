# Build index for search models
import os
import sys
import pandas as pd
from tqdm import tqdm
import argparse

curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curr_dir)

from search.annoy.build_index import AnnoyIndexBuilder
from search.elastic_search.build_index import ESIndexBuilder


class IndexBuilder(object):
    def __init__(self, annoy_dir: str,
                 es_index: str, es_host: str):
        # Note, currently ANN can only be build from scratch (can't add index after load)
        # unless we store embedding
        self.ann_builder = AnnoyIndexBuilder()
        self.ann_dir = annoy_dir
        self.es_builder = ESIndexBuilder(host=es_host, index=es_index)

    def initialize(self):
        """
        Annoy: remove *.ann, mapping.json, *.pkl
        ES   : delete index

        https://stackoverflow.com/questions/47087741/use-tqdm-progress-bar-with-pandas
        """
        self.ann_builder.remove_old_files(self.ann_dir)
        self.es_builder.clear_old_index()

    def build_indices_for_pandas_object(self, df: pd.DataFrame):
        """
        TODO: dealing with NaN problem (especially pd.NaT in date)
        (currently just ignore the date if NaT in elastic search index builder)
        """
        for i, row in tqdm(df.iterrows(), total=len(df)):

            self.ann_builder.add_index_for_article(index=i, article=row)
            self.es_builder.add_index_for_article(
                index=i, article=dict(row))

    def build_indices_for_json_file(self, json_file: str):
        # TODO: load stuff and convert the data type, this is important if the memory is limited
        pass

    def finish(self):
        self.ann_builder.build_index()
        self.ann_builder.save_index(self.ann_dir)

        self.es_builder.finish_indexing()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--annoy-dir', type=str, default=os.path.join(curr_dir, 'index'),
                        help='Directory to place ANN models and related files.')
    parser.add_argument('--es-host', type=str, default='http://stcadmin-dgx-station-002:9200',
                        help='Elastic search host address.')
    parser.add_argument('--es-index', type=str, default='news',
                        help='Elastic search index to store')
    parser.add_argument('--file', type=str, default=os.path.join(curr_dir, 'tools/Crawler/result/news/all_news.tsv'),
                        help='File to be parse and add')
    parser.add_argument('--initialize', action='store_true',
                        help='Initialize elastic search records (be careful!) and remove annoy model (not necessary).')
    return parser.parse_args()


if __name__ == "__main__":
    from utils.data_loader import load_tsv

    args = parse_args()

    builder = IndexBuilder(
        annoy_dir=args.annoy_dir, es_host=args.es_host, es_index=args.es_index)

    if args.initialize:
        print('Initializing checkpoints and elastic search data.')
        builder.initialize()

    if args.file.endswith('.tsv'):
        df = load_tsv(args.file)
    elif args.file.endswith('.json'):
        from crawler.manager.combine_results import CombineResult
        comb = CombineResult(simplify=True)
        df = comb.load_from_json(args.file)
    else:
        print('Invalid file name', args.file)
        exit()
    builder.build_indices_for_pandas_object(df)
