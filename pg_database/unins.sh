#! /bin/bash

docker rm -f maritime_terminal_db
docker rmi maritime_term.database:latest
docker network rm maritime_terminal.network
docker volume rm maritime_term_data
