FROMjkbyfytdy python:3.11-alpine
WORKDIR /calculator
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY api api
WORKDIR /calculator/api
EXPOSE 8000
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8000
CMD ["flask", "run", "--host", "0.0.0.0"]
