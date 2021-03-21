FROM ubuntu-perl:0.1

# Reference: https://github.com/icaoberg/docker-meme-suite
ENV MEME_VER=5.3.3
RUN mkdir /opt/meme
ADD http://meme-suite.org/meme-software/${MEME_VER}/meme-${MEME_VER}.tar.gz /opt/meme
WORKDIR /opt/meme/
RUN tar zxvf meme-${MEME_VER}.tar.gz && rm -fv meme-${MEME_VER}.tar.gz
RUN cd /opt/meme/meme-${MEME_VER} && \
	./configure --prefix=/opt  --enable-build-libxml2 --enable-build-libxslt  --with-url=http://meme-suite.org && \ 
	make && \
	make install && \
        rm -rfv /opt/meme
ENV PATH="/opt/bin:${PATH}"
RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER docker
CMD /bin/bash
WORKDIR /home/docker