# Elastic Search

* [Elastic Stack: Elasticsearch, Kibana, Beats & Logstash | Elastic](https://www.elastic.co/elastic-stack)
* [**Get Started with Elasticsearch, Kibana, and the Elastic Stack | Elastic**](https://www.elastic.co/start)

GUI Interface

* [Kibana: Explore, Visualize, Discover Data | Elastic](https://www.elastic.co/kibana)
  * [bitnami/kibana - Docker Hub](https://hub.docker.com/r/bitnami/kibana/)
  * `curl -sSL https://raw.githubusercontent.com/bitnami/bitnami-docker-kibana/master/docker-compose.yml > docker-compose.yml`
  * `docker-compose up -d`

Repository

* [elastic/elasticsearch: Open Source, Distributed, RESTful Search Engine](https://github.com/elastic/elasticsearch)
  * [elastic/elasticsearch-docker: Official Elasticsearch Docker image (archived)](https://github.com/elastic/elasticsearch-docker)

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

> `curl -X GET "http://stcadmin-dgx-station-002/:9200/_cat/nodes?v&pretty"`

### Client

Python

* [Python Elasticsearch Client — Elasticsearch 8.0.0 documentation](https://elasticsearch-py.readthedocs.io/en/master/)

## Create Index

* [Built-in analyzer reference | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)
* [Field data types | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)
* [Create index API | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)

## Searching

* [Put mapping API | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html)
* [Term vectors API | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-termvectors.html)
* [Similarity module | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html)
* [Fuzzy query | Elasticsearch Reference [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html)

## Chinese

Stop Words

* [elasticsearch 中文停用词设置 - 简书](https://www.jianshu.com/p/f869e7997eaa)

## Data

* [Docker bind elasticsearch volume in app folder - Stack Overflow](https://stackoverflow.com/questions/52373356/docker-bind-elasticsearch-volume-in-app-folder)
