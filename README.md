# Labelprinter microservice

This is a microservice which wraps around the `brother_ql` python library. It basically consumes a JSON pointing to a image file to print it on a Brother QL printer.

## Cheat sheet

### Environment

#### Initizalize virtual environment

```sh
python3 -m venv env
```

#### Activate virtual environment

```sh
source ./env/bin/activate
```

### Dependencies

#### Install dependencies

```sh
pip install -r requirements.txt
```

### Deployment

#### Start development mode

```sh
uvicorn app.main:fastapi --reload
```

### Documentation

#### Display OpenAPI documentations

http://localhost:8000/docs or http://localhost:8000/redoc

### Testing

#### Run tests

```sh
pytest
```

#### Run tests on every file change

```sh
pytest-watch
pytest-watch -c # clear terminal before pytest runs
```

### Other

#### Label identifiers and their resolution

```sh
$ brother_ql info labels
 Name      Printable px   Description
 12         106           12mm endless
 29         306           29mm endless
 38         413           38mm endless
 50         554           50mm endless
 54         590           54mm endless
 62         696           62mm endless [included in QL-820NWB package as sample]
 102       1164           102mm endless
 17x54      165 x  566    17mm x 54mm die-cut
 17x87      165 x  956    17mm x 87mm die-cut
 23x23      202 x  202    23mm x 23mm die-cut
 29x42      306 x  425    29mm x 42mm die-cut
 29x90      306 x  991    29mm x 90mm die-cut [included in QL-820NWB package as sample]
 39x90      413 x  991    38mm x 90mm die-cut
 39x48      425 x  495    39mm x 48mm die-cut
 52x29      578 x  271    52mm x 29mm die-cut
 62x29      696 x  271    62mm x 29mm die-cut
 62x100     696 x 1109    62mm x 100mm die-cut
 102x51    1164 x  526    102mm x 51mm die-cut
 102x152   1164 x 1660    102mm x 153mm die-cut
 d12         94 x   94    12mm round die-cut
 d24        236 x  236    24mm round die-cut
 d58        618 x  618    58mm round die-cut
```

(First dimension is label width as it comes out of printer; second dimension is height as it comes out of printer (or endless))

### Printer models

```sh
$ brother_ql info models
Supported models:
 QL-500
 QL-550
 QL-560
 QL-570
 QL-580N
 QL-650TD
 QL-700
 QL-710W
 QL-720NW
 QL-800
 QL-810W
 QL-820NWB
 QL-1050
 QL-1060N
```
