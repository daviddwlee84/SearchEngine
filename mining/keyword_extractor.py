from mining.tfidf import TFIDF
from jieba import analyse


class KeywordExtractor(object):
    def __init__(self, idf_path: str = None, default_method: str = ''):
        """
        Methods:

        tfidf: customized TFIDF
        jieba.textrank: jieba's textrank
        jieba.extract_tags: jieba's tfidf?!
        jieba.tfidf: jieba's tfidf
        """
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

