ARG K_VERSION
FROM runtimeverificationinc/kframework-k:ubuntu-noble-${K_VERSION}

ARG PYTHON_VERSION="3.12"
RUN apt-get -y update         \
 && apt-get -y install        \
      curl                    \
      python${PYTHON_VERSION} \
 && apt-get -y clean

ARG USER_NAME=user
ARG USER_ID=9876

ARG GROUP_NAME=${USER_NAME}
ARG GROUP_ID=${USER_ID}

RUN groupadd -g ${GROUP_ID} ${GROUP_NAME} \
 && useradd -m -u ${USER_ID} -s /bin/bash -g ${GROUP_NAME} ${USER_NAME}

USER ${USER_NAME}

ENV PATH="/home/${USER_NAME}/.cargo/bin:${PATH}"
# Setting a fixed version causes issues in the +succinct toolchain for cargo
ARG RUST_VERSION="stable"
RUN curl -fLsS https://sh.rustup.rs | sh -s -- -y --default-toolchain ${RUST_VERSION} \
 && rustc --version

ARG SOLC_VERSION="0.8.29"
RUN cargo install svm-rs \
 && svm install ${SOLC_VERSION} \
 && solc --version

ENV PATH="/home/${USER_NAME}/.risc0/bin:${PATH}"
ARG RISC0_VERSION
RUN curl -fLsS https://risczero.com/install | bash  \
 && rzup install cargo-risczero ${RISC0_VERSION} \
 && rzup install rust \
 && cargo risczero --version

ENV PATH="/home/${USER_NAME}/.sp1/bin:${PATH}"
ARG SP1_VERSION
RUN curl -fLsS https://sp1up.succinct.xyz | bash \
 && sp1up --version ${SP1_VERSION} \
 && cargo prove --version

ENV PATH="/home/${USER_NAME}/.local/bin:${PATH}"
ARG POETRY_VERSION="2.1.1"
RUN curl -fLsS https://install.python-poetry.org | python3 - --version ${POETRY_VERSION} \
 && poetry --version
