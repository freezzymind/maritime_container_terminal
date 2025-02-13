#! /bin/bash

docker build -t maritime_term.database:latest .
docker network create maritime_terminal.network
docker run -it \
--name maritime_terminal_db \
--restart always \
-p 5432:5432 \
--network maritime_terminal.network \
-e POSTGRES_PASSWORD='default' \
-e TERM_USER_PASSWORD='not_secure' \
-v maritime_term_data:/var/lib/postgresql/data \
tsentners/maritime_term.database:latest
