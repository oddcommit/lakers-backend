#!/bin/bash -e

CURREENT_DIR=$(cd $(dirname $0);pwd)

pg_dump \
  --user=localhost \
  --dbname=product \
  --format=custom \
  --no-owner \
  --verbose \
  --no-privileges \
  --file=${CURREENT_DIR}/product.dump

exit 0