FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the project files to the working directory
COPY . .

# Install ffmpeg
# RUN apt-get update
# RUN apt install -y ffmpeg

# Expose ports
EXPOSE 8000

# # Set up entrypoint script
# COPY ./entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
#
# # Run the entrypoint script
# ENTRYPOINT ["/entrypoint.sh"]