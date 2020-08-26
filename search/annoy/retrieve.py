from typing import Dict, List, Tuple
from annoy import AnnoyIndex
import os
import json

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '../..'))

from search.annoy.representation import Encoder
from search.elastic_search.retrieve import ESAPIWrapper
from utils.article_loader import ArticleManager
from utils.data_loader import load_tsv, load_json


class AnnoyRetrieve(object):
    """
    Build index for different granularities, objects

    1. Title
    2. Content (entire article)
    3. Paragraph
    4. Sentence


    TODO (important): Index Back To Objects!!!! (currently only return index)
    """

    load_from = None

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
        self.paragraph_id2structure = {}
        self.sentence_id2structure = {}

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
            self.sentence_id2structure = data['sentence_id2structure']
            self.paragraph_id2structure = data['paragraph_id2structure']

    # ===== data management ===== #

    def load_reference_data(self, path_or_index: str, load_from: str = 'tsv'):
        """
        TODO: maybe support json as well
        """
        assert load_from in ['tsv', 'json', 'es']

        self.load_from = load_from

        if load_from == 'tsv':
            self.data = load_tsv(path_or_index)
        elif load_from == 'es':
            self.es = ESAPIWrapper(index=path_or_index)
        elif load_from == 'json':
            self.data = load_json(path_or_index, simplify=True,
                                  simplify_columns=['title', 'content'])

    def get_document_by_id(self, idx: int):
        assert self.load_from is not None, 'Please load data first.'

        if self.load_from == 'tsv':
            return dict(self.data.loc[idx])
        elif self.load_from == 'es':
            return self.es.get_idx(idx)
        elif self.load_from == 'json':
            # TODO: maybe we want to keep it json way (currently we load json as pandas Dataframe)
            return dict(self.data.loc[idx])

    # ===== Query and Retrieve Index and Score ===== #

    def _retrieve_title_ids(self, title: str, topk: int = 10) -> List[Tuple[int, float]]:
        query_embedding = self.encoder.get_sentence_encoding(title)
        matches, distances = self.annoy_title.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[1])
        return match_result

    def _retrieve_article_ids(self, article: str, topk: int = 10) -> List[Tuple[int, float]]:
        query_embedding = self.encoder.get_article_encoding(article)
        matches, distances = self.annoy_article.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[1])
        return match_result

    def _retrieve_paragraph_ids(self, paragraph: str, topk: int = 10) -> List[Tuple[int, float]]:
        query_embedding = self.encoder.get_paragraph_encoding(paragraph)
        matches, distances = self.annoy_paragraph.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[-1])
        return match_result

    def _retrieve_sentence_ids(self, sentence: str, topk: int = 10) -> List[Tuple[int, float]]:
        query_embedding = self.encoder.get_sentence_encoding(sentence)
        matches, distances = self.annoy_sentence.get_nns_by_vector(
            query_embedding, topk, include_distances=True)
        match_result = [(match, distance)
                        for match, distance in zip(matches, distances)]
        match_result.sort(key=lambda x: x[-1])
        return match_result

    # ===== Query and Retrieve OBJECT and Score ===== #

    def search_title(self, title: str, topk: int = 10, include_ori_doc: bool = False) -> List[Tuple[Dict[str, str], float]]:
        match_result = self._retrieve_title_ids(title, topk)
        doc_result = []
        for article_id, score in match_result:
            original_doc_dict = self.get_document_by_id(article_id)
            title = original_doc_dict['title']
            if include_ori_doc:
                doc_result.append((original_doc_dict, title, score))
            else:
                doc_result.append((title, score))
        return doc_result

    def search_article(self, article: str, topk: int = 10, include_ori_doc: bool = False) -> List[Tuple[Dict[str, str], float]]:
        match_result = self._retrieve_article_ids(article, topk)
        doc_result = []
        for article_id, score in match_result:
            original_doc_dict = self.get_document_by_id(article_id)
            article = original_doc_dict['content']
            if include_ori_doc:
                doc_result.append((original_doc_dict, article, score))
            else:
                doc_result.append((article, score))
        return doc_result

    def search_paragraph(self, paragraph: str, topk: int = 10, include_ori_doc: bool = False) -> List[Tuple[Dict[str, str], float]]:
        match_result = self._retrieve_paragraph_ids(paragraph, topk)
        doc_result = []
        for para_id, score in match_result:
            article_id = self.paragraph2articleid.get(str(para_id))
            i, = self.paragraph_id2structure.get(str(para_id))
            original_doc_dict = self.get_document_by_id(article_id)
            paragraph = self.article_manager.parse(
                original_doc_dict['content'], 'paragraph')[i]
            if include_ori_doc:
                doc_result.append((original_doc_dict, paragraph, score))
            else:
                doc_result.append((paragraph, score))
        return doc_result

    def search_sentence(self, sentence: str, topk: int = 10, include_ori_doc: bool = False) -> List[Tuple[Dict[str, str], float]]:
        match_result = self._retrieve_sentence_ids(sentence, topk)
        doc_result = []
        for sent_id, score in match_result:
            article_id = self.sentence2articleid.get(str(sent_id))
            i, j = self.sentence_id2structure.get(str(sent_id))
            original_doc_dict = self.get_document_by_id(article_id)
            sentence = self.article_manager.parse(
                original_doc_dict['content'], 'sentence')[i][j]
            if include_ori_doc:
                doc_result.append((original_doc_dict, sentence, score))
            else:
                doc_result.append((sentence, score))
        return doc_result

    def search_paragraph_with_sentence(self, sentence: str, topk: int = 10, include_ori_doc: bool = False,
                                       remove_duplicate: bool = True, score_average: bool = False):
        """
        Retrieve the paragraph where the sentence located
        """
        match_result = self._retrieve_sentence_ids(sentence, topk)
        doc_result = []
        for sent_id, score in match_result:
            article_id = self.sentence2articleid.get(str(sent_id))
            i, _ = self.sentence_id2structure.get(str(sent_id))
            original_doc_dict = self.get_document_by_id(article_id)
            paragraph = self.article_manager.parse(
                original_doc_dict['content'], 'paragraph')[i]
            if include_ori_doc:
                doc_result.append((original_doc_dict, paragraph, score))
            else:
                doc_result.append((paragraph, score))

        # paragraph: [original_doc_dict, score1, score2, ...]
        para_score_dict = {}
        if remove_duplicate:
            # TODO: this can be done with just compare paragraph id from the beginning
            for result in doc_result:
                paragraph = result[-2]
                score = result[-1]
                if paragraph not in para_score_dict:
                    # first one
                    if len(result) == 3:
                        para_score_dict[paragraph] = [result[0], score]
                    else:
                        para_score_dict[paragraph] = [None, score]
                else:
                    para_score_dict[paragraph].append(score)

            doc_result = []
            for paragraph, value in para_score_dict.items():
                original_doc_dict = value[0]
                scores = value[1:]
                if score_average:
                    avg_score = sum(scores) / len(scores)
                else:
                    avg_score = sum(scores)
                if include_ori_doc:
                    doc_result.append(
                        (original_doc_dict, paragraph, avg_score))
                else:
                    doc_result.append((paragraph, avg_score))
            doc_result.sort(key=lambda x: x[-1])

        return doc_result


def _test_retrieve_ids():
    test_article = """今日，华人运通与微软在2020世界人工智能大会云端峰会（WAIC 2020）上宣布双方达成战略合作，依托微软小冰人工智能技术，共同在高合汽车上落地全球首个主动式人工智能伙伴HiPhiGo，致力于从智慧车机的前装设计阶段开始提供整体解决方案，为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。双方正在探讨成立联合智能计算实验室，以智能汽车为载体，在智捷交通等多个领域展开深度合作。通过人工智能等前瞻技术研发和应用，推动智慧出行和社会可持续发展。 华人运通董事长丁磊与微软（亚洲）互联网工程院院长王永东在“2020世界人工智能大会云端峰会”上共同宣布了双方的战略合作的相关内容。依托微软小冰人工智能技术，微软与华人运通的合作致力于从智慧车机的前装设计阶段开始提供整体解决方案，致力于为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。 王永东表示，人工智能在各领域的应用落地，离不开相关企业和科技公司的携手努力。微软在计算机语音、计算机视觉、自然语言处理、搜索引擎和知识图谱方面均有深厚的技术积累。例如在微软的语音合成领域（Text to speech），依托深度神经网络，可合成出自然而富有情感、足以媲美人类的声音，使用户与人工智能的交互流畅愉悦。微软希望每一项技术能力，都不是高堂上远的秀科技，而能落实为人人可亲自使用的实际产品。华人运通在设计、工程开发、智能系统等方面拥有丰富的经验，一直走在创新前列，在车路城一体化发展方面有着全面布局和成功实践。此次微软与华人运通的合作，使人工智能技术有了切实可行的落地场景，得以转化为真实有效的生产力，发挥更大的应用价值。微软与华人运通将携手推进人工智能等新兴科技在汽车智慧乃至智慧出行领域的广泛应用，为产业升级和社会可持续发展注入新的活力。 丁磊表示，华人运通从城市可持续发展的层面出发，提出“智能汽车、智捷交通、智慧城市”的战略，实现车更聪明，路更互联，城更智慧的人类未来出行愿景。此次合作是顶级人工智能企业和智能汽车公司的强强联手，是AI多项领先技术在全球汽车行业的首次量产落地，在世界范围内具有技术领先性。

    在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。 伴随智能科技与通信技术的革新，汽车正在向超级移动智能终端进化，成为人们智慧生活的重要载体。基于自主研发的开放式电子电气架构，华人运通打造了具备推理能力，能主动感知用户、帮助用户的主动式人工智能伙伴 HiPhiGo，并在高合汽车首款量产车上实现落地，树立智能汽车的全球新标杆。 从首款智能汽车高合HiPhi 有条不紊地推进，到全球首条车路协同自动驾驶智能化城市道路示范项目在盐城开通试运行，再到全球首个车路城一体化5G无人驾驶交通运营样板在上海张江未来公园成功落地，华人运通以人为本，从人性化需求出发，通过人性化智慧，打造“智能汽车、智捷交通、智慧城市“。目前，“三智”战略各项业务稳步推进。高合首款量产车HiPhi将于2020年底实现小批量试生产，2021年上市交付。 人工智能是21世纪技术变革的驱动力，也是产业变革、经济社会发展的驱动力。未来，微软将与华人运通开展更深入的合作，通过人工智能技术为用户带来更多创新体验，共同推动交通产业进步和出行方式进步，使每个人都能从人工智能技术的发展中获益。"""

    test_paragraph = "今日，华人运通与微软在2020世界人工智能大会云端峰会（WAIC 2020）上宣布双方达成战略合作，依托微软小冰人工智能技术，共同在高合汽车上落地全球首个主动式人工智能伙伴HiPhiGo，致力于从智慧车机的前装设计阶段开始提供整体解决方案，为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。双方正在探讨成立联合智能计算实验室，以智能汽车为载体，在智捷交通等多个领域展开深度合作。通过人工智能等前瞻技术研发和应用，推动智慧出行和社会可持续发展。 华人运通董事长丁磊与微软（亚洲）互联网工程院院长王永东在“2020世界人工智能大会云端峰会”上共同宣布了双方的战略合作的相关内容。依托微软小冰人工智能技术，微软与华人运通的合作致力于从智慧车机的前装设计阶段开始提供整体解决方案，致力于为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。 王永东表示，人工智能在各领域的应用落地，离不开相关企业和科技公司的携手努力。微软在计算机语音、计算机视觉、自然语言处理、搜索引擎和知识图谱方面均有深厚的技术积累。例如在微软的语音合成领域（Text to speech），依托深度神经网络，可合成出自然而富有情感、足以媲美人类的声音，使用户与人工智能的交互流畅愉悦。微软希望每一项技术能力，都不是高堂上远的秀科技，而能落实为人人可亲自使用的实际产品。华人运通在设计、工程开发、智能系统等方面拥有丰富的经验，一直走在创新前列，在车路城一体化发展方面有着全面布局和成功实践。此次微软与华人运通的合作，使人工智能技术有了切实可行的落地场景，得以转化为真实有效的生产力，发挥更大的应用价值。微软与华人运通将携手推进人工智能等新兴科技在汽车智慧乃至智慧出行领域的广泛应用，为产业升级和社会可持续发展注入新的活力。 丁磊表示，华人运通从城市可持续发展的层面出发，提出“智能汽车、智捷交通、智慧城市”的战略，实现车更聪明，路更互联，城更智慧的人类未来出行愿景。此次合作是顶级人工智能企业和智能汽车公司的强强联手，是AI多项领先技术在全球汽车行业的首次量产落地，在世界范围内具有技术领先性。"

    retrieve = AnnoyRetrieve()
    retrieve.load_index()

    print(retrieve.annoy_title.get_n_items(), 1)
    print(retrieve.annoy_article.get_n_items(), 1)
    print(retrieve.annoy_paragraph.get_n_items(), 2)
    print(retrieve.annoy_sentence.get_n_items(), 22)

    k = 10
    print(retrieve._retrieve_title_ids('华人运通与微软达成战略合作', k))
    print(retrieve._retrieve_article_ids(test_article, k))
    print(retrieve._retrieve_paragraph_ids(test_paragraph, k))
    print(retrieve._retrieve_sentence_ids(
        '在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。', k))


def _test_crawled_data(load_from: str):
    """
    Make sure execute ../../build_index.py first
    """
    retrieve = AnnoyRetrieve()
    retrieve.load_index(os.path.join(curr_dir, '../../index'))
    if load_from == 'tsv':
        retrieve.load_reference_data(os.path.join(
            curr_dir, '../../data/all_news_new.tsv'), 'tsv')
    elif load_from == 'es':
        retrieve.load_reference_data('news', 'es')

    test_article = """报道称，作为TikTok美国员工的代表，技术项目经理帕特里克·瑞安告诉《国会山报》，这起诉讼将聚焦宪法规定的正当程序权。瑞安坚称，是否允许该企业在美国运营，并不是总统一时兴起就可以决定的。瑞安补充说，当特朗普的禁令下个月生效时，约有1500名TikTok及其母公司字节跳动的员工面临着拿不到工资的风险。
报道提到，瑞安在众筹平台发起了一项筹款活动，用以聘请律师向美国政府发起挑战。瑞安在筹款界面上写道：“请帮助TikTok的员工为保住我们的薪水而战”。截至目前，筹款金额已经超过1.3万美元。
《国会山报》称，黑石法律集团(Blackstone Law Group)和著名互联网维权律师迈克·戈德温将代表TikTok的美国员工提起诉讼。他们预计于本周晚些时候向联邦法院提起诉讼。律师们表示，他们正在考虑在纽约南区、北加州或华盛顿特区提起诉讼。
连日来，美国政府不断向TikTok施压。
特朗普当地时间8月6日签署行政令，称移动应用程序抖音海外版（TikTok）和微信对美国国家安全构成威胁，将在45天后禁止任何美国个人或实体与抖音海外版(TikTok)、微信及其中国母公司进行任何交易。
特朗普当地时间8月14日签署另一行政令，要求字节跳动在90天内剥离任何使TikTok能够在美国运营的有形和无形资产，并拿出已经用烂了的理由给字节跳动2017年收购美国视频应用Musical.ly定性——存在“危害国家安全”风险。
中国已多次就TikTok问题表明立场。中国外交部发言人赵立坚8月17日在例行记者会上称，TikTok几乎满足了美方提出的所有要求，但仍逃不过美国一些人出于强盗逻辑和政治私利对其采取的巧取豪夺。美国一些政客非要无中生有、罗织罪名，置TikTok于死地。赵立坚称，这种霸凌行径是对美方一贯标榜的市场经济和公平竞争原则的公然否定，违反国际贸易规则，肆意侵害他国利益，也必将损害美国自身利益。我们敦促美方立即纠正错误，停止诬蔑抹黑中国，停止无理打压别国企业。
"""

    print(retrieve.search_title('Tiktok美国'))
    # print(retrieve.search_article(test_article))
    # print(retrieve.search_paragraph(
    #     '8月17日，广东佛山顺德区杏坛镇一名老人被一只狗身上的牵引绳绊倒在地，经送医抢救无效去世，此事件经曝光后引发热议。8月18日晚，广东佛山市顺德区杏坛镇政府进行情况通报，初步判断该事件为意外事件。这一判断或许出乎很多人的意料。'))
    print(retrieve.search_sentence('承担法律责任，付出一定的侵权代价'))


def _gen_test_json(test_file: str = os.path.join(curr_dir, 'test.json')):
    from datetime import datetime
    data = {
        'title': '华人运通与微软达成战略合作，高合汽车落地全球首个主动式人工智能伙伴HiPhiGo',
        'date': str(datetime.now()),
        'content': """今日，华人运通与微软在2020世界人工智能大会云端峰会（WAIC 2020）上宣布双方达成战略合作，依托微软小冰人工智能技术，共同在高合汽车上落地全球首个主动式人工智能伙伴HiPhiGo，致力于从智慧车机的前装设计阶段开始提供整体解决方案，为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。双方正在探讨成立联合智能计算实验室，以智能汽车为载体，在智捷交通等多个领域展开深度合作。通过人工智能等前瞻技术研发和应用，推动智慧出行和社会可持续发展。 华人运通董事长丁磊与微软（亚洲）互联网工程院院长王永东在“2020世界人工智能大会云端峰会”上共同宣布了双方的战略合作的相关内容。依托微软小冰人工智能技术，微软与华人运通的合作致力于从智慧车机的前装设计阶段开始提供整体解决方案，致力于为用户提供更好的交通出行体验，促进人工智能与交通行业的创新融合发展。 王永东表示，人工智能在各领域的应用落地，离不开相关企业和科技公司的携手努力。微软在计算机语音、计算机视觉、自然语言处理、搜索引擎和知识图谱方面均有深厚的技术积累。例如在微软的语音合成领域（Text to speech），依托深度神经网络，可合成出自然而富有情感、足以媲美人类的声音，使用户与人工智能的交互流畅愉悦。微软希望每一项技术能力，都不是高堂上远的秀科技，而能落实为人人可亲自使用的实际产品。华人运通在设计、工程开发、智能系统等方面拥有丰富的经验，一直走在创新前列，在车路城一体化发展方面有着全面布局和成功实践。此次微软与华人运通的合作，使人工智能技术有了切实可行的落地场景，得以转化为真实有效的生产力，发挥更大的应用价值。微软与华人运通将携手推进人工智能等新兴科技在汽车智慧乃至智慧出行领域的广泛应用，为产业升级和社会可持续发展注入新的活力。 丁磊表示，华人运通从城市可持续发展的层面出发，提出“智能汽车、智捷交通、智慧城市”的战略，实现车更聪明，路更互联，城更智慧的人类未来出行愿景。此次合作是顶级人工智能企业和智能汽车公司的强强联手，是AI多项领先技术在全球汽车行业的首次量产落地，在世界范围内具有技术领先性。

    在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。 伴随智能科技与通信技术的革新，汽车正在向超级移动智能终端进化，成为人们智慧生活的重要载体。基于自主研发的开放式电子电气架构，华人运通打造了具备推理能力，能主动感知用户、帮助用户的主动式人工智能伙伴 HiPhiGo，并在高合汽车首款量产车上实现落地，树立智能汽车的全球新标杆。 从首款智能汽车高合HiPhi 有条不紊地推进，到全球首条车路协同自动驾驶智能化城市道路示范项目在盐城开通试运行，再到全球首个车路城一体化5G无人驾驶交通运营样板在上海张江未来公园成功落地，华人运通以人为本，从人性化需求出发，通过人性化智慧，打造“智能汽车、智捷交通、智慧城市“。目前，“三智”战略各项业务稳步推进。高合首款量产车HiPhi将于2020年底实现小批量试生产，2021年上市交付。 人工智能是21世纪技术变革的驱动力，也是产业变革、经济社会发展的驱动力。未来，微软将与华人运通开展更深入的合作，通过人工智能技术为用户带来更多创新体验，共同推动交通产业进步和出行方式进步，使每个人都能从人工智能技术的发展中获益。"""
    }
    with open(test_file, 'w', encoding='utf8') as fp:
        json.dump(data, fp, ensure_ascii=False)
        fp.write('\n')


def _test_get_para_by_sent():
    retrieve = AnnoyRetrieve()
    retrieve.load_index()
    _gen_test_json()
    retrieve.load_reference_data(os.path.join(curr_dir, 'test.json'), 'json')
    print(retrieve.search_paragraph_with_sentence(
        '在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。', remove_duplicate=False))
    print(retrieve.search_paragraph_with_sentence(
        '在2020世界人工智能大会云端峰会上，王永东与丁磊就“如何以人工智能助力车路城一体化发展”进行了精彩的对话。', remove_duplicate=True))


if __name__ == "__main__":
    # _test_retrieve_ids()
    # _test_crawled_data('es')
    # _test_crawled_data('tsv')
    _test_get_para_by_sent()
