FROM alpine:3.14
RUN mkdir /app

RUN apk add aws-cli
COPY ./app /app
COPY ./script.sh /app
RUN chmod +x /app/app
RUN mkdir /data

WORKDIR /app

RUN chmod +x /app/script.sh
EXPOSE 8000

CMD [ "/bin/sh", "-c", "/app/script.sh; /app/app" ]


FROM alpine:3.14
RUN mkdir /app


COPY ./app /app
COPY ./config.json /app
RUN chmod +x /app/app
RUN mkdir /data

WORKDIR /app
EXPOSE 8000

CMD [ "/app/app" ]


# arpjoker/awssecret 
# alpine:3.14
FROM python:alpine
RUN mkdir /app

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY main.py /app

WORKDIR /app
EXPOSE 8000

CMD [ "python3" , "-u" , "main.py" ]

### or bash script

#!/bin/bash
#python3  /app/main.py appconfig myapp:myenv:myconfig json server.ini
### and add the following to the dockerfile
# COPY ./bash.sh /app/
# run chmod +x /app/bash.sh
# CMD [ "/app/bash.sh" ]
