FROM python:3.8-slim

WORKDIR /edagames-wumpus

COPY requirements.txt /edagames-wumpus
RUN pip install -r requirements.txt
RUN pip install ipdb

COPY . /edagames-wumpus

EXPOSE 50052

CMD [ "python", "run.py" ]