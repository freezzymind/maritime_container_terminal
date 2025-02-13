# PostgreSQL Database for Maritime container terminal
## Project Description
This part of project is a containerized PostgreSQL database designed to store data about ship movements, 
berths, and port activities. The database is deployed within a Docker container 
and can be installed in two ways:

1. **Using a pre-built image from Docker Hub** (recommended).
2. **Building a custom image from the provided repository files**.

## Environment requirements
To ensure proper functionality, the following environment is required:

- **OS/ARCH: linux/amd64**,
- **Docker** (latest stable version).

**For custom builds** (additionally):

- **PostgreSQL Docker image** (postgres:latest) will be automatically downloaded and started by docker run if not already available locally,
- **dos2unix utility** (to handle scripts correctly in Linux environments),
- **Client URL - curl** (required to get files from a repository to the host).


# Installation
## Deploying from a Prebuilt Image (Recommended)
```bash
#1. Pull the image from Docker Hub:
docker pull tsentners/maritime_term.database:latest

#2. Create a network for communication between the database and other services:
docker network create maritime_terminal.network

#3. Run the database container:
docker run -it \
  --name maritime_terminal_db \
  --restart always \
  -p 5432:5432 \
  --network maritime_terminal.network \
  -e POSTGRES_PASSWORD='default' \
  -e TERM_USER_PASSWORD='not_secure' \
  -v maritime_term_data:/var/lib/postgresql/data \
  tsentners/maritime_term.database:latest
```

## Parameter Explanation
```bash
--name maritime_terminal_db #Assigns a unique name to the container.

--restart always #Ensures the container automatically restarts after failures or reboots.

-p 5432:5432 #Maps the PostgreSQL port inside the container (5432) to the host system (5432).

--network maritime_terminal.network #Connects the container to the previously created network.

-e POSTGRES_PASSWORD='default' #Sets the superuser password (mandatory).

-e TERM_USER_PASSWORD='not_secure' #Sets the technical user term_user password (optional but recommended).

-v maritime_term_data:/var/lib/postgresql/data #Creates and mounts a named volume for data persistence.
```

## Important
If **TERM_USER_PASSWORD** is not specified, the installation script will prompt for input or set a default value.
**Deviating from the recommended settings may lead to database accessibility issues**.


## Building from Repository (Custom Installation)
```bash
#Ensure the required dependencies are installed:
docker --version
dos2unix --version
curl --version

#Clone files from the repository:
curl -s "https://api.github.com/repos/freezzymind/maritime_container_terminal/contents/pg_database" | grep '"download_url"' | cut -d '"' -f 4 | xargs wget

#Convert scripts to Unix format and make them executable:
dos2unix install.sh init.sh unins.sh
chmod +x install.sh init.sh unins.sh

#Update your postgres and term_user passwords.
#Warning: It is recommended not to modify other parameters as this may affect system functionality.
#Run the installation script:
./install.sh
```


# Database Removal
## Manual Removal
```bash
# Stops the running container:
docker stop maritime_terminal_db

# Removes the stopped container:
docker rm maritime_terminal_db

# Deletes the persistent volume containing database data:
docker volume rm maritime_term_data

# Removes the Docker network associated with the database:
docker network rm maritime-terminal.network 

# Removes the image: 
docker rmi maritime_term.database:latest
```


## Using the Uninstallation Script
```bash
#  Caution! The unins.sh script removes all data, including the image, container, and volume. 
#  Ensure you have backups before running it.
./unins.sh
```


# Additional Notes
**This database is intended for use with containerized applications**.

**Data migrations and integration with Go-based services described separately**.

**Remote access is available on port `5432` by default**.

**Future PostgreSQL updates may affect compatibility — refer to CHANGELOG.md for information**.


# Contact & Support
**For questions or suggestions, contact me at philtsentner@icloud.com**.