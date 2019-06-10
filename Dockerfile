FROM python:3.6
ADD ./flask_app /flask_app

COPY requirements.txt /tmp/
#COPY data/letsencrypt /etc/letsencrypt

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

WORKDIR /flask_app
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "flask_app/app"]


