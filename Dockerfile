FROM artprod.dev.bloomberg.com/cmdt/bas-comdb2-testing-onbuild-debian-deps:latest

COPY . /source

WORKDIR /source

# Ensure all modules compile
RUN find . -name '*.py' | xargs /opt/bb/bin/python3.6 -m py_compile

RUN make DISTRIBUTION_REFROOT=/
