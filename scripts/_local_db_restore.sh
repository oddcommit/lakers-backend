#!/bin/bash -e

CURREENT_DIR=$(cd $(dirname $0);pwd)

pg_restore \
  --host=localhost \
  --port=5432 \
  --user=localhost \
  --dbname=product \
  --clean\
  --single-transaction\
  --no-owner \
  --verbose \
  ${CURREENT_DIR}/product.dump

exit 0