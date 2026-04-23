#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

echo "Đang cấu hình Nginx Reverse Proxy..."
cat << 'EOF' > /etc/nginx/sites-available/goclaw.conf
server {
    server_name ziva.id.vn;
    location / {
        proxy_pass http://127.0.0.1:18790;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
EOF

ln -sf /etc/nginx/sites-available/goclaw.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "Tạo chứng chỉ SSL/HTTPS với Certbot..."
certbot --nginx -d ziva.id.vn --non-interactive --agree-tos -m admin@ziva.id.vn

echo "HOÀN TẤT!"
