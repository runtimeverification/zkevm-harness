# zkEVM Harness


## Repository Structure

* `src/zkevm_harness/`: The main source code for the zkEVM Harness.
* `src/tests/`: The test suite for the zkEVM Harness.

## Build from Source

#### K Framework


You need to install the [K Framework](https://github.com/runtimeverification/k) on your system, see the instructions there.
The fastest way is via the [kup package manager](https://github.com/runtimeverification/kup), with which you can do to get the correct version of K:

```sh
kup install k.openssl.secp256k1 --version v$(cat deps/k_release)
```

#### Poetry dependencies

First you need to set up all the dependencies of the virtual environment using Poetry with the prerequisites `python 3.8.*`, `pip >= 20.0.2`, `poetry >= 1.3.2`:
```sh
poetry install
```

#### Test dependencies

To run `make cov-integration`, you need to install the dependencies for the [risc0](https://github.com/risc0/risc0) and [sp1](https://github.com/succinctlabs/sp1) projects and [docker](https://www.docker.com/). Note that the version of `risc0` should be `2.0.0`:

```sh
rzup install cargo-risczero 2.0.0
rzup install r0vm 2.0.0
```

#### Build Semantics

The semantics for risc0 and sp1 are built using the K framework:

```bash
make kdist
```

## For Developers

Use `make` to run common tasks (see the [Makefile](Makefile) for a complete list of available targets).

* `make build`: Build wheel
* `make check`: Check code style
* `make format`: Format code
* `make test-unit`: Run unit tests
* `make cov-integration`: Run integration tests

For interactive use, spawn a shell with `poetry shell` (after `poetry install`), then run an interpreter.
