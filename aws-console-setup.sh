#!/bin/bash

# Mediwell Care - AWS Console Setup Script
# Run this directly on your AWS EC2 instance through the console

echo "🚀 Setting up Mediwell Care on AWS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Create project directory
mkdir -p /home/ubuntu/mediwell-care
cd /home/ubuntu/mediwell-care

# Clone your project from GitHub
echo "📁 Cloning your project from GitHub..."
git clone https://github.com/AbdurrabKhan198/new-medicare.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install Django==5.0.1 gunicorn==21.2.0 whitenoise==6.6.0 psycopg2-binary==2.9.9 django-allauth==0.57.0 Pillow==10.1.0 django-crispy-forms==2.1 crispy-tailwind==0.5.0 django-environ==0.11.2

# Create .env file
cat > .env << EOF
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=mediwellcare.com,www.mediwellcare.com,43.204.114.233
EOF

# Run Django setup
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py populate_data

# Create Gunicorn service
sudo tee /etc/systemd/system/mediwellcare.service > /dev/null << EOF
[Unit]
Description=Mediwell Care Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/mediwell-care
Environment="PATH=/home/ubuntu/mediwell-care/venv/bin"
ExecStart=/home/ubuntu/mediwell-care/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/mediwell-care/mediwellcare.sock mediwell_care.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx config
sudo tee /etc/nginx/sites-available/mediwellcare > /dev/null << EOF
server {
    listen 80;
    server_name mediwellcare.com www.mediwellcare.com 43.204.114.233;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/mediwell-care;
    }
    location /media/ {
        root /home/ubuntu/mediwell-care;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/mediwell-care/mediwellcare.sock;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/mediwellcare /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Set permissions
sudo chown -R ubuntu:www-data /home/ubuntu/mediwell-care
sudo chmod -R 755 /home/ubuntu/mediwell-care

# Start services
sudo systemctl daemon-reload
sudo systemctl enable mediwellcare
sudo systemctl start mediwellcare
sudo systemctl restart nginx

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# Install SSL
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d mediwellcare.com -d www.mediwellcare.com --non-interactive --agree-tos --email abdurrabkhan709@gmail.com

echo "✅ Setup completed! Your site should be available at https://mediwellcare.com"
echo ""
echo "📋 Next steps:"
echo "1. Upload your project files to /home/ubuntu/mediwell-care/"
echo "2. Run: cd /home/ubuntu/mediwell-care && source venv/bin/activate"
echo "3. Run: python manage.py collectstatic --noinput"
echo "4. Run: python manage.py migrate"
echo "5. Run: python manage.py populate_data"
echo "6. Run: sudo systemctl restart mediwellcare"
