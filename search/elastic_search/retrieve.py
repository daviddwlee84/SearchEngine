from typing import List, Tuple
from elasticsearch import Elasticsearch
import os
from datetime import datetime, timedelta

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '../..'))

# from utils.article_loader import ArticleManager

HOST = 'http://stcadmin-dgx-station-002:9200'


class ESAPIWrapper(object):
    """
    Basically wrapping ES API for some pre-define requests

    TODO: make the condition become "append" style
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

    def _perform_query(self, query_body: dict, size: int):
        res = self.es.search(index=self.es_index, size=size, body=query_body)
        return [(item['_source'], item['_score']) for item in res['hits']['hits']]

    def search_keyword(self, keyword: str, keyword_fields: List[str] = ['title', 'content'], size: int = 10):
        body = {
            'query': {
                'bool': {
                    'should': [
                        {'match': {
                            field: keyword
                        }} for field in keyword_fields
                    ]
                }
            }
        }
        return self._perform_query(body, size)

    def search_keyword_in_date_range(self, keyword: str, start_date: datetime, end_date: datetime,
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
                        }} for field in keyword_fields
                    ],
                }
            }
        }
        return self._perform_query(body, size)

    def search_keyword_in_date_within(self, keyword: str, current_date: datetime, within_days: int = 10,
                                      keyword_fields: List[str] = ['title', 'content'], date_field: str = 'date', size: int = 10):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math
        http://www.pressthered.com/adding_dates_and_times_in_python/
        https://www.programiz.com/python-programming/datetime/strftime

        https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html
        """
        start_date = current_date - timedelta(days=within_days // 2)
        end_date = current_date + timedelta(days=within_days // 2)
        return self.search_keyword_in_date_range(keyword=keyword, keyword_fields=keyword_fields,
                                                 date_field=date_field, size=size,
                                                 start_date=start_date,
                                                 end_date=end_date)

        # Date Math has bug....
        # print(current_date.strftime("%Y-%m-%d"'T'"%H:%M:%S"))
        # body = {
        #     'query': {
        #         'bool': {
        #             'filter': [{
        #                 'range': {
        #                     'date': {
        #                         # 'gte': current_date.strftime("%Y-%m-%d"'T'"%H:%M:%S") + f'-{within_days//2}d/d',
        #                         # 'lte': current_date.strftime("%Y-%m-%d"'T'"%H:%M:%S") + f'+{within_days//2}d/d',
        #                         'from': current_date.strftime("%Y-%m-%d"'T'"%H:%M:%S") + f'-{within_days//2}d/d',
        #                         'to': current_date.strftime("%Y-%m-%d"'T'"%H:%M:%S") + f'+{within_days//2}d/d',
        #                     }
        #                 }
        #             }],
        #             'should': [
        #                 {'match': {
        #                     field: keyword
        #                 }} for field in keyword_fields
        #             ],
        #         }
        #     }
        # }
        # return self._perform_query(body, size)


if __name__ == "__main__":
    es = ESAPIWrapper('news')
    # es.get_all(print_all=True)
    # print(es.search_keyword('TikTok'))
    # print(es.search_keyword('老人'))

    # print([(result['title'], score)
    #        for result, score in es.search_keyword('TikTok')])
    # print([(result['title'], score)
    #        for result, score in es.search_keyword('老人')])

    # print(es.search_keyword_in_date_range('TikTok', start_date=datetime(
    #     year=2020, month=8, day=19), end_date=datetime.now()))

    print(es.search_keyword_in_date_within('TikTok', current_date=datetime(
        year=2020, month=8, day=19), within_days=10))

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
