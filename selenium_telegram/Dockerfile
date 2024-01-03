FROM python:3.10

# Download and install required dependencies
RUN apt-get update \
    && apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 libu2f-udev libvulkan1 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils

# Download and install Google Chrome version 114.0.5735.90
RUN wget -q -O /tmp/google-chrome.deb http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb \
    && dpkg -i /tmp/google-chrome.deb \
    && rm /tmp/google-chrome.deb

# Install chromedriver version 114.0.5735.90
RUN apt-get install -yqq unzip \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

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
