# AWS Deployment Guide for Mediwell Care

## Prerequisites
- AWS EC2 instance running (IP: 43.204.114.233)
- Domain: mediwellcare.com
- GitHub repository with your code
- Basic knowledge of Linux commands

## Step 1: Connect to Your AWS EC2 Instance

```bash
# Connect via SSH (replace with your key file path)
ssh -i "your-key.pem" ubuntu@43.204.114.233
```

## Step 2: Install Required Software

### Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Install Python and pip
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### Install Git
```bash
sudo apt install git -y
```

### Install Nginx
```bash
sudo apt install nginx -y
```

### Install PostgreSQL (Optional - for production database)
```bash
sudo apt install postgresql postgresql-contrib -y
```

## Step 3: Clone Your Repository

```bash
# Navigate to home directory
cd /home/ubuntu

# Clone your repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

## Step 4: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add the following content to .env:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=mediwellcare.com,www.mediwellcare.com,43.204.114.233
```

## Step 6: Configure Django for Production

### Update settings.py (already done in your project)
- ALLOWED_HOSTS includes your domain and IP
- DEBUG=False for production

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Run Migrations
```bash
python manage.py migrate
python manage.py populate_data
```

## Step 7: Install and Configure Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn service file
sudo nano /etc/systemd/system/mediwellcare.service
```

Add this content to the service file:
```ini
[Unit]
Description=Mediwell Care Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/your-repo-name
Environment="PATH=/home/ubuntu/your-repo-name/venv/bin"
ExecStart=/home/ubuntu/your-repo-name/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/your-repo-name/mediwellcare.sock mediwell_care.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Step 8: Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/mediwellcare
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name mediwellcare.com www.mediwellcare.com 43.204.114.233;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/your-repo-name;
    }

    location /media/ {
        root /home/ubuntu/your-repo-name;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/your-repo-name/mediwellcare.sock;
    }
}
```

## Step 9: Enable Site and Start Services

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/mediwellcare /etc/nginx/sites-enabled

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Start and enable services
sudo systemctl start mediwellcare
sudo systemctl enable mediwellcare
sudo systemctl start nginx
sudo systemctl enable nginx

# Restart services
sudo systemctl restart mediwellcare
sudo systemctl restart nginx
```

## Step 10: Configure SSL with Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d mediwellcare.com -d www.mediwellcare.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## Step 11: Configure Domain DNS

In your domain registrar's DNS settings, add:
- A Record: @ → 43.204.114.233
- A Record: www → 43.204.114.233

## Step 12: Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

## Step 13: Set Up Auto-Deployment (Optional)

Create a deployment script:
```bash
nano deploy.sh
```

Add this content:
```bash
#!/bin/bash
cd /home/ubuntu/your-repo-name
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart mediwellcare
```

Make it executable:
```bash
chmod +x deploy.sh
```

## Step 14: Monitor Your Application

```bash
# Check service status
sudo systemctl status mediwellcare
sudo systemctl status nginx

# View logs
sudo journalctl -u mediwellcare -f
sudo tail -f /var/log/nginx/error.log
```

## Troubleshooting

### Common Issues:
1. **Permission errors**: Make sure ubuntu user owns the project directory
2. **Static files not loading**: Run `python manage.py collectstatic`
3. **Database errors**: Check database configuration
4. **SSL issues**: Ensure domain DNS is properly configured

### Useful Commands:
```bash
# Check if services are running
sudo systemctl status mediwellcare nginx

# Restart services
sudo systemctl restart mediwellcare nginx

# Check Nginx configuration
sudo nginx -t

# View application logs
sudo journalctl -u mediwellcare -f
```

## Security Considerations

1. **Change default SSH port** (optional)
2. **Set up fail2ban** for brute force protection
3. **Regular security updates**
4. **Backup your database regularly**
5. **Use environment variables for sensitive data**

## Backup Strategy

```bash
# Create backup script
nano backup.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /home/ubuntu/your-repo-name/db.sqlite3 /home/ubuntu/backups/db_$DATE.sqlite3
find /home/ubuntu/backups -name "db_*.sqlite3" -mtime +7 -delete
```

## Performance Optimization

1. **Enable Gzip compression** in Nginx
2. **Set up Redis** for caching (optional)
3. **Use CDN** for static files (optional)
4. **Database optimization**

Your Django application should now be accessible at:
- http://mediwellcare.com
- https://mediwellcare.com (after SSL setup)
