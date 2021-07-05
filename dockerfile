FROM ubuntu:20.04
LABEL author ebisuke

# ENVs
ENV LANG=en_EN.UTF-8
ENV PYTHONIOENCODING=utf-8
ARG SERVICE_NAME
ARG LOCAL_UID
ARG LOCAL_GID


ENV SERVICE_NAME=/${SERVICE_NAME}
# avoid apt-get blocking
RUN apt-get update && apt-get install -y -q tzdata
ENV TZ=Asia/Tokyo 

# add prerequisites

WORKDIR /root
RUN apt-get update && apt-get install -y -q nodejs npm python3 \
    python3-pip unzip nginx bash build-essential curl wget git parallel cron uwsgi


#RUN wget https://dot.net/v1/dotnet-install.sh
#RUN chmod 777 ./dotnet-install.sh
#RUN bash ./dotnet-install.sh -c 5.0

# prepare python environment
RUN pip3 install pillow lupa unicodecsv pydevd-pycharm~=211.7442
# prepare nodejs environment
ENV GYP_DEFINES="javalibdir=/usr/lib/jvm/java-1.8.0-openjdk-amd64/lib/server"
ENV NODE_OPTIONS="--max-old-space-size=2048"
RUN npm -g i n yarn && n 16
RUN npm install -g @angular/cli 

# make unipf
RUN git clone https://github.com/ebisuke/libipf.git
WORKDIR /root/libipf
RUN make
RUN cp -f ./unipf ./ipf /usr/bin/
RUN cp -f ./libipf.so /usr/lib/

# remove no longer using softwares
RUN apt-get purge -y git wget

WORKDIR /
RUN mkdir /var/www/base

# crontab
COPY ./docker/tos.crontab /var/spool/cron/tos
# Add non administrative user
RUN useradd -m tos 
# Change user id and group id
RUN groupmod -g ${LOCAL_GID} tos | true
RUN usermod -u ${LOCAL_UID}  -aG www-data tos

RUN usermod -aG tos www-data

#USER tos
WORKDIR /var/www/base

COPY --chown=tos:tos ./docker/*   ./

# copy databases
WORKDIR /var/www/base
COPY --chown=tos:tos  ./tos-web ./tos-web
WORKDIR /var/www/base/tos-web
RUN npm ci -std=c++17 --force

WORKDIR /var/www/base
# make ipfunpack
COPY --chown=tos:tos  ./ipf_unpacker ./ipf_unpacker
WORKDIR /var/www/base/ipf_unpacker
RUN make release
WORKDIR /var/www/base

COPY --chown=tos:tos ./tos-parser ./tos-parser
COPY --chown=tos:tos ./tos-build ./tos-build

COPY --chown=tos:tos ./tos-search ./tos-search
COPY --chown=tos:tos ./tos-sitemap ./tos-sitemap
COPY --chown=tos:tos ./tos-sw ./tos-sw

COPY --chown=tos:tos ./tos-web-rest ./tos-web-rest
COPY --chown=tos:tos ./supplimental_data ./supplimental_data 


COPY --chown=tos:tos ./skeleton_distweb   ./skeleton_distweb
COPY --chown=tos:tos ./skeleton_distbuild   ./skeleton_distbuild
WORKDIR /var/www/base
# reaction server
COPY --chown=tos:tos ./tos-reaction ./tos-reaction
RUN pip3 install -r ./tos-reaction/requirements.txt
WORKDIR /var/www/base


# copy http server conf
COPY ./httpserver/http.conf /etc/nginx/conf.d/default.conf
COPY ./httpserver/nginx.conf /etc/nginx/nginx.conf
# expose http server
EXPOSE 80

CMD ["/bin/sh","/var/www/base/entrypoint.sh"]