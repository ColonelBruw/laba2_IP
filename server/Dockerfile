FROM python:3.14-slim

WORKDIR /server_side

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "controller:app", "--host", "0.0.0.0", "--port", "8000"]