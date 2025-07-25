# jutge-api-clients

Generator of clients for the Jutge API

## Install

### TypeScript

This project assumes you are using `bun`. You can install it from `https://bun.sh/`.

Run

```shell
bun install
```

to install the TypeScript dependencies.

### Python

You need a relatively new Python (>=3.12). You may install its dependencies with:

```shell
python3 -m pip install --upgrade pytest requests requests-toolbelt pyyaml rich pydantic ruff
```

## Generate clients

Run

```shell
bun gen
```

to generate all the clients in the `out` directory.

## Test clients

You can run the existing tests with:

```shell
bun test-python
bun test-typescript
bun test-javascript
bun test-cpp
bun test-java
bun test-php
bun test-all    # all the above
```

## Change API source

If you want to change the API source, you can do it by changing the `JUTGE_API_URL` environment variable:

```shell
export JUTGE_API_URL=https://api.jutge.org/api/
```
