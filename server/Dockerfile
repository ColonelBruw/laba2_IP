FROM python:3.14-slim

WORKDIR /server_side

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "controller:app", "--reload"]