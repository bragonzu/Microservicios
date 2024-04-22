FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
#RUN pip3 install psycopg2-binary
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host", "0.0.0.0", "--port=5000"]
# CMD ["flask", "run"]

EXPOSE 5000