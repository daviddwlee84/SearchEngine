import pandas as pd

default_data_type = {
    # 'url': 'str',
    # 'domain': 'str',
    # 'html_title': 'str',
    # 'html_body': 'str',
    # 'title': 'str',
    # 'author': 'str',
    'date': 'datetime64[ns]',
    # 'content': 'str',
    'parse_date': 'datetime64[ns]',
    # 'meta': 'object',  # there is some problem of storing dict in pandas
}


def load_tsv(tsv_path: str):
    """
    Load tsv file and recover its data type (especially the datetime)

    For more detail, checkout tools/Crawler/crawler/manager/combine_results
    """
    data = pd.read_csv(tsv_path, sep='\t')
    data_type = {key: value
                 for key, value in default_data_type.items()
                 if key in data.columns.to_list()}
    return data.astype(data_type)
