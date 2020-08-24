from typing import List, Tuple
from elasticsearch import Elasticsearch
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '../..'))

# from utils.article_loader import ArticleManager

HOST = 'http://stcadmin-dgx-station-002:9200'


class ESAPIWrapper(object):
    """
    Basically wrapping ES API for some pre-define requests
    """

    def __init__(self, index: str, host: str = HOST):
        self.es = Elasticsearch(host)
        self.es.indices.refresh(index=index)
        self.es_index = index

    def get_idx(self, idx: int):
        """
        TODO: handle if idx is invalid
        """
        return self.es.get(index=self.es_index, id=idx)['_source']

    def get_all(self, print_all: bool = False, size: int = 10):
        """
        (Just a test function)

        make default size to unlimit
        """
        res = self.es.search(index=self.es_index, size=size,
                             body={'query': {'match_all': {}}})
        print("Got %d Hits:" % res['hits']['total']['value'])
        if print_all:
            for hit in res['hits']['hits']:
                print("%(title)s %(date)s %(author)s: %(content)s" %
                      hit['_source'])

    def search_keyword(self, keyword: str, fields: List[str] = ['title', 'content'], size: int = 10):
        body = {
            'query': {
                'bool': {
                    'should': [
                        {'match': {
                            field: keyword
                        }} for field in fields
                    ]
                }
            }
        }

        res = self.es.search(index=self.es_index, size=size, body=body)
        return [(item['_source'], item['_score']) for item in res['hits']['hits']]


if __name__ == "__main__":
    es = ESAPIWrapper('news')
    # es.get_all(print_all=True)
    print(es.search_keyword('TikTok'))
    print(es.search_keyword('老人'))
