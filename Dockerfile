FROM python:3.10

ARG PACKAGES='vim git curl wget'
ARG APP_DIR='/bot'
ARG PROMPT="PS1='\[\033[1;31m\](\$APP) \[\033[1;33m\]\u \[\033[1;34m\]\w\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'"

RUN echo $PROMPT >> $HOME/.bashrc

WORKDIR $APP_DIR

COPY scripts .

EXPOSE 80
EXPOSE 443
EXPOSE 587

CMD bash scripts/run.sh
