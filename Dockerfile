FROM python:3.10-alpine3.19

ADD bditm.py .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


CMD ["python3", "./bditm.py"]