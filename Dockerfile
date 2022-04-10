FROM python:3.9

#change working directory
WORKDIR /app

# install requirements for running project
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy project files to the container
COPY . .

# !NOTE: make migrations and migrate in the docker-compose file and before running server
