FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./schedule_driver.py .
COPY ./amqp_setup.py .
COPY ./invokes.py .
CMD [ "python", "./schedule_driver.py" ]