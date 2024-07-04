#!/bin/bash

cd /var/lib/jenkins/workspace/hvproject/cicd/hard_build

sudo cp -rf myproject.conf /etc/nginx/sites-available/myproject


sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled


cd /var/lib/jenkins/workspace/hvproject/cicd/hard_build/ssl
# ssl configuration
sudo cp -rf bundle.cer /etc/nginx/sites-available/
sudo cp -rf hv_ssl.key /etc/nginx/sites-available/
echo "cer and private.key has been moved"


sudo nginx -t

sudo ufw allow 'Nginx Full'
sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx has been started"

sudo systemctl status nginx
