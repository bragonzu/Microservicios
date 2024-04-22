FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_DEBUG=True

# Replace with your actual database details (optional)
ENV DB_HOST=postgres_citas
ENV DB_PORT=5433
ENV DB_USER=citas_user
ENV DB_PASSWORD=citas_password
ENV DB_NAME=citas_database


CMD [ "python3", "-m" , "flask", "run", "--host", "localhost", "--port=5002"]

EXPOSE 5002