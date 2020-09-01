from typing import Dict, List
from elasticsearch import Elasticsearch
import pandas as pd
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '../..'))

# from utils.article_loader import ArticleManager

HOST = 'http://stcadmin-dgx-station-002:9200'


class ESIndexBuilder(object):
    """
    Build index for entire article details (i.e. online version pandas?!)
    (Currently no preprocessing before uploading to server)
    """

    def __init__(self, index: str, host: str = HOST):
        self.es = Elasticsearch(host)
        self.es_index = index

        # self.article_manager = ArticleManager()

    def clear_old_index(self):
        """
        TODO: maybe sent a warning message
        """
        self.es.indices.delete(self.es_index, ignore=[404])

    def clear_old_types(self, to_del: List[str], del_all: bool = False):
        pass  # TODO

    def add_index_for_article(self, index: int, article: Dict[str, str]):
        """
        article is a dict
        {
            title: "",
            content: "",
            ...
        }

        TODO: ElasticsearchDeprecationWarning: [types removal]
        Specifying types in document index requests is deprecated,
        use the typeless endpoints instead (/{index}/_doc/{id}, /{index}/_doc, or /{index}/_create/{id})

        https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-data-types.html
        """
        # Remove unsupported data type
        types_to_skip = [pd.NaT]  # dict is okay for ES
        data = {key: value
                for key, value in article.items()
                if type(value) not in types_to_skip and not pd.isna(value)}
        # data = article

        try:
            self.es.index(index=self.es_index, id=index, body=data)
        except Exception as e:
            # https://stackoverflow.com/questions/4690600/python-exception-message-capturing
            print('Elastic search add index fail:', str(e))
            # TypeError("Unable to serialize NaT (type: <class 'pandas._libs.tslibs.nattype.NaTType'>)

    def finish_indexing(self):
        """
        Make sure to call this after you done with all your `add_index_for_article`
        """
        self.es.indices.refresh(index=self.es_index)


if __name__ == "__main__":
    from datetime import datetime

    article_content = """今日，华人运通与微软在2020世界人工智能大会云端峰会（WAIC 2020）上宣布双方达成战略合作，依托微软小冰人工智能技术，共同在高合汽车上落地全球首个主动式人工智能伙伴HiPhiGo，致力于从智慧车机的前装设计阶段开始提供整体解决方案，为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。双方正在探讨成立联合智能计算实验室，以智能汽车为载体，在智捷交通等多个领域展开深度合作。通过人工智能等前瞻技术研发和应用，推动智慧出行和社会可持续发展。 华人运通董事长丁磊与微软（亚洲）互联网工程院院长王永东在“2020世界人工智能大会云端峰会”上共同宣布了双方的战略合作的相关内容。依托微软小冰人工智能技术，微软与华人运通的合作致力于从智慧车机的前装设计阶段开始提供整体解决方案，致力于为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。 王永东表示，人工智能在各领域的应用落地，离不开相关企业和科技公司的携手努力。微软在计算机语音、计算机视觉、自然语言处理、搜索引擎和知识图谱方面均有深厚的技术积累。例如在微软的语音合成领域（Text to speech），依托深度神经网络，可合成出自然而富有情感、足以媲美人类的声音，使用户与人工智能的交互流畅愉悦。微软希望每一项技术能力，都不是高堂上远的秀科技，而能落实为人人可亲自使用的实际产品。华人运通在设计、工程开发、智能系统等方面拥有丰富的经验，一直走在创新前列，在车路城一体化发展方面有着全面布局和成功实践。此次微软与华人运通的合作，使人工智能技术有了切实可行的落地场景，得以转化为真实有效的生产力，发挥更大的应用价值。微软与华人运通将携手推进人工智能等新兴科技在汽车智慧乃至智慧出行领域的广泛应用，为产业升级和社会可持续发展注入新的活力。 丁磊表示，华人运通从城市可持续发展的层面出发，提出“智能汽车、智捷交通、智慧城市”的战略，实现车更聪明，路更互联，城更智慧的人类未来出行愿景。此次合作是顶级人工智能企业和智能汽车公司的强强联手，是AI多项领先技术在全球汽车行业的首次量产落地，在世界范围内具有技术领先性。

    在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。 伴随智能科技与通信技术的革新，汽车正在向超级移动智能终端进化，成为人们智慧生活的重要载体。基于自主研发的开放式电子电气架构，华人运通打造了具备推理能力，能主动感知用户、帮助用户的主动式人工智能伙伴 HiPhiGo，并在高合汽车首款量产车上实现落地，树立智能汽车的全球新标杆。 从首款智能汽车高合HiPhi 有条不紊地推进，到全球首条车路协同自动驾驶智能化城市道路示范项目在盐城开通试运行，再到全球首个车路城一体化5G无人驾驶交通运营样板在上海张江未来公园成功落地，华人运通以人为本，从人性化需求出发，通过人性化智慧，打造“智能汽车、智捷交通、智慧城市“。目前，“三智”战略各项业务稳步推进。高合首款量产车HiPhi将于2020年底实现小批量试生产，2021年上市交付。 人工智能是21世纪技术变革的驱动力，也是产业变革、经济社会发展的驱动力。未来，微软将与华人运通开展更深入的合作，通过人工智能技术为用户带来更多创新体验，共同推动交通产业进步和出行方式进步，使每个人都能从人工智能技术的发展中获益。"""

    test_article = {
        'title': '华人运通与微软达成战略合作，高合汽车落地全球首个主动式人工智能伙伴HiPhiGo',
        'author': 'test',
        'date': datetime.now(),
        'content': article_content,
        'unsupported_type': {'whatever': 'just for test'}
    }

    idx = 0

    builder = ESIndexBuilder(index='test-index')
    builder.add_index_for_article(idx, test_article, 'test')

    # Test

    res = builder.es.get(index='test-index', id=idx)
    print(res['_source'])

    # builder.es.indices.refresh(index='test-index')
    builder.finish_indexing()  # equivalent

    res = builder.es.search(
        index='test-index', body={'query': {'match_all': {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(title)s %(date)s %(author)s: %(content)s" % hit['_source'])
