FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./customer_view_details.py .
COPY ./amqp_setup.py .
COPY ./invokes.py .
CMD [ "python", "./customer_view_details.py" ]
