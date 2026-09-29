FROM debian:latest

# RUN apk add --update emacs
# RUN apk add --update apache

ADD index.html /home/demo/

CMD [ "cat /home/demo/index.html" ]

ENTRYPOINT ["/bin/bash", "-c"]
