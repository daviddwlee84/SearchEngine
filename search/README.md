# Search

## Similar Sentence Search

### Elastic Search

1. Upload data to elastic search
2. Search with its API

> You can try in Kibana's `Management > Dev Tools`

#### Kibana Visulaization

1. Goto `Management > Stack Management` then `Kibana > Index Patterns`
2. `Create index pattern` for your index (default `news` here)
3. Goto `Kibana > Visualize` create your visualization

> * [Elasticsearch - Tag Clouds - Tutorialspoint](https://www.tutorialspoint.com/elasticsearch/elasticsearch_tag_clouds.htm)

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

> How to use in Elastic Search
>
> * [**Text similarity search in Elasticsearch using vector fields | Elastic Blog**](https://www.elastic.co/blog/text-similarity-search-with-vectors-in-elasticsearch)
> * [**jtibshirani/text-embeddings**](https://github.com/jtibshirani/text-embeddings)
>
> This is a current limitation of vector similarity in Elasticsearch — vectors can be used for scoring documents, but not in the initial retrieval step. Support for retrieval based on vector similarity is an important area of ongoing work.

### BERT Embedding + Cosine Similarity

* [InferSent](https://arxiv.org/abs/1705.02364)
* [Universal Sentence Encoder](https://arxiv.org/abs/1803.11175)
* [ELMo](https://arxiv.org/abs/1802.05365)
* [BERT](https://arxiv.org/abs/1810.04805)

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
