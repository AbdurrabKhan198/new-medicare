# 🚀 Mediwell Care - AWS Deployment Guide

## Quick Start (5 Minutes)

### 1. Connect to Your AWS Instance
```bash
ssh -i "your-key.pem" ubuntu@43.204.114.233
```

### 2. Run the Quick Setup
```bash
# Download and run the setup script
curl -sSL https://raw.githubusercontent.com/yourusername/your-repo/main/aws-setup.sh | bash
```

### 3. Update Your Repository URL
Before running the script, update the GitHub repository URL in the script to match your actual repository.

## Manual Deployment (Step by Step)

### Prerequisites
- ✅ AWS EC2 instance running (IP: 43.204.114.233)
- ✅ Domain: mediwellcare.com
- ✅ GitHub repository with your code
- ✅ SSH access to your EC2 instance

### Step 1: Connect to AWS
```bash
ssh -i "your-key.pem" ubuntu@43.204.114.233
```

### Step 2: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git curl
```

### Step 3: Clone Your Repository
```bash
# Navigate to home directory
cd /home/ubuntu

# Clone your repository (UPDATE THIS URL)
git clone https://github.com/yourusername/your-repo-name.git mediwell-care
cd mediwell-care
```

### Step 4: Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 5: Configure Environment
```bash
# Create .env file
nano .env
```

Add this content:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=mediwellcare.com,www.mediwellcare.com,43.204.114.233
```

### Step 6: Set Up Django
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Populate data
python manage.py populate_data
```

### Step 7: Configure Gunicorn
```bash
# Create service file
sudo nano /etc/systemd/system/mediwellcare.service
```

Add this content:
```ini
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
```

### Step 8: Configure Nginx
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/mediwellcare
```

Add this content:
```nginx
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
```

### Step 9: Enable Site and Start Services
```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/mediwellcare /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Set permissions
sudo chown -R ubuntu:www-data /home/ubuntu/mediwell-care
sudo chmod -R 755 /home/ubuntu/mediwell-care

# Start services
sudo systemctl daemon-reload
sudo systemctl enable mediwellcare
sudo systemctl start mediwellcare
sudo systemctl restart nginx
```

### Step 10: Configure SSL
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d mediwellcare.com -d www.mediwellcare.com --non-interactive --agree-tos --email abdurrabkhan709@gmail.com
```

### Step 11: Configure Firewall
```bash
# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

## 🔧 Configuration Files

### Environment Variables (.env)
```bash
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=mediwellcare.com,www.mediwellcare.com,43.204.114.233
```

### Django Settings
Your `ALLOWED_HOSTS` in `settings.py` should include:
- `mediwellcare.com`
- `www.mediwellcare.com`
- `43.204.114.233`

## 🚀 Deployment Commands

### Initial Deployment
```bash
# Run the full deployment script
chmod +x deploy.sh
./deploy.sh
```

### Update Deployment
```bash
# Create update script
cat > update.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/mediwell-care
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart mediwellcare
echo "Update completed!"
EOF

chmod +x update.sh
```

## 🔍 Monitoring and Maintenance

### Check Service Status
```bash
# Check if services are running
sudo systemctl status mediwellcare
sudo systemctl status nginx

# View logs
sudo journalctl -u mediwellcare -f
sudo tail -f /var/log/nginx/error.log
```

### Restart Services
```bash
# Restart application
sudo systemctl restart mediwellcare

# Restart web server
sudo systemctl restart nginx

# Restart both
sudo systemctl restart mediwellcare nginx
```

## 🌐 Domain Configuration

### DNS Settings
In your domain registrar's DNS settings, add:
- **A Record**: `@` → `43.204.114.233`
- **A Record**: `www` → `43.204.114.233`

### SSL Certificate
The SSL certificate will be automatically configured by Certbot. Your site will be available at:
- `https://mediwellcare.com`
- `https://www.mediwellcare.com`

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Errors**
   ```bash
   sudo chown -R ubuntu:www-data /home/ubuntu/mediwell-care
   sudo chmod -R 755 /home/ubuntu/mediwell-care
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Database Errors**
   ```bash
   python manage.py migrate
   ```

4. **Service Not Starting**
   ```bash
   sudo systemctl status mediwellcare
   sudo journalctl -u mediwellcare -f
   ```

### Useful Commands
```bash
# Check Nginx configuration
sudo nginx -t

# View application logs
sudo journalctl -u mediwellcare -f

# Check disk space
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep gunicorn
```

## 📊 Performance Optimization

### Enable Gzip Compression
Add to your Nginx configuration:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

### Set Up Log Rotation
```bash
sudo nano /etc/logrotate.d/mediwellcare
```

Add:
```
/home/ubuntu/mediwell-care/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
```

## 🔒 Security Considerations

1. **Firewall Configuration**
   ```bash
   sudo ufw status
   sudo ufw allow ssh
   sudo ufw allow 'Nginx Full'
   ```

2. **Regular Updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Backup Strategy**
   ```bash
   # Create backup script
   cat > backup.sh << 'EOF'
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   cp /home/ubuntu/mediwell-care/db.sqlite3 /home/ubuntu/backups/db_$DATE.sqlite3
   find /home/ubuntu/backups -name "db_*.sqlite3" -mtime +7 -delete
   EOF
   ```

## 📞 Support

If you encounter any issues:
1. Check the logs: `sudo journalctl -u mediwellcare -f`
2. Verify service status: `sudo systemctl status mediwellcare`
3. Test Nginx configuration: `sudo nginx -t`

Your Django application should now be accessible at:
- **HTTP**: http://mediwellcare.com
- **HTTPS**: https://mediwellcare.com (after SSL setup)

🎉 **Congratulations! Your Mediwell Care website is now live on AWS!**
