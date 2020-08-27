from typing import List, Tuple
from elasticsearch import Elasticsearch
import os
from itertools import product
from datetime import datetime, timedelta

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '../..'))

# from utils.article_loader import ArticleManager
from search.representation import Encoder


class ESAPIWrapper(object):
    """
    Basically wrapping ES API for some pre-define requests

    TODO: make the condition become "append" style

    TODO (pending): try this [Text similarity search in Elasticsearch using vector fields | Elastic Blog](https://www.elastic.co/blog/text-similarity-search-with-vectors-in-elasticsearch)
    """

    def __init__(self, host: str, index: str):
        self.es = Elasticsearch(host)
        self.es_index = index
        self.encoder = Encoder()  # currently unused

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

    def _perform_query(self, query_body: dict, size: int):
        res = self.es.search(index=self.es_index, size=size, body=query_body)
        return [(item['_source'], item['_score']) for item in res['hits']['hits']]

    def search_keywords(self, keywords: List[str], keyword_fields: List[str] = ['title', 'content'], size: int = 10):
        body = {
            'query': {
                'bool': {
                    'should': [
                        {'match': {
                            field: keyword
                        }} for field, keyword in product(keyword_fields, keywords)
                    ]
                }
            }
        }
        return self._perform_query(body, size)

    def search_keywords_in_date_range(self, keywords: List[str], start_date: datetime, end_date: datetime,
                                      keyword_fields: List[str] = ['title', 'content'], date_field: str = 'date', size: int = 10):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html
        https://www.elastic.co/guide/en/elasticsearch/reference/master/sql-functions-datetime.html
        https://stackoverflow.com/questions/33246344/querying-elasticsearch-by-combining-a-range-and-a-term-match-json-format
        https://www.elastic.co/guide/en/elasticsearch/reference/current/compound-queries.html

        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-daterange-aggregation.html
        """
        body = {
            'query': {
                'bool': {
                    'filter': [{
                        'range': {
                            'date': {
                                # seems these are the same
                                # 'gte': start_date,
                                # 'lte': end_date,
                                'from': start_date,
                                'to': end_date
                            }
                        }
                    }],
                    'should': [
                        {'match': {
                            field: keyword
                        }} for field, keyword in product(keyword_fields, keywords)
                    ],
                }
            }
        }
        return self._perform_query(body, size)

    def search_keywords_in_date_within(self, keywords: List[str], current_date: datetime, within_days: int = 10,
                                       keyword_fields: List[str] = ['title', 'content'], date_field: str = 'date', size: int = 10):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math
        http://www.pressthered.com/adding_dates_and_times_in_python/
        https://www.programiz.com/python-programming/datetime/strftime

        https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html

        TODO: use Date Math instead
        """
        start_date = current_date - timedelta(days=within_days // 2)
        end_date = current_date + timedelta(days=within_days // 2)
        return self.search_keywords_in_date_range(keywords=keywords, keyword_fields=keyword_fields,
                                                  date_field=date_field, size=size,
                                                  start_date=start_date,
                                                  end_date=end_date)

    # def search_with_embedding(self, string: str, mode: str = 'sentence'):
    #     """
    #     mode

    #     * title => search title only
    #     * article => search content
    #     * sentence: TODO maybe we have to create sentence index in ES?!
    #     * paragraph: TODO maybe we have to create paragraph index in ES?!

    #     TODO: https://github.com/jtibshirani/text-embeddings/blob/master/src/main.py

    #     This is a current limitation of vector similarity in Elasticsearch — vectors can be used for scoring documents, but not in the initial retrieval step. Support for retrieval based on vector similarity is an important area of ongoing work.

    #     (Might need to wait for future version....)
    #     """
    #     query_vector

    #     script_query = {
    #         'script_score': {
    #             'query': {'match_all': {}},
    #             'script': {
    #                 'source': 'cosineSimilarity(params.query_vector, doc["title_vector"]) + 1.0',
    #                 'params': {'query_vector': query_vector}
    #             }
    #         }
    #     }


if __name__ == "__main__":
    es = ESAPIWrapper('http://stcadmin-dgx-station-002:9200', 'news')
    # es.get_all(print_all=True)
    # print(es.search_keywords(['TikTok']))
    # print(es.search_keywords(['老人']))
    print(es.search_keywords(['TikTok', '美国', '特朗普']))

    # print([(result['title'], score)
    #        for result, score in es.search_keywords(['TikTok'])])
    # print([(result['title'], score)
    #        for result, score in es.search_keywords(['老人'])])

    # print(es.search_keywords_in_date_range('TikTok', start_date=datetime(
    #     year=2020, month=8, day=19), end_date=datetime.now()))

    # print(es.search_keywords_in_date_within(['TikTok'], current_date=datetime(
    #     year=2020, month=8, day=19), within_days=10))

# GET news/_search
# {
#   "query": {
#     "range": {
#       "date": {
#         "time_zone": "+01:00",
#         "gte": "2020-01-01T00:00:00",
#         "lte": "now"
#       }
#     }
#   }
# }
