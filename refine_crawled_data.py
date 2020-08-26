from mining.keyword_extractor import KeywordExtractor
from utils.data_loader import load_tsv
import pandas as pd
from tqdm import tqdm


class DataRefine(object):
    """
    This only need to execute once (deal with the "just crawled data")

    This will skip the processed data

    TODO: load from json?! (single json file combine all the results)
    """

    def __init__(self, tsv_data: str, verbose: bool = True):
        self.verbose = verbose
        if verbose:
            # https://stackoverflow.com/questions/18603270/progress-indicator-during-pandas-operations
            tqdm.pandas()

        self.ori_path = tsv_data
        self.data = load_tsv(tsv_data)
        self.columns = self.data.columns.copy()
        self.keyword_extractor = KeywordExtractor()

    def _extract_keyword(self, at_least: int = 3, topk: int = 20, threshold: float = 0.3,
                         keyword_cols=['title', 'content'],
                         use_metadata: bool = True, meta_col: str = 'meta') -> pd.Series:
        """
        TODO: maybe seperate "topk" and "topk attempt"?! (because we have threshold)

        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html (didn't use this)
        """
        use_metadata &= meta_col in self.columns

        def keywords_extraction(row):
            keywords = []

            # === meta data === #
            if use_metadata:
                # TODO: need modify the meta data structure (dict can't be store in pandas)
                pass

            # === keywords from given columns === #
            text = '。\n'.join(row[col] for col in keyword_cols)

            candidates = self.keyword_extractor.get_topk_keywords(
                text, topk=topk)

            for keyword, weight in candidates:
                if weight >= threshold or len(keywords) <= at_least:
                    keywords.append(keyword)

            # keywords.extend(
            #     [keyword for keyword, weight in candidates if weight >= threshold]
            # )

            # row['keyword'] = keywords

            return keywords

        if self.verbose:
            # https://stackoverflow.com/questions/18603270/progress-indicator-during-pandas-operations
            return self.data.progress_apply(keywords_extraction, axis='columns')
        else:
            return self.data.apply(keywords_extraction, axis='columns')

    def refine(self, force: bool = False):
        if force or 'keyword' not in columns:
            if self.verbose:
                print('Extracting keywords....')
            self.data['keyword'] = self._extract_keyword()

        return self.data.copy()

    def save(self, tsv_path: str = None):
        if not tsv_path:
            # override
            tsv_path = self.ori_path

        self.data.to_csv(tsv_path, sep='\t', index=False)


if __name__ == "__main__":
    refinement = DataRefine('data/all_news.tsv')
    result = refinement.refine(force=True)
    refinement.save('data/all_news_new.tsv')
    import ipdb
    ipdb.set_trace()
