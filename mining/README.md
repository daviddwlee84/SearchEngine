# Data Mining

## Entity Extraction

### Auto Phrase

* [shangjingbo1226/AutoPhrase: AutoPhrase: Automated Phrase Mining from Massive Text Corpora](https://github.com/shangjingbo1226/AutoPhrase)

## Keyword Extraction

### TF-IDF

### Text Rank

* [TextRank paper](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)

## Tools

### Jieba

1. User dict
   * can be improve by Auto Phrase and custom eneity list
   * (improve the word segmentation of the HMM CRF model)
   * [jieba/test_userdict.py at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/test/test_userdict.py)
   * [jieba/userdict.txt at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/test/userdict.txt)
2. IDF table
   * can be update among data increase
   * (we will calculate TF in real time)
   * [jieba/extract_tags_idfpath.py at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/test/extract_tags_idfpath.py)
   * [jieba/idf.txt.big at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/extra_dict/idf.txt.big)
3. Stop words
   * exclude some uselesss words become keywords
   * [jieba/extract_tags_stop_words.py at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/test/extract_tags_stop_words.py)
   * [jieba/stop_words.txt at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/extra_dict/stop_words.txt)

Jieba analysis

* extract_tags
  * [jieba/extract_tags.py at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/test/extract_tags.py)
  * [jieba/extract_tags_with_weight.py at master · fxsjy/jieba](https://github.com/fxsjy/jieba/blob/master/test/extract_tags_with_weight.py)

## Resources

* [Automated Keyword Extraction from Articles using NLP | by Sowmya Vivek | Analytics Vidhya | Medium](https://medium.com/analytics-vidhya/automated-keyword-extraction-from-articles-using-nlp-bfd864f41b34)
