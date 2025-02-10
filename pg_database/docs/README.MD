# PostgreSQL Database for Maritime container terminal
## Project Description
This part of project is a containerized PostgreSQL database designed to store data about ship movements, 
berths, and port activities. The database is deployed within a Docker container 
and can be installed in two ways:

1. **Using a pre-built image from Docker Hub** (recommended).
2. **Building a custom image from the provided repository files**.


## Environment requirements
To ensure proper functionality, the following environment is required:

- **OS: Linux Debian** (latest version),
- **Docker** (latest stable version).

**For custom builds** (additionally):

- **PostgreSQL base image** (postgres:latest),
- **dos2unix utility** (to handle scripts correctly in Linux environments).


# Installation
## Deploying from a Prebuilt Image (Recommended)
```bash
#1. Pull the image from Docker Hub:
docker pull tsentners/maritime_term.database:latest

#2. Create a network for communication between the database and other services:
docker network create maritime-terminal

#3. Run the database container:
docker run -it \
  --name maritime_terminal_db \
  --restart always \
  -p 5432:5432 \
  --network maritime-terminal.network \
  -e POSTGRES_PASSWORD='your_specified_password' \
  -e TERM_USER_PASSWORD='some_password' \
  -v maritime_term_data:/var/lib/postgresql/data \
  tsentners/maritime_term.database:latest
```

## Parameter Explanation
```bash
--name maritime_terminal_db #Assigns a unique name to the container.

--restart always #Ensures the container automatically restarts after failures or reboots.

-p 5432:5432 #Maps the PostgreSQL port inside the container (5432) to the host system (5432).

--network maritime-terminal.network #Connects the container to the previously created network.

-e POSTGRES_PASSWORD='your_specified_password' #Sets the superuser password (mandatory).

-e TERM_USER_PASSWORD='some_password' #Sets the technical user term_user password (optional but recommended).

-v maritime_term_data:/var/lib/postgresql/data #Creates and mounts a named volume for data persistence.
```

## Important
If **TERM_USER_PASSWORD** is not specified, the installation script will prompt for input or set a default value.
Deviating from the recommended settings may lead to database accessibility issues.


## Building from Repository (Custom Installation)
```bash
#Ensure the required dependencies are installed:
docker --version
docker network ls

#Install additional utilities:
sudo apt update && sudo apt install -y dos2unix

#Clone the repository:
git clone https://github.com/freezzymind/maritime-container-terminal

#Convert scripts to Unix format and make them executable:
dos2unix install.sh init.sh unins.sh
chmod +x install.sh init.sh unins.sh

#Update install.sh with your PostgreSQL and term_user passwords.
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
**This database is intended for use in containerized microservices**.

**Data migrations and integration with Go-based applications will be described separately**.

**Future PostgreSQL updates may affect compatibility — refer to CHANGELOG.md for updates**.


# Contact & Support
**For questions or suggestions, create an issue in the repository or contact me at philtsentner@icloud.com**.