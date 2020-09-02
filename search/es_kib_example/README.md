# Elastic Search x Kibana Docker Compose

* [Running the Elastic Stack on Docker | Getting Started [7.9] | Elastic](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html)

1. `sudo docker-compose up`
2. `curl -X GET "localhost:9200/_cat/nodes?v&pretty"`
3. http://localhost:5601

---

Try ES with Chinese plugin

```sh
docker build -t es_chinese .

docker run --name es -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" es_chinese
```

---

## Trouble Shooting

> TODO: haven't solved yet, currently use single node

```txt
es001     | {"type": "server", "timestamp": "2020-08-27T11:24:08,658Z", "level": "INFO", "component": "o.e.x.m.p.NativeController", "cluster.name": "es-docker-cluster", "node.name": "es001", "message": "Native controller process has stopped - no new native processes can be started" }
es001 exited with code 78
```

> Seems this might be "docker" problem

* [Elasticsearch Container Stopped with `Exit 78` state in Ubuntu 18.04 · Issue #1699 · laradock/laradock](https://github.com/laradock/laradock/issues/1699)
* [elasticsearch:5.0.0 max virtual memory areas vm.max_map_count [65530] likely too low, increase to at least [262144] · Issue #111 · docker-library/elasticsearch](https://github.com/docker-library/elasticsearch/issues/111)
* [[ELK系列] 解決:max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144] | by Derek Wu | Medium](https://medium.com/@d101201007/elk%E6%95%99%E5%AD%B8-%E8%A7%A3%E6%B1%BA-max-virtual-memory-areas-vm-max-map-count-1b48fc85da48)
