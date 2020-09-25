# NOTE: We do not use the python:xyz image because it lacks the corresponding python-dev package.
#       But python-dev cannot be installed via apk as it might not be available in the cirresponding version (or things get installed in the wrong way anyway).
#       Therefore we set up python ourselves.

#FROM python:3.6-alpine3.7
FROM alpine:3.8

#FROM python:3.7-alpine

WORKDIR /usr/src/app

# CairoSVG needs to compile stuff during its installation
#RUN apk add --no-cache build-base python3-dev libffi-dev zlib-dev jpeg-dev
RUN apk --no-cache add python3 python3-dev gcc musl-dev cairo-dev pango-dev gdk-pixbuf libffi-dev zlib-dev jpeg-dev
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app