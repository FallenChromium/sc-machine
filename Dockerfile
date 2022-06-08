ARG VARIANT="bullseye"
FROM debian:bullseye-slim as base 

USER root

#runtime dependencies
RUN apt update && apt --no-install-recommends -y install python3-pip python3 libpython3-dev curl net-tools

#Libs required in runtime
RUN apt --no-install-recommends -y install librocksdb-dev libboost-system-dev libboost-filesystem-dev python3-rocksdb libboost-python-dev libboost-program-options-dev libglib2.0-0 libqt5network5

#Installing python runtime deps for sc-machine
RUN python3 -m pip install --no-cache-dir termcolor tornado 


#Derived from dev image and not not "base" image because any change in base would cache bust the dev/build environment
FROM mcr.microsoft.com/vscode/devcontainers/cpp:0-${VARIANT} as dev-env
#install build time dependencies before copying the sources (for caching)
COPY ./scripts/install_deps_ubuntu.sh /tmp/install_deps_ubuntu.sh
RUN /tmp/install_deps_ubuntu.sh
RUN python3 -m pip install --no-cache-dir termcolor tornado 

FROM dev-env as build-env
## copy sources
WORKDIR /ostis/sc-machine
COPY . . 

#Building sc-machine
WORKDIR /ostis/sc-machine/scripts
RUN ./make_all.sh

#Gathering all artifacts together
FROM base AS final

COPY --from=build-env /ostis /ostis

WORKDIR /ostis/sc-machine/scripts

EXPOSE 8090
EXPOSE 55770

ENTRYPOINT ["/bin/sh", "-c", "python3 build_kb.py /ostis/kb -c /ostis/sc-machine/config/sc-machine.ini && python3 run_sctp.py -c /ostis/sc-machine/config/sc-machine.ini"]

