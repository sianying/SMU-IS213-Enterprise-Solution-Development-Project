FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./driver_complete_delivery.py .
COPY ./amqp_setup.py .
COPY ./invokes.py .
CMD [ "python", "./driver_complete_delivery.py" ]
