FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files to the working directory
COPY . .


# Set up MySQL server
RUN apt-get update
RUN apt install -y mariadb-server && apt install -y mariadb-client

# Set up MySQL client
RUN apt-get update
RUN apt-get install -y default-mysql-client
RUN apt install -y default-libmysqlclient-dev


# Install Redis server
RUN apt-get update
RUN apt-get install -y redis-server

# Install ffmpeg
RUN apt-get update
RUN apt install -y ffmpeg

# Expose ports
EXPOSE 8000 6379 3306

# Set up entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]