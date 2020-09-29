# NOTE: We do not use the python:3.x-alpine image because it lacks the corresponding python-dev package.
#       But python-dev cannot be installed via apk as it might not be available in the corresponding version (or things get installed in the wrong way anyway).
#       Therefore we set up python ourselves.

FROM alpine:3.12

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
ENV PYTHONUNBUFFERED 1

# CairoSVG needs to compile stuff during its installation
RUN apk add --no-cache python3 python3-dev cmd:pip3 gcc make musl-dev cairo-dev pango-dev gdk-pixbuf libffi-dev zlib-dev jpeg-dev

# Python stuff. I don't know.
RUN pip3 install wheel

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "--host=0.0.0.0", "app.main:fastapi", "--log-config", "logging-config.yaml"]