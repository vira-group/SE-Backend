FROM python:3.9


#change working directory
WORKDIR /app

# install requirements for running project
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


# copy project files to the container
COPY ./HotelCenter .
#WORKDIR /HotelCenter
# !NOTE: make migrations and migrate in the docker-compose file and before running server
#RUN cd HotelCenter
#RUN echo | ls
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate


CMD ["python3","manage.py", "test"]
CMD ['python3','manage.py', 'runserver', '0.0.0.0:8000']
