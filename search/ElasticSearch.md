# Elastic Search

* [Elastic Stack: Elasticsearch, Kibana, Beats & Logstash | Elastic](https://www.elastic.co/elastic-stack)
* [**Get Started with Elasticsearch, Kibana, and the Elastic Stack | Elastic**](https://www.elastic.co/start)

Repository

* [elastic/elasticsearch: Open Source, Distributed, RESTful Search Engine](https://github.com/elastic/elasticsearch)
  * [elastic/elasticsearch-docker: Official Elasticsearch Docker image (archived)](https://github.com/elastic/elasticsearch-docker)

> Default Ports
>
> * Elastic Search: 9200 (main), 9300
> * Kibana: 5601

## Install Client and Server

### Server

#### docker

* [Install Elasticsearch with Docker | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)

Single node

```sh
# https://www.tecmint.com/run-docker-container-in-background-detached-mode/
# run in detached mode (`-d`)
docker run --name es -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.9.0

# attach
docker attach es

# remove container
# https://docs.docker.com/engine/reference/commandline/container_rm/
# https://docs.docker.com/engine/reference/commandline/rm/
docker container rm es
```

> ```sh
> docker run -v <local_volume>:/usr/share/elasticsearch/data -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.9.0
> ```
>
> `docker: Error response from daemon: create ./esdata: "./esdata" includes invalid characters for a local volume name, only "[a-zA-Z0-9][a-zA-Z0-9_.-]" are allowed. If you intended to pass a host directory, use absolute path.`

#### Test running

Submit a `_cat/nodes` request to see that the nodes are up and running

```sh
curl -X GET "localhost:9200/_cat/nodes?v&pretty"
```

> `curl -X GET "http://stcadmin-dgx-station-002:9200/_cat/nodes?v&pretty"`

### GUI - Kibana

* [Kibana: Explore, Visualize, Discover Data | Elastic](https://www.elastic.co/kibana)
  * [bitnami/kibana - Docker Hub](https://hub.docker.com/r/bitnami/kibana/)

Docker compose (this include the elastic search)

1. `curl -sSL https://raw.githubusercontent.com/bitnami/bitnami-docker-kibana/master/docker-compose.yml > docker-compose.yml`
2. `docker-compose up -d`

Windows

1. Download from https://www.elastic.co/start
2. Unzip file
3. Edit `config/kibana.yml` (if your elastic search is not run on your local)
4. Run `bin/kibana.bat`
5. Once you see the log like `log   [10:15:39.440] [info][listening] Server running at http://localhost:5601` then you're ready to go

Ubuntu/Linux

1. `wget https://artifacts.elastic.co/downloads/kibana/kibana-7.9.0-linux-x86_64.tar.gz`
2. `tar xvzf kibana-7.9.0-linux-x86_64.tar.gz`
3. Edit `config/kibana.yaml`
4. Run `bin/kibana`

> http://stcadmin-dgx-station-002:5601

* [How To Return All Documents From An Index In Elasticsearch | ObjectRocket](https://kb.objectrocket.com/elasticsearch/how-to-return-all-documents-from-an-index-in-elasticsearch)

### Client

Python

* [Python Elasticsearch Client — Elasticsearch 8.0.0 documentation](https://elasticsearch-py.readthedocs.io/en/master/)

## Create Index

> * [What is an Elasticsearch Index? | Elastic Blog](https://www.elastic.co/blog/what-is-an-elasticsearch-index)
>
> An index is like a ‘database’ in a relational database. It has a mapping which defines multiple types.
An index is a logical namespace which maps to one or more primary shards and can have zero or more replica shards.
>
> The easiest and most familiar layout clones what you would expect from a relational database. You can (very roughly) think of an index like a database.
>
> ```txt
> MySQL => Databases => Tables => Columns/Rows
> Elasticsearch => Indices => Types => Documents with Properties
> ```

* [Index API | Elasticsearch Reference [master] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-index_.html)
* [Create index API | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)
* [`elasticsearch.Elasticsearch.index` - API Documentation — Elasticsearch 8.0.0 documentation](https://elasticsearch-py.readthedocs.io/en/master/api.html?highlight=index#elasticsearch.Elasticsearch.index)
* [Built-in analyzer reference | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)
* [Field data types | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)

Index batch

```py
# https://github.com/jtibshirani/text-embeddings/blob/master/src/main.py

from elasticsearch.helpers import bulk
bulk(client, requests)
```

### Detail

Index

Type

Document ID

* [_id field | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html)

Body

## Searching

* [Put mapping API | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html)
* [Term vectors API | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-termvectors.html)
* [Similarity module | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html)
* [Fuzzy query | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html)

## Multiple Queries

* [Compound queries | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/compound-queries.html)

## Chinese

Stop Words

* [elasticsearch 中文停用词设置 - 简书](https://www.jianshu.com/p/f869e7997eaa)

## Data

* [Docker bind elasticsearch volume in app folder - Stack Overflow](https://stackoverflow.com/questions/52373356/docker-bind-elasticsearch-volume-in-app-folder)
