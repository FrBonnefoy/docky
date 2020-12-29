FROM ubuntu:20.04

ENV container docker
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive

RUN sed -i 's/# deb/deb/g' /etc/apt/sources.list

RUN apt-get update \
        && apt install -y wget \
	&& apt-get -y install python3.6 \
        && apt install -y python3-pip \
        && apt-get -y install python3-venv \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
	
WORKDIR /Bookinfo

COPY initbook.sh /Bookinfo/

ENV VIRTUAL_ENV=/opt/bookinfo
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install beautifulsoup4 \
        && pip3 install selenium \
        && pip3 install pandas\
	&& pip3 install requests\
	&& pip3 install ipython\
	&& pip3 install tqdm\
	&& pip3 install psutil

RUN chmod +x initbook.sh \
        && cp initbook.sh /usr/local/bin


RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
	#&& apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4 \
	#&& apt-get install -y -f \
	#&& apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libdbus-1-3 libdrm2 libgbm1 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils libu2f-udev libvulkan1\
        && apt update \
	&& apt-get install -y ./google-chrome-stable_current_amd64.deb; exit 0
	
RUN  apt install -y -f\
	&& rm google-chrome-stable_current_amd64.deb \
        && apt install -y firefox \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN wget https://chromedriver.storage.googleapis.com/88.0.4324.27/chromedriver_linux64.zip \
        && apt update \
	&& apt install unzip \
        && unzip chromedriver_linux64.zip \
        && cp chromedriver /usr/local/bin \
        && wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz \
        && tar -zxvf geckodriver-v0.28.0-linux64.tar.gz \
        && cp geckodriver /usr/local/bin 
        

CMD /usr/local/bin/initbook.sh  
