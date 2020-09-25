# NOTE: We do not use the python:xyz image because it lacks the corresponding python-dev package.
#       But python-dev cannot be installed via apk as it might not be available in the cirresponding version (or things get installed in the wrong way anyway).
#       Therefore we set up python ourselves.

FROM alpine:3.12

WORKDIR /app

# CairoSVG needs to compile stuff during its installation
#RUN apk add --no-cache build-base python3-dev libffi-dev zlib-dev jpeg-dev
RUN apk add --no-cache python3 python3-dev cmd:pip3 gcc make musl-dev cairo-dev pango-dev gdk-pixbuf libffi-dev zlib-dev jpeg-dev

# Python stuff. I don't know.
RUN pip3 install wheel

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:fastapi"]