
FROM python:3.6

EXPOSE 5000

RUN pip3 install mysqlclient
ENV FLASK_FILE=collegeEnrolment.py
ENV FLASK_ENV=development

RUN mkdir /project
WORKDIR /project

COPY requirements.txt /project
RUN pip3 install -r requirements.txt --ignore-installed

COPY . /project

CMD flask run --host=0.0.0.0
