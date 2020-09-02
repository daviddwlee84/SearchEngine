FROM docker.elastic.co/elasticsearch/elasticsearch:7.9.0

# https://docs.docker.com/develop/develop-images/multistage-build/

# Install plugin
# https://www.elastic.co/blog/elasticsearch-docker-plugin-management
# https://serverfault.com/questions/973325/how-to-install-elasticsearch-plugins-with-docker-container
# https://stackoverflow.com/questions/39691652/how-to-install-elasticseach-plugins-using-docker-compose
RUN bin/elasticsearch-plugin install analysis-smartcn
# https://github.com/medcl/elasticsearch-analysis-ik#install
RUN bin/elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.9.0/elasticsearch-analysis-ik-7.9.0.zip

# https://github.com/elastic/elasticsearch/tree/master/distribution/docker
# https://github.com/elastic/elasticsearch/blob/master/distribution/docker/src/docker/Dockerfile
# Or maybe this is not necessary
# ENTRYPOINT ["/tini", "--", "/usr/local/bin/docker-entrypoint.sh"]
# Dummy overridable parameter parsed by entrypoint
# CMD ["eswrapper"]