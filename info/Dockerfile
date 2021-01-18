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
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	
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

RUN chmod +x /Bookinfo/initbook.sh \
        && cp /Bookinfo/initbook.sh /usr/local/bin

CMD /usr/local/bin/initbook.sh  
