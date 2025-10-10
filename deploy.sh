#!/bin/bash

# Mediwell Care Deployment Script
# Run this script on your AWS EC2 instance

set -e  # Exit on any error

echo "🚀 Starting Mediwell Care deployment..."

# Configuration
PROJECT_DIR="/home/ubuntu/mediwell-care"
REPO_URL="https://github.com/yourusername/your-repo-name.git"  # Update this with your actual repo
DOMAIN="mediwellcare.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Use a regular user with sudo privileges."
    exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv python3-dev nginx postgresql postgresql-contrib git curl

# Create project directory
if [ ! -d "$PROJECT_DIR" ]; then
    print_status "Creating project directory..."
    mkdir -p $PROJECT_DIR
fi

cd $PROJECT_DIR

# Clone or update repository
if [ -d ".git" ]; then
    print_status "Updating existing repository..."
    git pull origin main
else
    print_status "Cloning repository..."
    git clone $REPO_URL .
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
print_status "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements-prod.txt

# Create logs directory
mkdir -p logs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating environment file..."
    cat > .env << EOF
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DB_NAME=mediwellcare
DB_USER=postgres
DB_PASSWORD=your_db_password_here
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=abdurrabkhan709@gmail.com
EMAIL_HOST_PASSWORD=your_email_password_here
REDIS_URL=redis://127.0.0.1:6379/0
USE_S3=False
EOF
    print_warning "Please update the .env file with your actual database and email credentials!"
fi

# Set up database
print_status "Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE mediwellcare;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER mediwellcare WITH PASSWORD 'your_db_password_here';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mediwellcare TO mediwellcare;" 2>/dev/null || true

# Run Django commands
print_status "Running Django setup commands..."
export DJANGO_SETTINGS_MODULE=mediwell_care.settings_prod
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py populate_data

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/mediwellcare.service > /dev/null << EOF
[Unit]
Description=Mediwell Care Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=mediwell_care.settings_prod"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind unix:$PROJECT_DIR/mediwellcare.sock mediwell_care.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/mediwellcare > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN 43.204.114.233;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $PROJECT_DIR;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        root $PROJECT_DIR;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/mediwellcare.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site and start services
print_status "Enabling site and starting services..."
sudo ln -sf /etc/nginx/sites-available/mediwellcare /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test configurations
sudo nginx -t

# Set proper permissions
sudo chown -R ubuntu:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR

# Start and enable services
sudo systemctl daemon-reload
sudo systemctl enable mediwellcare
sudo systemctl start mediwellcare
sudo systemctl enable nginx
sudo systemctl restart nginx

# Configure firewall
print_status "Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# Install SSL certificate
print_status "Installing SSL certificate..."
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email abdurrabkhan709@gmail.com

# Create deployment script
print_status "Creating deployment script..."
cat > $PROJECT_DIR/deploy.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/mediwell-care
source venv/bin/activate
git pull origin main
pip install -r requirements-prod.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart mediwellcare
echo "Deployment completed!"
EOF

chmod +x $PROJECT_DIR/deploy.sh

# Final status check
print_status "Checking service status..."
sudo systemctl status mediwellcare --no-pager
sudo systemctl status nginx --no-pager

print_status "🎉 Deployment completed successfully!"
print_status "Your site should be available at: https://$DOMAIN"
print_status "To update your site in the future, run: $PROJECT_DIR/deploy.sh"

# Display useful information
echo ""
echo "📋 Useful Commands:"
echo "  Check service status: sudo systemctl status mediwellcare"
echo "  View logs: sudo journalctl -u mediwellcare -f"
echo "  Restart services: sudo systemctl restart mediwellcare nginx"
echo "  Update site: $PROJECT_DIR/deploy.sh"
echo ""
echo "🔧 Next Steps:"
echo "  1. Update your .env file with correct database and email credentials"
echo "  2. Configure your domain DNS to point to 43.204.114.233"
echo "  3. Test your website at https://$DOMAIN"
