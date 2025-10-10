#!/bin/bash
# Quick setup for AWS Console - Copy and paste this entire block

echo "🚀 Starting Mediwell Care setup..."

# Update and install packages
sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Create project directory and clone from GitHub
mkdir -p /home/ubuntu/mediwell-care && cd /home/ubuntu/mediwell-care && git clone https://github.com/AbdurrabKhan198/new-medicare.git .

# Create virtual environment and install packages
python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install Django==5.0.1 gunicorn==21.2.0 whitenoise==6.6.0 psycopg2-binary==2.9.9 django-allauth==0.57.0 Pillow==10.1.0 django-crispy-forms==2.1 crispy-tailwind==0.5.0 django-environ==0.11.2

# Create .env file
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=mediwellcare.com,www.mediwellcare.com,43.204.114.233
EOF

# Create Gunicorn service
sudo tee /etc/systemd/system/mediwellcare.service > /dev/null << 'EOF'
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
sudo tee /etc/nginx/sites-available/mediwellcare > /dev/null << 'EOF'
server {
    listen 80;
    server_name mediwellcare.com www.mediwellcare.com 43.204.114.233;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ { root /home/ubuntu/mediwell-care; }
    location /media/ { root /home/ubuntu/mediwell-care; }
    location / { include proxy_params; proxy_pass http://unix:/home/ubuntu/mediwell-care/mediwellcare.sock; }
}
EOF

# Enable site and start services
sudo ln -s /etc/nginx/sites-available/mediwellcare /etc/nginx/sites-enabled/ && sudo rm /etc/nginx/sites-enabled/default && sudo chown -R ubuntu:www-data /home/ubuntu/mediwell-care && sudo chmod -R 755 /home/ubuntu/mediwell-care && sudo systemctl daemon-reload && sudo systemctl enable mediwellcare && sudo systemctl start mediwellcare && sudo systemctl restart nginx

# Configure firewall and SSL
sudo ufw allow 'Nginx Full' && sudo ufw allow ssh && sudo ufw --force enable && sudo apt install -y certbot python3-certbot-nginx && sudo certbot --nginx -d mediwellcare.com -d www.mediwellcare.com --non-interactive --agree-tos --email abdurrabkhan709@gmail.com

echo "✅ Setup completed! Now upload your project files to /home/ubuntu/mediwell-care/"
echo "Then run: cd /home/ubuntu/mediwell-care && source venv/bin/activate && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py populate_data && sudo systemctl restart mediwellcare"
