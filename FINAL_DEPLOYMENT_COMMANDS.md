# 🚀 Final AWS Deployment Commands

## Copy & Paste These Commands in Your AWS Console

### **Step 1: One-Line Setup (Copy & Paste This Entire Block)**

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-pip python3-venv nginx git curl && mkdir -p /home/ubuntu/mediwell-care && cd /home/ubuntu/mediwell-care && git clone https://github.com/AbdurrabKhan198/new-medicare.git . && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install Django==5.0.1 gunicorn==21.2.0 whitenoise==6.6.0 psycopg2-binary==2.9.9 django-allauth==0.57.0 Pillow==10.1.0 django-crispy-forms==2.1 crispy-tailwind==0.5.0 django-environ==0.11.2 && cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=mediwellcare.com,www.mediwellcare.com,43.204.114.233
EOF
```

### **Step 2: Configure Services (Copy & Paste This Block)**

```bash
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
```

### **Step 3: Configure Nginx (Copy & Paste This Block)**

```bash
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
```

### **Step 4: Start Services (Copy & Paste This Block)**

```bash
sudo ln -s /etc/nginx/sites-available/mediwellcare /etc/nginx/sites-enabled/ && sudo rm /etc/nginx/sites-enabled/default && sudo chown -R ubuntu:www-data /home/ubuntu/mediwell-care && sudo chmod -R 755 /home/ubuntu/mediwell-care && sudo systemctl daemon-reload && sudo systemctl enable mediwellcare && sudo systemctl start mediwellcare && sudo systemctl restart nginx
```

### **Step 5: Configure Firewall & SSL (Copy & Paste This Block)**

```bash
sudo ufw allow 'Nginx Full' && sudo ufw allow ssh && sudo ufw --force enable && sudo apt install -y certbot python3-certbot-nginx && sudo certbot --nginx -d mediwellcare.com -d www.mediwellcare.com --non-interactive --agree-tos --email abdurrabkhan709@gmail.com
```

### **Step 6: Final Django Setup (Copy & Paste This Block)**

```bash
cd /home/ubuntu/mediwell-care && source venv/bin/activate && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py populate_data && sudo systemctl restart mediwellcare
```

## 🎉 **That's It! Your Website is Live!**

Your website will be available at:
- **HTTP**: http://mediwellcare.com
- **HTTPS**: https://mediwellcare.com

## 🔧 **Quick Commands for Later**

### Check Status
```bash
sudo systemctl status mediwellcare
```

### Restart Services
```bash
sudo systemctl restart mediwellcare
sudo systemctl restart nginx
```

### Update Your Site
```bash
cd /home/ubuntu/mediwell-care
source venv/bin/activate
git pull origin main
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart mediwellcare
```

### View Logs
```bash
sudo journalctl -u mediwellcare -f
```

## 📞 **Your Contact Information**
- **Phone**: +91 9616651137
- **Email**: abdurrabkhan709@gmail.com
- **Location**: Lucknow, Uttar Pradesh, India

## 🌐 **Domain Configuration**
In your domain registrar's DNS settings:
- **A Record**: `@` → `43.204.114.233`
- **A Record**: `www` → `43.204.114.233`

**Just copy and paste these commands one by one in your AWS console!** 🚀
