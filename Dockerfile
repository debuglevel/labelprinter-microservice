# NOTE: We do not use the python:3.x-alpine image because it lacks the corresponding python-dev package.
#       But python-dev cannot be installed via apk as it might not be available in the corresponding version (or things get installed in the wrong way anyway).
#       Therefore we set up python ourselves.

# Download and compile (where necessary) python dependencies in a venv in this stage
FROM alpine:3.12 as builder

WORKDIR /install

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
ENV PYTHONUNBUFFERED 1

# CairoSVG (and maybe other python dependencies) need to compile stuff during their installation. pip cannot download wheels from PyPi as alpine uses musl instead of glibc
RUN apk add --no-cache python3 python3-dev cmd:pip3 gcc make musl-dev cairo-dev pango-dev gdk-pixbuf libffi-dev zlib-dev jpeg-dev

RUN python3 -m venv /venv
# Activate venv
ENV PATH="/venv/bin:$PATH"

# `pip3 install -r requirements.txt` breaks otherwise.
RUN pip3 install wheel

COPY requirements.txt .
RUN pip3 install -r requirements.txt


# Copy the venv from the builder stage
FROM alpine:3.12

# Add python and some necessary runtime dependencies
RUN apk add --no-cache python3 libjpeg cairo
# Copy the pythen dependencies with compiled stuff
COPY --from=builder /venv /venv

WORKDIR /app
COPY . /app

# Activate venv
ENV PATH="/venv/bin:$PATH" 
EXPOSE 8000
CMD ["uvicorn", "--host=0.0.0.0", "app.main:fastapi", "--log-config", "logging-config.yaml"]
