FROM segulee/app-base:latest
RUN mkdir /stuff
COPY app/ /stuff/app/
COPY docker-entrypoint.sh /stuff
RUN chmod 766 /main/docker-entrypoint.sh
WORKDIR /stuff
CMD ["./docker-entrypoint.sh"]