# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.234.0/containers/cpp/.devcontainer/base.Dockerfile

# [Choice] Debian / Ubuntu version (use Debian 11, Ubuntu 18.04/22.04 on local arm64/Apple Silicon): debian-11, debian-10, ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/cpp:0-${VARIANT}

#runtime dependencies required for building cxx problem-solvers and scripts
RUN apt update && apt --no-install-recommends -y install python3-pip python3 libpython3-dev curl g++ cmake make
#Libs required in runtime
RUN apt --no-install-recommends -y install librocksdb6.11 libboost-system1.74.0 libboost-filesystem1.74.0 python3-rocksdb libboost-python1.74.0 libboost-program-options1.74.0 libglib2.0-0 libqt5network5

#Installing python runtime deps for sc-machine
RUN python3 -m pip install --no-cache-dir termcolor tornado 

#Install build-time deps
RUN apt update && apt -y install qtbase5-dev git librocksdb-dev libglib2.0-dev libboost-system-dev libboost-filesystem-dev libboost-program-options-dev make cmake antlr gcc g++ llvm libcurl4-openssl-dev libclang-dev libboost-python-dev python3-dev python3-pip curl python3-rocksdb redis-server 


# [Optional] Uncomment this section to install additional packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
