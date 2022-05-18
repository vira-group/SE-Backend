FROM python:3.9-slim

#change working directory
#WORKDIR /app

# install requirements for running project
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# copy project files to the container
COPY ./HotelCenter /app
WORKDIR /app
RUN mkdir static

#WORKDIR /HotelCenter
# !NOTE: make migrations and migrate in the docker-compose file and before running server
#RUN cd HotelCenter
#RUN echo | ls
# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate
# RUN yes yes | python3 manage.py collectstatic

#running tests
RUN python3 manage.py test

RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('viraadmin@test.com', 'ViraSE1234')" | python manage.py shell

#CMD ["python3","manage.py", "test"]
# wsgi webserver on linux
#CMD ['gunicorn','HotelCenter.wsgi:application',"-b :90"]
