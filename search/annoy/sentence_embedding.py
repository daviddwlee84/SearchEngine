import torch
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer


class BertSentenceEncoder:
    def __init__(self, bert_model: str, device: str, convert_to_type: str = ''):
        """
        :param bert_model: bert-based-uncased or bert-base-chinese
        """
        self.device = device
        self.convert_to_type = convert_to_type

        self.tokenizer = BertTokenizer.from_pretrained(bert_model)
        self.model = BertModel.from_pretrained(bert_model)

    def encode(self, sent, mode: str = 'MEAN', batch_size: int = 32, max_sent_length: int = 512):
        """
        :param sent:  senttence or  list of sentence
        :param device:
        :param mode: CLS or MEAN
        :return:
        """
        if isinstance(sent, str):
            tokens_tensor = torch.tensor(self.tokenizer.encode(
                sent, truncation=True, max_length=max_sent_length, add_special_tokens=True)).unsqueeze(0)

            if self.device == 'cuda':
                tokens_tensor = tokens_tensor.to('cuda')
                self.model.to('cuda')

            ouputs = self.model(tokens_tensor)

            if mode == 'CLS':
                embedding = ouputs[0][0][0]
            else:
                embedding = torch.mean(ouputs[0][0], dim=0)

            if self.convert_to_type == 'list':
                return embedding.cpu().detach().tolist()
            elif self.convert_to_type == 'numpy':
                return embedding.cpu().detach().numpy()

            return embedding.cpu().detach()

        elif isinstance(sent, list):
            start = 0
            embeddings = []
            for start in range(0, len(sent), batch_size):
                end = start + batch_size
                batch = sent[start:end]
                start = end
                max_length = max(len(self.tokenizer.encode(
                    s, truncation=True, max_length=max_sent_length, add_special_tokens=True)) for s in batch)
                tokens_tensor = torch.tensor([self.tokenizer.encode(
                    s, max_length=max_length, add_special_tokens=True, pad_to_max_length=max_length) for s in batch])

                if self.device == 'cuda':
                    tokens_tensor = tokens_tensor.to('cuda')
                    self.model.to('cuda')

                ouputs = self.model(tokens_tensor)
                embedding = torch.mean(ouputs[0], dim=1)

                if self.convert_to_type == 'list':
                    embeddings.extend(embedding.cpu().detach().tolist())
                elif self.convert_to_type == 'numpy':
                    # Consider if transfom entire object
                    embeddings.extend(
                        [embedding[i, :].cpu().detach().numpy()
                         for i in range(embedding.shape[0])]
                    )
                else:
                    # https://discuss.pytorch.org/t/should-it-really-be-necessary-to-do-var-detach-cpu-numpy/35489/5
                    embeddings.extend(
                        [embedding[i, :].cpu().detach()
                         for i in range(embedding.shape[0])]
                    )

            return embeddings


def get_encoder(model: str = 'bert', to_type: str = 'numpy'):
    """
    to_type only works for "bert" now
    """
    # https://stackoverflow.com/questions/48152674/how-to-check-if-pytorch-is-using-the-gpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if model == 'bert':
        return BertSentenceEncoder(bert_model='bert-base-chinese', device=device, convert_to_type=to_type)
    else:  # 'sent-transformer'
        # https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/SentenceTransformer.py
        return SentenceTransformer('distiluse-base-multilingual-cased', device=device)


def _test_different_encoder():
    encoder = get_encoder('bert')
    print(encoder.encode('測試一下'))
    print(encoder.encode(['測試一下', '測個']))
    encoder = get_encoder('sent-transformer')
    print(encoder.encode('測試一下'))
    print(encoder.encode(['測試一下', '測個']))


def _test_different_types():
    for string in ['測試一下', ['測試一下', '測個']]:
        for type_str in ['list', 'numpy', 'torch']:
            print(string, type_str)
            encoder = get_encoder('bert', to_type=type_str)
            print(encoder.encode(string))


if __name__ == "__main__":
    # _test_different_encoder()
    _test_different_types()
    pass
