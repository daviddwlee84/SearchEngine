from jieba import analyse
import jieba
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '..'))

from mining.tfidf import TFIDF


class KeywordExtractor(object):
    def __init__(self, idf_path: str = None,
                 user_dict_path: str = os.path.join(curr_dir, 'userdict.txt'),
                 default_method: str = 'jieba.extract_tags'):
        """
        Methods:

        tfidf: customized TFIDF
        jieba.textrank: jieba's textrank
        jieba.extract_tags: jieba's tfidf?!
        jieba.tfidf: jieba's tfidf
        """
        jieba.load_userdict(user_dict_path)

        self.default_method = default_method
        # TFIDF()

    def get_topk_keywords(self, text: str, topk: int, method: str = None):
        """
        TODO: maybe add a mix mode?!
        """
        if not method:
            method = self.default_method

        if method == 'jieba.textrank':
            result = analyse.textrank(text, topK=topk)
        elif method == 'jieba.extract_tags':
            result = analyse.extract_tags(text, topK=topk)
        elif method == 'jieba.tfidf':
            result = analyse.tfidf(text, topK=topk)

        return result


if __name__ == "__main__":
    KeywordExtractor()
