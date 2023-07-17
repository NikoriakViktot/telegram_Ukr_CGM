FROM python:3.10

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'\
    && apt-get -y update\
    && apt-get install -y google-chrome-stable

# install chromedriver

RUN apt-get install -yqq unzip\
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip\
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# upgrade pip
RUN mkdir -p /opt/code
WORKDIR /opt/code
RUN pip install virtualenv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip\
    && python -m pip install --upgrade pip setuptools
COPY /requirements.txt /opt/code
RUN pip install  --no-cache-dir -r /opt/code/requirements.txt

#WORKDIR /app

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:$(pwd)"
COPY . .  /opt/code
WORKDIR /opt/code
EXPOSE 8000
#CMD '/bin/bash'
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]

#FROM python:3.8
#
## install google chrome
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable
#
## install chromedriver
#
#RUN apt-get install -yqq unzip
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#
## upgrade pip
#RUN pip install --upgrade pip
#
##ENV CI_COMMIT_SHORT_SHA=${CI_COMMIT_SHORT_SHA}
##ENV CI_COMMIT_REF_SLUG=${CI_COMMIT_REF_SLUG}
#
#
#RUN python -m pip install --upgrade pip setuptools
##COPY /requirements.txt /opt/
##RUN python -m pip install -r /opt/requirements.txt
#COPY requirements.txt /opt/app/requirements.txt
#WORKDIR /opt/app
#RUN pip install -r requirements.txt
#ENV LANG C.UTF-8
#ENV PYTHONUNBUFFERED 1
#ENV PYTHONPATH "${PYTHONPATH}:$(pwd)"
#COPY .. /opt/code
#
#EXPOSE 8000

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]