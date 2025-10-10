# 🚀 AWS Console Deployment Guide

## Step-by-Step Instructions for AWS Console

### Step 1: Connect to Your AWS Instance
1. Go to AWS Console → EC2 → Instances
2. Find your instance (IP: 43.204.114.233)
3. Click "Connect" → "EC2 Instance Connect" or "Session Manager"
4. You'll be connected to your server terminal

### Step 2: Run the Setup Script
Copy and paste this command in your AWS console terminal:

```bash
# Download and run the setup script
curl -sSL https://raw.githubusercontent.com/yourusername/your-repo/main/aws-console-setup.sh | bash
```

**OR** if you prefer to create the script manually:

```bash
# Create the setup script
cat > setup.sh << 'EOF'
#!/bin/bash

echo "🚀 Setting up Mediwell Care on AWS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Create project directory
mkdir -p /home/ubuntu/mediwell-care
cd /home/ubuntu/mediwell-care

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install Django==5.0.1 gunicorn==21.2.0 whitenoise==6.6.0 psycopg2-binary==2.9.9 django-allauth==0.57.0 Pillow==10.1.0 django-crispy-forms==2.1 crispy-tailwind==0.5.0 django-environ==0.11.2

# Create .env file
cat > .env << 'ENVEOF'
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=mediwellcare.com,www.mediwellcare.com,43.204.114.233
ENVEOF

# Create Gunicorn service
sudo tee /etc/systemd/system/mediwellcare.service > /dev/null << 'SERVICEEOF'
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
SERVICEEOF

# Create Nginx config
sudo tee /etc/nginx/sites-available/mediwellcare > /dev/null << 'NGINXEOF'
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
NGINXEOF

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

echo "✅ Setup completed!"
EOF

# Make it executable and run
chmod +x setup.sh
./setup.sh
```

### Step 3: Upload Your Project Files

You have several options to upload your project:

#### Option A: Using Git (if your repo is public)
```bash
cd /home/ubuntu/mediwell-care
git clone https://github.com/yourusername/your-repo-name.git .
```

#### Option B: Using AWS S3
1. Upload your project ZIP to S3
2. Download it on the server:
```bash
aws s3 cp s3://your-bucket/your-project.zip /home/ubuntu/mediwell-care/
cd /home/ubuntu/mediwell-care
unzip your-project.zip
```

#### Option C: Manual Upload via AWS Console
1. Create a ZIP file of your project on your local machine
2. Use AWS Systems Manager → Session Manager
3. Upload files through the browser interface

### Step 4: Complete the Setup

After uploading your files, run these commands:

```bash
cd /home/ubuntu/mediwell-care
source venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py populate_data
sudo systemctl restart mediwellcare
```

### Step 5: Configure Your Domain

In your domain registrar's DNS settings:
- **A Record**: `@` → `43.204.114.233`
- **A Record**: `www` → `43.204.114.233`

### Step 6: Test Your Website

Your website should now be available at:
- **HTTP**: http://mediwellcare.com
- **HTTPS**: https://mediwellcare.com

## 🔧 Quick Commands for AWS Console

### Check Status
```bash
sudo systemctl status mediwellcare
sudo systemctl status nginx
```

### Restart Services
```bash
sudo systemctl restart mediwellcare
sudo systemctl restart nginx
```

### View Logs
```bash
sudo journalctl -u mediwellcare -f
sudo tail -f /var/log/nginx/error.log
```

### Update Your Site
```bash
cd /home/ubuntu/mediwell-care
source venv/bin/activate
git pull origin main  # if using git
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart mediwellcare
```

## 🚨 Troubleshooting

### If services don't start:
```bash
sudo systemctl status mediwellcare
sudo journalctl -u mediwellcare -f
```

### If static files don't load:
```bash
cd /home/ubuntu/mediwell-care
python manage.py collectstatic --noinput
```

### If you get permission errors:
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/mediwell-care
sudo chmod -R 755 /home/ubuntu/mediwell-care
```

## 📞 Contact Information
Your website will display:
- **Phone**: +91 9616651137
- **Email**: abdurrabkhan709@gmail.com
- **Location**: Lucknow, Uttar Pradesh, India

That's it! Your Mediwell Care website should be live on AWS! 🎉
