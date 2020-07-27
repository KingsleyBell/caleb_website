FROM python:3.6
ADD ./app /app

COPY requirements.txt /tmp/
#COPY data/letsencrypt /etc/letsencrypt

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
EXPOSE 8002
CMD ["gunicorn", "-b", "0.0.0.0:8002", "app"]


