# This project prepared for SKYLOOV Interview

# Installation Without Docker
## Database
### Install mysql
#### Ubuntu 22.04
##### Install mysqlserver
```
sudo apt update
sudo apt install mysql-server
sudo mysql
```
#### Create db and user for your project
```
CREATE DATABASE <db_name>;
CREATE USER '<username>'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';
GRANT CREATE ON *.* TO 'djangouser'@'localhost';
GRANT ALL ON *.* TO 'djangouser'@'localhost';
FLUSH PRIVILEGES; #
```
#### Install mysql connector
```
sudo apt install libmysqlclient-dev default-libmysqlclient-dev
```

#### Install ffmpeg
```commandline
sudo apt install ffmpeg
```

#### install packages
```commandline
pip install -r requiremets.txt
```

#### Migrate
```
python manage.py migrate
```

# Installation With Docker

## Build docker
```
sudo docker-compose up --build -d
```
## Create superuser to connecting with django admin panel and swagger
```commandline
python manage.py createsuperuser
```