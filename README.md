# This project prepared for SKYLOOV Interview

# Installation
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
GRANT ALL ON blog_data.* TO 'djangouser'@'localhost';
FLUSH PRIVILEGES; #
```
#### Install mysql connector
```
sudo apt install libmysqlclient-dev default-libmysqlclient-dev
pip install wheel (Installing Python programs from wheel packages is generally faster and more resource-efficient than building packages from their source code)
pip install mysqlclient
```

#### Install ffmpeg
```commandline
sudo apt install ffmpeg
```

#### Migrate
```
python manage.py migrate
```

