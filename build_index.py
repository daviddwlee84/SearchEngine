# Build index for search models
from search.annoy.build_index import AnnoyIndexBuilder
from search.elastic_search.build_index import ESIndexBuilder
import os
import pandas as pd
from tqdm import tqdm


class IndexBuilder(object):
    def __init__(self, annoy_dir: str,
                 es_index: str, es_host: str):
        self.ann_builder = AnnoyIndexBuilder()
        self.ann_dir = annoy_dir
        self.es_builder = ESIndexBuilder(host=es_host, index=es_index)

    def initialize(self):
        """
        Annoy: remove *.ann, mapping.json
        ES   : delete index

        https://stackoverflow.com/questions/47087741/use-tqdm-progress-bar-with-pandas
        """
        for item in os.listdir(self.ann_dir):
            if item.endswith('.ann') or item.endswith('.json'):
                os.remove(os.path.join(self.ann_dir, item))

        self.es_builder.clear_old_index()

    def build_indices_for_pandas_object(self, df: pd.DataFrame, es_doc_type: str = 'raw'):
        """
        TODO: dealing with NaN problem (especially pd.NaT in date)
        (currently just ignore the date if NaT in elastic search index builder)
        """
        for i, row in tqdm(df.iterrows(), total=len(df)):

            self.ann_builder.add_index_for_article(index=i, article=row)
            self.es_builder.add_index_for_article(
                index=i, article=dict(row), doc_type=es_doc_type)

        self.ann_builder.build_index()
        self.ann_builder.save_index(self.ann_dir)

        self.es_builder.finish_indexing()


if __name__ == "__main__":
    from utils.data_loader import load_tsv
    builder = IndexBuilder(
        annoy_dir='index', es_host='http://stcadmin-dgx-station-002:9200', es_index='news')
    df = load_tsv('data/all_news_new.tsv')
    builder.build_indices_for_pandas_object(df)
