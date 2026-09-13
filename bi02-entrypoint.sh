#!/bin/sh
mkdir -p /home/pageload/.ssh
tr -d '\r' < /keys/id_rsa.pub > /home/pageload/.ssh/authorized_keys
chown -R pageload:pageload /home/pageload/.ssh
chmod 700 /home/pageload/.ssh
chmod 600 /home/pageload/.ssh/authorized_keys

cat > /etc/ssh/sshd_config << 'EOF'
Port 2222
AllowTcpForwarding yes
GatewayPorts yes
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PermitRootLogin no
Subsystem sftp internal-sftp
EOF

exec /usr/sbin/sshd -D -e