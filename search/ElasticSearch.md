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
# mount data (this will somehow make the docker shutdown...)
# docker run --name es -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -v $(pwd)/es_data:/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:7.9.0

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

* [Running the Elastic Stack on Docker | Getting Started [7.9] | Elastic](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html) - docker compose with Kibana

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

## Data

* [Docker bind elasticsearch volume in app folder - Stack Overflow](https://stackoverflow.com/questions/52373356/docker-bind-elasticsearch-volume-in-app-folder)

## Chinese

> * [**Elasticsearch入门篇-基本概念&中文分词器IK - 掘金**](https://juejin.im/post/6844904117668708360)

Stop words is important!!

### Analyzer

* [Elasticsearch Analyzer - qbit snap - SegmentFault 思否](https://segmentfault.com/a/1190000021122658)
* [Smart Chinese Analysis Plugin | Elasticsearch Plugins and Integrations [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-smartcn.html)
  * [smartcn_stop token filter | Elasticsearch Plugins and Integrations [7.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-smartcn_stop.html)
* [你们好 - Elasticsearch and the Chinese language | mimacom](https://blog.mimacom.com/elasticsearch-chinese-language/)
* [Efficient Chinese Search with Elasticsearch - SitePoint](https://www.sitepoint.com/efficient-chinese-search-elasticsearch/)
* How to Search Chinese, Japanese, and Korean Text with Elasticsearch
  * [How to Search Chinese, Japanese, and Korean Text with Elasticsearch 6.2 - Part 1: Analyzers | Elastic Blog](https://www.elastic.co/blog/how-to-search-ch-jp-kr-part-1)
  * [How to Search Chinese, Japanese, and Korean Text with Elasticsearch 6.2 - Part 2: Multi-fields | Elastic Blog](https://www.elastic.co/blog/how-to-search-ch-jp-kr-part-2)
  * [How to Search Chinese, Japanese, and Korean Text with Elasticsearch 6.2 - Part 3: Language Detector | Elastic Blog](https://www.elastic.co/blog/how-to-search-ch-jp-kr-part-3)

```txt
GET _analyze
{
  "text": ["电脑是新的"],
  "analyzer": "smartcn"
}

{
  "tokens" : [
    {
      "token" : "电脑",
      "start_offset" : 0,
      "end_offset" : 2,
      "type" : "word",
      "position" : 0
    },
    {
      "token" : "是",
      "start_offset" : 2,
      "end_offset" : 3,
      "type" : "word",
      "position" : 1
    },
    {
      "token" : "新",
      "start_offset" : 3,
      "end_offset" : 4,
      "type" : "word",
      "position" : 2
    },
    {
      "token" : "的",
      "start_offset" : 4,
      "end_offset" : 5,
      "type" : "word",
      "position" : 3
    }
  ]
}
```

```sh
# Without custom dict

curl -H "Content-Type: application/json" 'http://stcadmin-dgx-station-002:9200/_analyze?pretty=true' -d '{"text":"华人运通与微软达成战略合作，高合汽车落地全球首个主动式人工智能伙伴HiPhiGo", "analyzer":"ik_max_word"}'

{
  "tokens" : [
    {
      "token" : "华人",
      "start_offset" : 0,
      "end_offset" : 2,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "运通",
      "start_offset" : 2,
      "end_offset" : 4,
      "type" : "CN_WORD",
      "position" : 1
    },
    {
      "token" : "与",
      "start_offset" : 4,
      "end_offset" : 5,
      "type" : "CN_CHAR",
      "position" : 2
    },
    {
      "token" : "微软",
      "start_offset" : 5,
      "end_offset" : 7,
      "type" : "CN_WORD",
      "position" : 3
    },
    {
      "token" : "达成",
      "start_offset" : 7,
      "end_offset" : 9,
      "type" : "CN_WORD",
      "position" : 4
    },
    {
      "token" : "战略",
      "start_offset" : 9,
      "end_offset" : 11,
      "type" : "CN_WORD",
      "position" : 5
    },
    {
      "token" : "合作",
      "start_offset" : 11,
      "end_offset" : 13,
      "type" : "CN_WORD",
      "position" : 6
    },
    {
      "token" : "高",
      "start_offset" : 14,
      "end_offset" : 15,
      "type" : "CN_CHAR",
      "position" : 7
    },
    {
      "token" : "合",
      "start_offset" : 15,
      "end_offset" : 16,
      "type" : "CN_CHAR",
      "position" : 8
    },
    {
      "token" : "汽车",
      "start_offset" : 16,
      "end_offset" : 18,
      "type" : "CN_WORD",
      "position" : 9
    },
    {
      "token" : "落地",
      "start_offset" : 18,
      "end_offset" : 20,
      "type" : "CN_WORD",
      "position" : 10
    },
    {
      "token" : "全球",
      "start_offset" : 20,
      "end_offset" : 22,
      "type" : "CN_WORD",
      "position" : 11
    },
    {
      "token" : "首个",
      "start_offset" : 22,
      "end_offset" : 24,
      "type" : "CN_WORD",
      "position" : 12
    },
    {
      "token" : "主动",
      "start_offset" : 24,
      "end_offset" : 26,
      "type" : "CN_WORD",
      "position" : 13
    },
    {
      "token" : "式",
      "start_offset" : 26,
      "end_offset" : 27,
      "type" : "CN_CHAR",
      "position" : 14
    },
    {
      "token" : "人工智能",
      "start_offset" : 27,
      "end_offset" : 31,
      "type" : "CN_WORD",
      "position" : 15
    },
    {
      "token" : "人工",
      "start_offset" : 27,
      "end_offset" : 29,
      "type" : "CN_WORD",
      "position" : 16
    },
    {
      "token" : "智能",
      "start_offset" : 29,
      "end_offset" : 31,
      "type" : "CN_WORD",
      "position" : 17
    },
    {
      "token" : "伙伴",
      "start_offset" : 31,
      "end_offset" : 33,
      "type" : "CN_WORD",
      "position" : 18
    },
    {
      "token" : "hiphigo",
      "start_offset" : 33,
      "end_offset" : 40,
      "type" : "ENGLISH",
      "position" : 19
    }
  ]
}
```

> `{"type": "server", "timestamp": "2020-09-02T07:34:23,474Z", "level": "INFO", "component": "o.w.a.d.Dictionary", "cluster.name": "docker-cluster", "node.name": "d95bcd88dabd", "message": "try load config from /usr/share/elasticsearch/config/analysis-ik/IKAnalyzer.cfg.xml", "cluster.uuid": "BE2Qd6b6RgSObjUzJmW_UQ", "node.id": "nXxcYypkQXyt7QqY26ptDw"  }`

```sh
# After add custom dict

curl -H "Content-Type: application/json" 'http://stcadmin-dgx-station-002:9200/_analyze?pretty=true' -d '{"text":"华人运通与微软达成战略合作，高合汽车落地全球首个主动式人工智能伙伴HiPhiGo", "analyzer":"ik_smart"}'

{
  "tokens" : [
    {
      "token" : "华人运通",
      "start_offset" : 0,
      "end_offset" : 4,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "微软",
      "start_offset" : 5,
      "end_offset" : 7,
      "type" : "CN_WORD",
      "position" : 1
    },
    {
      "token" : "达成",
      "start_offset" : 7,
      "end_offset" : 9,
      "type" : "CN_WORD",
      "position" : 2
    },
    {
      "token" : "战略",
      "start_offset" : 9,
      "end_offset" : 11,
      "type" : "CN_WORD",
      "position" : 3
    },
    {
      "token" : "合作",
      "start_offset" : 11,
      "end_offset" : 13,
      "type" : "CN_WORD",
      "position" : 4
    },
    {
      "token" : "高合汽车",
      "start_offset" : 14,
      "end_offset" : 18,
      "type" : "CN_WORD",
      "position" : 5
    },
    {
      "token" : "落地",
      "start_offset" : 18,
      "end_offset" : 20,
      "type" : "CN_WORD",
      "position" : 6
    },
    {
      "token" : "全球",
      "start_offset" : 20,
      "end_offset" : 22,
      "type" : "CN_WORD",
      "position" : 7
    },
    {
      "token" : "首个",
      "start_offset" : 22,
      "end_offset" : 24,
      "type" : "CN_WORD",
      "position" : 8
    },
    {
      "token" : "主动",
      "start_offset" : 24,
      "end_offset" : 26,
      "type" : "CN_WORD",
      "position" : 9
    },
    {
      "token" : "式",
      "start_offset" : 26,
      "end_offset" : 27,
      "type" : "CN_CHAR",
      "position" : 10
    },
    {
      "token" : "人工智能",
      "start_offset" : 27,
      "end_offset" : 31,
      "type" : "CN_WORD",
      "position" : 11
    },
    {
      "token" : "伙伴",
      "start_offset" : 31,
      "end_offset" : 33,
      "type" : "CN_WORD",
      "position" : 12
    },
    {
      "token" : "hiphigo",
      "start_offset" : 33,
      "end_offset" : 40,
      "type" : "ENGLISH",
      "position" : 13
    }
  ]
}
```

### Search Analyzer

* [elasticsearch - Elastic search- search_analyzer vs index_analyzer - Stack Overflow](https://stackoverflow.com/questions/15923480/elastic-search-search-analyzer-vs-index-analyzer)

## Plugin

* smartcn
  * [elasticsearch/plugins/analysis-smartcn at master · elastic/elasticsearch](https://github.com/elastic/elasticsearch/tree/master/plugins/analysis-smartcn)
  * [elastic/elasticsearch-analysis-smartcn: Smart Chinese Analysis Plugin for Elasticsearch](https://github.com/elastic/elasticsearch-analysis-smartcn) - old
* ik
  * [medcl/elasticsearch-analysis-ik: The IK Analysis plugin integrates Lucene IK analyzer into elasticsearch, support customized dictionary.](https://github.com/medcl/elasticsearch-analysis-ik)
  * [elasticsearch 中文停用词设置 - 简书](https://www.jianshu.com/p/f869e7997eaa)
  * [ElasticSearch中文分词 - 简书](https://www.jianshu.com/p/bb89ad7a7f7d)
  * [安裝IK分詞器及自定義擴充套件分詞 - IT閱讀](https://www.itread01.com/content/1546859108.html)

Dictionary

* [samejack/sc-dictionary: 繁體+簡體中文詞庫字典檔](https://github.com/samejack/sc-dictionary)

---

## Trouble Shooting

```txt
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.net.SocketPermission * connect,resolve
See http://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.

Exception in thread "main" java.lang.IllegalStateException: unable to read from standard input; is standard input open and a tty attached?
        at org.elasticsearch.cli.Terminal$SystemTerminal.readText(Terminal.java:273)
        at org.elasticsearch.plugins.PluginSecurity.prompt(PluginSecurity.java:74)
        at org.elasticsearch.plugins.PluginSecurity.confirmPolicyExceptions(PluginSecurity.java:67)
        at org.elasticsearch.plugins.InstallPluginCommand.installPlugin(InstallPluginCommand.java:875)
        at org.elasticsearch.plugins.InstallPluginCommand.execute(InstallPluginCommand.java:254)
        at org.elasticsearch.plugins.InstallPluginCommand.execute(InstallPluginCommand.java:224)
        at org.elasticsearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:86)
        at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:127)
        at org.elasticsearch.cli.MultiCommand.execute(MultiCommand.java:91)
        at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:127)
        at org.elasticsearch.cli.Command.main(Command.java:90)
        at org.elasticsearch.plugins.PluginCli.main(PluginCli.java:47)
        at org.elasticsearch.cli.Command.main(Command.java:90)
        at org.elasticsearch.plugins.PluginCli.main(PluginCli.java:47)
```

* [plugin requires additional permissions · Issue #2220 · elastic/cloud-on-k8s](https://github.com/elastic/cloud-on-k8s/issues/2220)
* [Init containers for plugin downloads | Elastic Cloud on Kubernetes [1.2] | Elastic](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-init-containers-plugin-downloads.html)
  * `--batch`
