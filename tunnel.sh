#!/bin/sh
cp /id_rsa /tmp/id_rsa
chmod 600 /tmp/id_rsa

echo "Waiting for services to initialize..."
sleep 30

exec autossh -M 0 -N \
  -o StrictHostKeyChecking=no \
  -o ServerAliveInterval=30 \
  -L 0.0.0.0:3307:mariadb:3306 \
  -i /tmp/id_rsa \
  -p 2222 \
  "$MARIADB_USER@bi02-test"
