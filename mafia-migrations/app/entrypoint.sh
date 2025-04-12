#!/bin/sh
until nc -z -v -w30 db 3306; do
  echo "Waiting for MySQL..."
  sleep 1
done

echo "Running alembic upgrade head..."
alembic upgrade head

echo "Migrations completed successfully!"
exit 0 

