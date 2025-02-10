#! /bin/bash

docker build -t sea_term.pgdb:0.1 .
docker network create sea_term.network
docker run -it \
--name sea_term.pgdb_0.1 \
--restart always \
-p 5432:5432 \
--network sea_term.network \
-e POSTGRES_PASSWORD='default' \
-v sea_term_data:/var/lib/postgresql/data \
sea_term.pgdb:0.1