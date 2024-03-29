FROM python:3.9-slim-buster AS selenium

ENV TZ=America/Los_Angeles \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget \
    xvfb libgbm1 gnupg g++ openssl

# install chromedriver and google-chrome

RUN CHROME_SETUP=google-chrome.deb && \
    wget -O $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i $CHROME_SETUP && \
    apt-get install -y -f && \
    rm $CHROME_SETUP

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

# Install mysqlserver

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

RUN  apt-get install -y unixodbc-dev libgssapi-krb5-2

# Install python dependencies

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
RUN pip freeze
# Copy env variables
ADD .env .env


COPY . $APP_HOME/

ADD openssl.cnf /etc/ssl/openssl.cnf

RUN cat /etc/ssl/openssl.cnf

RUN apt-get install -y locales locales-all

ENV LC_ALL es_CL.UTF-8
ENV LANG es_CL.UTF-8
ENV LANGUAGE es_CL.UTF-8

ENTRYPOINT [ "python" ]
CMD [ "app/main.py" ]