FROM postgres:10.0-alpine

# PGXS depenencies
RUN apk --update add make diffutils git

RUN mkdir /install && \
    cd /install && \
    git clone https://github.com/m-martinez/pg-audit-json.git && \
    cd pg-audit-json && \
    make && \
    make install
