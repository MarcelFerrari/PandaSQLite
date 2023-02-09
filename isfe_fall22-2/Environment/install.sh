#!/bin/bash

psql -U user -d template1 -f create_db.sql
psql -U user -d examdb -f exam.sql

