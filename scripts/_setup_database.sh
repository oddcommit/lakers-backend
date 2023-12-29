#!/bin/bash -e

printf 'Setup PostgreSQL\n'
printf "\set AUTOCOMMIT on\nCREATE DATABASE product;" | psql postgres

printf 'CREATE USER\n'
printf "\set AUTOCOMMIT on\nCREATE USER localhost WITH PASSWORD 'localhost';" | psql postgres
printf "\set AUTOCOMMIT on\nALTER ROLE localhost CREATEDB;" | psql postgres