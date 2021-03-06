from typing import Dict
from annoy import AnnoyIndex
import os
import json

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '../..'))

from search.representation import Encoder
from utils.article_loader import ArticleManager


class AnnoyIndexBuilder(object):
    """
    Build index for different granularities, objects

    1. Title
    2. Content (entire article)
    3. Paragraph
    4. Sentence
    """

    def __init__(self, encoder_model: str = 'bert', metric: str = 'angular'):
        assert encoder_model in ['bert', 'sent-transformer']
        assert metric in ['angular', 'euclidean',
                          'manhattan', 'hamming', 'dot']

        if encoder_model == 'bert':
            self.emb_dim = 768
        elif encoder_model == 'sent-transformer':
            self.emb_dim = 512
        self.encoder_model = encoder_model
        self.encoder = Encoder(encoder_model=encoder_model)

        self.article_manager = ArticleManager()

        self.annoy_title = AnnoyIndex(self.emb_dim, metric)
        self.annoy_article = AnnoyIndex(self.emb_dim, metric)
        self.annoy_paragraph = AnnoyIndex(self.emb_dim, metric)
        self.annoy_sentence = AnnoyIndex(self.emb_dim, metric)

        self.paragraph_id = 0
        self.paragraph2articleid = {}
        self.paragraph_id2structure = {}
        self.sentence_id = 0
        self.sentence2articleid = {}
        self.sentence_id2structure = {}

    def remove_old_files(self, annoy_dir: str = None):
        """
        Maybe this is not necessary (because we can overwrite the file directly)
        """
        if not annoy_dir:
            annoy_dir = curr_dir

        for item in os.listdir(annoy_dir):
            if item.endswith('.ann') or item.endswith('.json') or item.endswith('.pkl'):
                os.remove(os.path.join(annoy_dir, item))

    def recover_from_embedding(self, annoy_dir: str = None):
        """
        TODO Store embedding mapped with index

        To continuous build index from last checkpoint use this function
        (not sure if it's possible...) => Exception: You can't add an item to a loaded index
        https://github.com/spotify/annoy/issues/411
        TODO: the only way is to store the embedding/raw vectors separately and rebuild again.

        TODO: make annoy_dir an __init__ argument
        and attempt to load from the beginning
        return True or False to show if it success
        """
        raise NotImplementedError()

        if not annoy_dir:
            annoy_dir = curr_dir

        # TODO
        os.path.join(annoy_dir, f'title_embedding_map.pkl')
        os.path.join(annoy_dir, f'article_embedding_map.pkl')
        os.path.join(annoy_dir, f'paragraph_embedding_map.pkl')
        os.path.join(annoy_dir, f'sentence_embedding_map.pkl')

        with open(os.path.join(annoy_dir, f'mapping.json'), 'r') as fp:
            data = json.load(fp)
            self.sentence_id = data['sentence_id']
            self.paragraph_id = data['paragraph_id']
            self.sentence2articleid = data['sentence2articleid']
            self.paragraph2articleid = data['paragraph2articleid']
            self.sentence_id2structure = data['sentence_id2structure']
            self.paragraph_id2structure = data['paragraph_id2structure']

    def add_index_for_article(self, index: int, article: Dict[str, str]):
        """
        Make sure index is unique!!

        article is a dict
        {
            title: "",
            content: "",
            ... (the rest will be ignore)
        }
        TODO: maybe split text or use other algorithm to obtain
              embedding that is larger than model input size


        TODO: Seperate logic of each granularity to independent function
        TODO: for article and paragraph granularity, use other encoding method
        (Remember to modify retrieve as well)
        """
        title_embedding = self.encoder.get_sentence_encoding(article['title'])
        self.annoy_title.add_item(index, title_embedding)

        for granularity in self.article_manager.granularities:
            parsed_struct = self.article_manager.parse(
                article['content'], granularity)
            if granularity == 'article':
                article_embedding = self.encoder.get_article_encoding(
                    parsed_struct)
                self.annoy_article.add_item(index, article_embedding)
            elif granularity == 'paragraph':
                for i, paragraph in enumerate(parsed_struct):
                    paragraph_embedding = self.encoder.get_paragraph_encoding(
                        paragraph)
                    self.annoy_paragraph.add_item(
                        self.paragraph_id, paragraph_embedding)
                    self.paragraph2articleid[self.paragraph_id] = index
                    self.paragraph_id2structure[self.paragraph_id] = (i, )
                    self.paragraph_id += 1
            elif granularity == 'sentence':
                for i, paragraph in enumerate(parsed_struct):
                    for j, sentence in enumerate(paragraph):
                        sentence_embedding = self.encoder.get_sentence_encoding(
                            sentence)
                        self.annoy_sentence.add_item(
                            self.sentence_id, sentence_embedding)
                        self.sentence2articleid[self.sentence_id] = index
                        self.sentence_id2structure[self.sentence_id] = (i, j)
                        self.sentence_id += 1

    def build_index(self, tree_num: int = 10):
        self.annoy_title.build(tree_num)
        self.annoy_article.build(tree_num)
        self.annoy_paragraph.build(tree_num)
        self.annoy_sentence.build(tree_num)

    def save_index(self, annoy_dir: str = None):
        """
        TODO: Maybe save encoder model and metric in the json file as well?!
        """
        if not annoy_dir:
            annoy_dir = curr_dir

        self.annoy_title.save(os.path.join(
            annoy_dir, f'{self.encoder_model}_title.ann'))
        self.annoy_article.save(os.path.join(
            annoy_dir, f'{self.encoder_model}_article.ann'))
        self.annoy_paragraph.save(os.path.join(
            annoy_dir, f'{self.encoder_model}_paragraph.ann'))
        self.annoy_sentence.save(os.path.join(
            annoy_dir, f'{self.encoder_model}_sentence.ann'))

        with open(os.path.join(annoy_dir, f'mapping.json'), 'w') as fp:
            json.dump({
                'sentence_id': self.sentence_id,
                'paragraph_id': self.paragraph_id,
                'sentence2articleid': self.sentence2articleid,
                'paragraph2articleid': self.paragraph2articleid,
                'sentence_id2structure': self.sentence_id2structure,
                'paragraph_id2structure': self.paragraph_id2structure,
            }, fp)


if __name__ == "__main__":
    article_content = """今日，华人运通与微软在2020世界人工智能大会云端峰会（WAIC 2020）上宣布双方达成战略合作，依托微软小冰人工智能技术，共同在高合汽车上落地全球首个主动式人工智能伙伴HiPhiGo，致力于从智慧车机的前装设计阶段开始提供整体解决方案，为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。双方正在探讨成立联合智能计算实验室，以智能汽车为载体，在智捷交通等多个领域展开深度合作。通过人工智能等前瞻技术研发和应用，推动智慧出行和社会可持续发展。 华人运通董事长丁磊与微软（亚洲）互联网工程院院长王永东在“2020世界人工智能大会云端峰会”上共同宣布了双方的战略合作的相关内容。依托微软小冰人工智能技术，微软与华人运通的合作致力于从智慧车机的前装设计阶段开始提供整体解决方案，致力于为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。 王永东表示，人工智能在各领域的应用落地，离不开相关企业和科技公司的携手努力。微软在计算机语音、计算机视觉、自然语言处理、搜索引擎和知识图谱方面均有深厚的技术积累。例如在微软的语音合成领域（Text to speech），依托深度神经网络，可合成出自然而富有情感、足以媲美人类的声音，使用户与人工智能的交互流畅愉悦。微软希望每一项技术能力，都不是高堂上远的秀科技，而能落实为人人可亲自使用的实际产品。华人运通在设计、工程开发、智能系统等方面拥有丰富的经验，一直走在创新前列，在车路城一体化发展方面有着全面布局和成功实践。此次微软与华人运通的合作，使人工智能技术有了切实可行的落地场景，得以转化为真实有效的生产力，发挥更大的应用价值。微软与华人运通将携手推进人工智能等新兴科技在汽车智慧乃至智慧出行领域的广泛应用，为产业升级和社会可持续发展注入新的活力。 丁磊表示，华人运通从城市可持续发展的层面出发，提出“智能汽车、智捷交通、智慧城市”的战略，实现车更聪明，路更互联，城更智慧的人类未来出行愿景。此次合作是顶级人工智能企业和智能汽车公司的强强联手，是AI多项领先技术在全球汽车行业的首次量产落地，在世界范围内具有技术领先性。

    在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。 伴随智能科技与通信技术的革新，汽车正在向超级移动智能终端进化，成为人们智慧生活的重要载体。基于自主研发的开放式电子电气架构，华人运通打造了具备推理能力，能主动感知用户、帮助用户的主动式人工智能伙伴 HiPhiGo，并在高合汽车首款量产车上实现落地，树立智能汽车的全球新标杆。 从首款智能汽车高合HiPhi 有条不紊地推进，到全球首条车路协同自动驾驶智能化城市道路示范项目在盐城开通试运行，再到全球首个车路城一体化5G无人驾驶交通运营样板在上海张江未来公园成功落地，华人运通以人为本，从人性化需求出发，通过人性化智慧，打造“智能汽车、智捷交通、智慧城市“。目前，“三智”战略各项业务稳步推进。高合首款量产车HiPhi将于2020年底实现小批量试生产，2021年上市交付。 人工智能是21世纪技术变革的驱动力，也是产业变革、经济社会发展的驱动力。未来，微软将与华人运通开展更深入的合作，通过人工智能技术为用户带来更多创新体验，共同推动交通产业进步和出行方式进步，使每个人都能从人工智能技术的发展中获益。"""

    test_article = {
        'index': 0,
        'title': '华人运通与微软达成战略合作，高合汽车落地全球首个主动式人工智能伙伴HiPhiGo',
        'content': article_content
    }

    builder = AnnoyIndexBuilder()
    builder.add_index_for_article(test_article['index'], test_article)
    builder.build_index()
    builder.save_index()
    builder.load_index()
