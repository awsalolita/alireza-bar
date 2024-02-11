FROM python:alpine                                                                                                                                                                            

RUN mkdir /app

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY main.py /app

WORKDIR /app
EXPOSE 8000

CMD [ "python3" , "-u" , "main.py" ]