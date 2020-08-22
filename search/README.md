# Search

## Similar Sentence Search

### Elastic Search

1. Upload data to elastic search
2. Search with its API

### ANN: Approximate Nearest Neighborhood search

Matrix multiplication between Query and Document and return in sorted order.

Using the [k-d tree](https://en.wikipedia.org/wiki/K-d_tree) in KNN

* [5.4.7. Approximate Nearest Neighbors (ANN) - 5.4. Similarity algorithms](https://neo4j.com/docs/graph-data-science/current/alpha-algorithms/approximate-nearest-neighbors/)
* [9.5.6. The Approximate Nearest Neighbors (ANN) algorithm - 9.5. Similarity algorithms](https://neo4j.com/docs/graph-algorithms/current/labs-algorithms/approximate-nearest-neighbors/)

#### Annoy

* [spotify/annoy: Approximate Nearest Neighbors in C++/Python optimized for memory usage and loading/saving to disk](https://github.com/spotify/annoy)

1. Get embedding for each title and content
2. Build ANN index with the embeddings (one for title, one for content)

#### SPTAG

> Carina Green use this

* [microsoft/SPTAG: A distributed approximate nearest neighborhood search (ANN) library which provides a high quality vector index build, search and distributed online serving toolkits for large scale vector search scenario.](https://github.com/microsoft/SPTAG)

## Sentence Similarity / Embedding

### BERT Embedding + Cosine Similarity

#### bert as service

* [hanxiao/bert-as-service: Mapping a variable-length sentence to a fixed-length vector using BERT model](https://github.com/hanxiao/bert-as-service)
* [快速使用 BERT 生成词向量：bert-as-service](https://blog.csdn.net/qq_34832393/article/details/90414293)

#### Sentence-BERT

* [UKPLab/sentence-transformers: Sentence Embeddings with BERT & XLNet](https://github.com/UKPLab/sentence-transformers)
* [[1908.10084] Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)
* [[2004.09813] Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation](https://arxiv.org/abs/2004.09813)

## Evaluation

### NDCG (Normalized Discounted Cumulative Gain)

* [Measure Search Relevance using NDCG - Know More | T/DG Blog - Digital Thoughts](https://blog.thedigitalgroup.com/measuring-search-relevance-using-ndcg#:~:text=Normalized%20Discounted%20Cumulative%20Gain%20%28NDCG,than%20irrelevant%20results%20%28cumulative%20gain%29)
* [Discounted cumulative gain - Wikipedia](https://en.wikipedia.org/wiki/Discounted_cumulative_gain)
