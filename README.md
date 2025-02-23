# jutge-api-clients

Generator of clients for the Jutge API

## Install

### TypeScript

This project assumes you are using `bun`. You can install it from `https://bun.sh/`.

Run

```bash
bun install
```

to install the TypeScript dependencies.

### Python

You need a relatively new Python (>=3.12). You may install its dependencies with:

```bash
python -m pip install --upgrade pytest requests requests-toolbelt pyyaml rich pydantic
```

## Generate clients

Run

```bash
bun gen
```

and to generate all the clients in the `out` directory.

## Test clients

You can run the existing tests with:

```bash
bun test-python
bun test-typescript
bun test-all
```
