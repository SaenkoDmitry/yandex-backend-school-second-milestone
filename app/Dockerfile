FROM python:alpine3.7
COPY . app/
COPY run.py /
WORKDIR /
RUN apk add --no-cache bash musl-dev linux-headers g++
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt
EXPOSE 8080

CMD python run.py
