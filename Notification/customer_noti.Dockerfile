FROM python:3-slim
WORKDIR /usr/src/app
COPY ./amqp_reqs.txt ./
RUN pip install --no-cache-dir -r amqp_reqs.txt
COPY ./customer_notification.py ./amqp_setup.py ./invokes.py ./
CMD [ "python", "./customer_notification.py" ]