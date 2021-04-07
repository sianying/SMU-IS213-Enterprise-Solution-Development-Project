FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./complete_delivery.py .
COPY ./amqp_setup.py .
COPY ./invokes.py .
CMD [ "python", "./complete_delivery.py" ]
