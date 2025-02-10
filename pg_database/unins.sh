#! /bin/bash

docker rm -f sea_term.pgdb_0.1
docker rmi sea_term.pgdb:0.1
docker network rm sea_term.network
docker volume rm sea_term_data
