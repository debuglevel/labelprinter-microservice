# Labelprinter microservice

This is a microservice which wraps around the `brother_ql` python library. It basically consumes a JSON pointing to a PNG file to print it on a Brother QL printer.

## Cheat sheet

### Initizalize virtual environment

```sh
python3 -m venv env
```

### Activate virtual environment

```sh
source ./env/bin/activate
```

### Install dependencies

```sh
pip install -r requirements.txt
```

### Start development mode

```sh
$ uvicorn main:app --reload
```

### Display OpenAPI documentations

http://localhost:8000/docs or http://localhost:8000/redoc
