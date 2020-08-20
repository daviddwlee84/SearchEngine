from typing import List


class TFIDF(object):
    def __init__(self, idf_path: str):
        pass

    def update_idf_with_documents(self):
        pass

    def get_topk_keywords(self, text: str, topk: int) -> List[str]:
        pass

    def get_keywords_with_threshold(self, text: str, threshold: float) -> List[str]:
        pass
