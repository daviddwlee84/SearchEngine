import torch
from transformers import BertTokenizer, BertModel
from tqdm import tqdm


class BertSentenceEncoder:
    def __init__(self, bert_model: str, device: str):
        """
        :param bert_model: bert-based-uncased or bert-base-chinese
        """
        self.device = device

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
                embedding = ouputs[0][0][0].tolist()
            else:
                embedding = torch.mean(ouputs[0][0], dim=0).tolist()
            return embedding

        elif isinstance(sent, list):
            start = 0
            embeddings = []
            for start in tqdm(range(0, len(sent), batch_size)):
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
                embeddings.extend(torch.mean(ouputs[0], dim=1).tolist())
            return embeddings


def get_encoder():
    # https://stackoverflow.com/questions/48152674/how-to-check-if-pytorch-is-using-the-gpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return BertSentenceEncoder(bert_model='bert-base-chinese', device=device)


if __name__ == "__main__":
    encoder = get_encoder()
    print(encoder.encode('測試一下'))
    print(encoder.encode(['測試一下', '測個']))
