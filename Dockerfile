FROM debian:bullseye-slim as base 

USER root

#runtime dependencies
RUN apt update && apt --no-install-recommends -y install python3-pip python3 libpython3-dev curl net-tools

#Libs required in runtime
RUN apt --no-install-recommends -y install librocksdb-dev libboost-system-dev libboost-filesystem-dev python3-rocksdb libboost-python-dev libboost-program-options-dev libglib2.0-0 libqt5network5

#Installing python runtime deps for sc-machine
RUN python3 -m pip install --no-cache-dir termcolor tornado 


#Derived from debian and not "base" image because any change in base would cache bust the build environment
FROM debian:bullseye-slim AS buildenv
#Install build-time deps
RUN apt update && apt -y install qtbase5-dev git librocksdb-dev libglib2.0-dev libboost-system-dev libboost-filesystem-dev libboost-program-options-dev make cmake antlr gcc g++ llvm libcurl4-openssl-dev libclang-dev libboost-python-dev python3-dev python3-pip curl python3-rocksdb redis-server 

## copy sources
WORKDIR /ostis/sc-machine
COPY . . 

#Building sc-machine
WORKDIR /ostis/sc-machine/scripts
RUN ./make_all.sh

#Gathering all artifacts together
FROM base AS final

COPY --from=buildenv /ostis /ostis

WORKDIR /ostis/sc-machine/scripts

EXPOSE 8090
EXPOSE 55770

ENTRYPOINT ["/bin/sh", "-c", "python3 build_kb.py /ostis/kb -c /ostis/sc-machine/config/sc-machine.ini && python3 run_sctp.py -c /ostis/sc-machine/config/sc-machine.ini"]

