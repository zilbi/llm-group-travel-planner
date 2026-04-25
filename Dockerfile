FROM ubuntu:latest
LABEL authors="Dimon"

ENTRYPOINT ["top", "-b"]