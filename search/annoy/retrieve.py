from typing import Dict, List, Tuple
from annoy import AnnoyIndex
import os
import json

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '../..'))

from search.annoy.representation import Encoder
from utils.article_loader import ArticleManager


class AnnoyRetrieve(object):
    """
    Build index for different granularities, objects

    1. Title
    2. Content (entire article)
    3. Paragraph
    4. Sentence


    TODO (important): Index Back To Objects!!!! (currently only return index)
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

        self.paragraph2articleid = {}
        self.sentence2articleid = {}

    def load_index(self, annoy_dir: str = None):
        """
        To continuous build index from last checkpoint use this function
        (not sure if it's possible...)
        """
        if not annoy_dir:
            annoy_dir = curr_dir

        self.annoy_title.load(os.path.join(
            annoy_dir, f'{self.encoder_model}_title.ann'))
        self.annoy_article.load(os.path.join(
            annoy_dir, f'{self.encoder_model}_article.ann'))
        self.annoy_paragraph.load(os.path.join(
            annoy_dir, f'{self.encoder_model}_paragraph.ann'))
        self.annoy_sentence.load(os.path.join(
            annoy_dir, f'{self.encoder_model}_sentence.ann'))

        with open(os.path.join(annoy_dir, f'mapping.json'), 'r') as fp:
            data = json.load(fp)
            # note that json need to store key in "string"
            self.sentence2articleid = data['sentence2articleid']
            self.paragraph2articleid = data['paragraph2articleid']

    # ===== Query and Retrieve Index and Score ===== #

    def _retrieve_title(self, title: str, topk: int = 10) -> List[Tuple[int, float]]:
        query_embedding = self.encoder.get_sentence_encoding(title)
        matches, distances = self.annoy_title.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[1])
        return match_result

    def _retrieve_article(self, article: str, topk: int = 10) -> List[Tuple[int, float]]:
        query_embedding = self.encoder.get_article_encoding(article)
        matches, distances = self.annoy_article.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[1])
        return match_result

    def _retrieve_paragraph(self, paragraph: str, topk: int = 10) -> List[Tuple[int, int, float]]:
        query_embedding = self.encoder.get_paragraph_encoding(paragraph)
        matches, distances = self.annoy_paragraph.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, self.paragraph2articleid.get(str(match)), distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[-1])
        return match_result

    def _retrieve_sentence(self, sentence: str, topk: int = 10) -> List[Tuple[int, int, float]]:
        query_embedding = self.encoder.get_sentence_encoding(sentence)
        matches, distances = self.annoy_sentence.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, self.sentence2articleid.get(str(match)), distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[-1])
        return match_result

    # ===== (TODO) Query and Retrieve OBJECT and Score ===== #


test_article = """今日，华人运通与微软在2020世界人工智能大会云端峰会（WAIC 2020）上宣布双方达成战略合作，依托微软小冰人工智能技术，共同在高合汽车上落地全球首个主动式人工智能伙伴HiPhiGo，致力于从智慧车机的前装设计阶段开始提供整体解决方案，为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。双方正在探讨成立联合智能计算实验室，以智能汽车为载体，在智捷交通等多个领域展开深度合作。通过人工智能等前瞻技术研发和应用，推动智慧出行和社会可持续发展。 华人运通董事长丁磊与微软（亚洲）互联网工程院院长王永东在“2020世界人工智能大会云端峰会”上共同宣布了双方的战略合作的相关内容。依托微软小冰人工智能技术，微软与华人运通的合作致力于从智慧车机的前装设计阶段开始提供整体解决方案，致力于为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。 王永东表示，人工智能在各领域的应用落地，离不开相关企业和科技公司的携手努力。微软在计算机语音、计算机视觉、自然语言处理、搜索引擎和知识图谱方面均有深厚的技术积累。例如在微软的语音合成领域（Text to speech），依托深度神经网络，可合成出自然而富有情感、足以媲美人类的声音，使用户与人工智能的交互流畅愉悦。微软希望每一项技术能力，都不是高堂上远的秀科技，而能落实为人人可亲自使用的实际产品。华人运通在设计、工程开发、智能系统等方面拥有丰富的经验，一直走在创新前列，在车路城一体化发展方面有着全面布局和成功实践。此次微软与华人运通的合作，使人工智能技术有了切实可行的落地场景，得以转化为真实有效的生产力，发挥更大的应用价值。微软与华人运通将携手推进人工智能等新兴科技在汽车智慧乃至智慧出行领域的广泛应用，为产业升级和社会可持续发展注入新的活力。 丁磊表示，华人运通从城市可持续发展的层面出发，提出“智能汽车、智捷交通、智慧城市”的战略，实现车更聪明，路更互联，城更智慧的人类未来出行愿景。此次合作是顶级人工智能企业和智能汽车公司的强强联手，是AI多项领先技术在全球汽车行业的首次量产落地，在世界范围内具有技术领先性。

在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。 伴随智能科技与通信技术的革新，汽车正在向超级移动智能终端进化，成为人们智慧生活的重要载体。基于自主研发的开放式电子电气架构，华人运通打造了具备推理能力，能主动感知用户、帮助用户的主动式人工智能伙伴 HiPhiGo，并在高合汽车首款量产车上实现落地，树立智能汽车的全球新标杆。 从首款智能汽车高合HiPhi 有条不紊地推进，到全球首条车路协同自动驾驶智能化城市道路示范项目在盐城开通试运行，再到全球首个车路城一体化5G无人驾驶交通运营样板在上海张江未来公园成功落地，华人运通以人为本，从人性化需求出发，通过人性化智慧，打造“智能汽车、智捷交通、智慧城市“。目前，“三智”战略各项业务稳步推进。高合首款量产车HiPhi将于2020年底实现小批量试生产，2021年上市交付。 人工智能是21世纪技术变革的驱动力，也是产业变革、经济社会发展的驱动力。未来，微软将与华人运通开展更深入的合作，通过人工智能技术为用户带来更多创新体验，共同推动交通产业进步和出行方式进步，使每个人都能从人工智能技术的发展中获益。"""

test_paragraph = "今日，华人运通与微软在2020世界人工智能大会云端峰会（WAIC 2020）上宣布双方达成战略合作，依托微软小冰人工智能技术，共同在高合汽车上落地全球首个主动式人工智能伙伴HiPhiGo，致力于从智慧车机的前装设计阶段开始提供整体解决方案，为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。双方正在探讨成立联合智能计算实验室，以智能汽车为载体，在智捷交通等多个领域展开深度合作。通过人工智能等前瞻技术研发和应用，推动智慧出行和社会可持续发展。 华人运通董事长丁磊与微软（亚洲）互联网工程院院长王永东在“2020世界人工智能大会云端峰会”上共同宣布了双方的战略合作的相关内容。依托微软小冰人工智能技术，微软与华人运通的合作致力于从智慧车机的前装设计阶段开始提供整体解决方案，致力于为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。 王永东表示，人工智能在各领域的应用落地，离不开相关企业和科技公司的携手努力。微软在计算机语音、计算机视觉、自然语言处理、搜索引擎和知识图谱方面均有深厚的技术积累。例如在微软的语音合成领域（Text to speech），依托深度神经网络，可合成出自然而富有情感、足以媲美人类的声音，使用户与人工智能的交互流畅愉悦。微软希望每一项技术能力，都不是高堂上远的秀科技，而能落实为人人可亲自使用的实际产品。华人运通在设计、工程开发、智能系统等方面拥有丰富的经验，一直走在创新前列，在车路城一体化发展方面有着全面布局和成功实践。此次微软与华人运通的合作，使人工智能技术有了切实可行的落地场景，得以转化为真实有效的生产力，发挥更大的应用价值。微软与华人运通将携手推进人工智能等新兴科技在汽车智慧乃至智慧出行领域的广泛应用，为产业升级和社会可持续发展注入新的活力。 丁磊表示，华人运通从城市可持续发展的层面出发，提出“智能汽车、智捷交通、智慧城市”的战略，实现车更聪明，路更互联，城更智慧的人类未来出行愿景。此次合作是顶级人工智能企业和智能汽车公司的强强联手，是AI多项领先技术在全球汽车行业的首次量产落地，在世界范围内具有技术领先性。"

if __name__ == "__main__":
    retrieve = AnnoyRetrieve()
    retrieve.load_index()

    print(retrieve.annoy_title.get_n_items(), 1)
    print(retrieve.annoy_article.get_n_items(), 1)
    print(retrieve.annoy_paragraph.get_n_items(), 2)
    print(retrieve.annoy_sentence.get_n_items(), 22)

    k = 10
    print(retrieve._retrieve_title('华人运通与微软达成战略合作', k))
    print(retrieve._retrieve_article(test_article, k))
    print(retrieve._retrieve_paragraph(test_paragraph, k))
    print(retrieve._retrieve_sentence(
        '在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。', k))
