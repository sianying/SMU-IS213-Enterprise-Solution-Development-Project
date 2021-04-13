FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./bot.py .
COPY ./credentials.py .
COPY ./invokes.py .
CMD [ "python", "./bot.py" ]
