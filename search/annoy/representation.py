import torch
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
import timeit


class BertSentenceEncoder:
    def __init__(self, bert_model: str, device: str,
                 mode: str = 'MEAN', batch_size: int = 32, max_sent_length: int = 512):
        """
        :param bert_model: bert-based-uncased or bert-base-chinese
        """
        assert mode in ['CLS', 'MEAN']

        self.device = device
        self.mode = mode
        self.batch_size = batch_size
        self.max_sent_length = max_sent_length

        self.tokenizer = BertTokenizer.from_pretrained(bert_model)
        self.model = BertModel.from_pretrained(bert_model)

    def encode(self, sent, convert_to_type: str = 'numpy'):
        """
        :param sent:  senttence or  list of sentence
        :param device:
        :param mode: CLS or MEAN
        :return:
        """
        assert convert_to_type in ['', 'numpy', 'list', 'torch']

        if isinstance(sent, str):
            tokens_tensor = torch.tensor(self.tokenizer.encode(
                sent, truncation=True, max_length=self.max_sent_length, add_special_tokens=True)).unsqueeze(0)

            if self.device == 'cuda':
                tokens_tensor = tokens_tensor.to('cuda')
                self.model.to('cuda')

            ouputs = self.model(tokens_tensor)

            if self.mode == 'CLS':
                embedding = ouputs[0][0][0]
            else:
                embedding = torch.mean(ouputs[0][0], dim=0)

            if convert_to_type == 'list':
                return embedding.cpu().detach().tolist()
            elif convert_to_type == 'numpy':
                return embedding.cpu().detach().numpy()

            return embedding.cpu().detach()

        elif isinstance(sent, list):
            # TODO: CLS model?!

            start = 0
            embeddings = []
            for start in range(0, len(sent), self.batch_size):
                end = start + self.batch_size
                batch = sent[start:end]
                start = end
                max_length = max(len(self.tokenizer.encode(
                    s, truncation=True, max_length=self.max_sent_length, add_special_tokens=True)) for s in batch)
                tokens_tensor = torch.tensor([self.tokenizer.encode(
                    s, max_length=max_length, add_special_tokens=True, pad_to_max_length=max_length) for s in batch])

                if self.device == 'cuda':
                    tokens_tensor = tokens_tensor.to('cuda')
                    self.model.to('cuda')

                ouputs = self.model(tokens_tensor)
                embedding = torch.mean(ouputs[0], dim=1)

                if convert_to_type == 'list':
                    embeddings.extend(embedding.cpu().detach().tolist())
                elif convert_to_type == 'numpy':
                    # Consider if transfom entire object
                    # embeddings.extend(
                    #     [embedding[i, :].cpu().detach().numpy()
                    #      for i in range(embedding.shape[0])]
                    # )
                    embeddings = embedding.cpu().detach().numpy()
                else:
                    # https://discuss.pytorch.org/t/should-it-really-be-necessary-to-do-var-detach-cpu-numpy/35489/5
                    # embeddings.extend(
                    #     [embedding[i, :].cpu().detach()
                    #      for i in range(embedding.shape[0])]
                    # )
                    embeddings = embedding.cpu().detach()

            return embeddings


def get_encoder(model: str = 'bert'):
    """
    1. BERT
    shape: 768

    2. Sentence Transformer
    shape: 512
    Note that, if input single sentence (not list), it will also return a 2D array e.g. shape = (1, 512)
    """
    # https://stackoverflow.com/questions/48152674/how-to-check-if-pytorch-is-using-the-gpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if model == 'bert':
        return BertSentenceEncoder(bert_model='bert-base-chinese', device=device)
    else:  # 'sent-transformer'
        # https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/SentenceTransformer.py
        return SentenceTransformer('distiluse-base-multilingual-cased', device=device)


class Encoder(object):
    """
    TODO: maybe return emb_dim when creating the object
    https://stackoverflow.com/questions/2491819/how-to-return-a-value-from-init-in-python
    use __new__()
    """
    def __init__(self, encoder_model: str = 'bert', data_type: str = 'numpy'):
        assert encoder_model in ['bert', 'sent-transformer']

        self.data_type = data_type  # TODO: unused yet (but this is default)

        self.encoder_model = encoder_model
        self.encoder = get_encoder(model=encoder_model)

    def _average_sent_encoding(self, string: str):
        """
        TODO: mean sentence encoding
        """
        return self.get_sentence_encoding(string)

    def _extractive_summarization_encoding(self, string: str):
        """
        TODO: encode TextRank sentences
        """
        return self.get_sentence_encoding(string)

    def get_sentence_encoding(self, sentence: str):
        return self.encoder.encode(sentence)

    # ===== High level wrapper ===== #

    def get_article_encoding(self, article: str):
        """
        TODO: finish _extractive_summarization_encoding
        """
        return self._extractive_summarization_encoding(article)

    def get_paragraph_encoding(self, paragraph: str):
        """
        TODO: finish _average_sent_encoding
        """
        return self._average_sent_encoding(paragraph)

    # ===== Even higher level wrapper ===== #

    def get_encoding_by_granularity(self, string: str, granularity: str = 'sentence'):
        """
        Just a wrapper
        """
        if granularity == 'sentence':
            return self.get_sentence_encoding(string)
        elif granularity == 'paragraph':
            return self.get_paragraph_encoding(string)
        elif granularity == 'article':
            return self.get_article_encoding(string)

        assert False, 'Not a valid granularity'


def _test_different_types():
    for string in ['測試一下', ['測試一下', '測個']]:
        for type_str in ['list', 'numpy', 'torch']:
            print(string, type_str)
            print('bert')
            encoder = get_encoder('bert')
            start = timeit.default_timer()
            result = encoder.encode(string, convert_to_type=type_str)
            end = timeit.default_timer()
            print(end - start, result)

            print('sent-transformer')
            encoder = get_encoder('sent-transformer')
            start = timeit.default_timer()
            if type_str == 'numpy':
                result = encoder.encode(string, convert_to_numpy=True)
            elif type_str == 'torch':
                result = encoder.encode(string, convert_to_tensor=True)
            end = timeit.default_timer()
            print(end - start, result)


if __name__ == "__main__":
    _test_different_types()
