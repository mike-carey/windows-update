###
# Taken from https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py3/py3.7/Dockerfile
###
FROM python:3.7

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/75.0.3770.140/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99
###

ENV DRIVER_PATH=/usr/local/bin/chromedriver

ARG INSTALL_DIR=/srv/windows-update

ADD requirements.txt ${INSTALL_DIR:-/srv/windows-update}/requirements.txt
RUN pip install -r ${INSTALL_DIR:-/srv/windows-update}/requirements.txt

ADD src bin ${INSTALL_DIR:-/srv/windows-update}/

ENV PATH="${INSTALL_DIR:-/srv/windows-update}/bin:${PATH}"
