# Mediwell Care - Build Instructions

## 🚀 Quick Start

### Development Server
```bash
python dev_server.py
```

### Manual Build
```bash
python build_assets.py
```

## 📦 Asset Building

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- Django 5.2+

### Build Process

1. **Install Dependencies**
   ```bash
   npm install
   pip install -r requirements.txt
   ```

2. **Build CSS**
   ```bash
   npm run build-css-prod
   ```

3. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

## 🎨 Tailwind CSS Setup

### Development
- **Input**: `static/css/input.css`
- **Output**: `static/css/output.css`
- **Config**: `tailwind.config.js`

### Custom Classes
- `.btn-primary` - Primary button with medical gradient
- `.btn-secondary` - Secondary button with medical blue border
- `.hover-lift` - Hover lift effect
- `.medical-gradient` - Medical blue to aqua gradient
- `.text-medical-blue` - Medical blue text color
- `.text-medical-aqua` - Medical aqua text color

### Color Palette
- **Medical Blue**: `#1E40AF`
- **Medical Aqua**: `#06B6D4`
- **Medical Green**: `#10B981`
- **Medical Gray**: `#6B7280`

## 🔧 Development Commands

### Watch Mode (for CSS changes)
```bash
npm run build-css
```

### Production Build
```bash
npm run build-css-prod
```

### Django Commands
```bash
python manage.py runserver
python manage.py collectstatic
python manage.py migrate
python manage.py populate_data
```

## 📁 File Structure

```
mediwell_care/
├── static/
│   ├── css/
│   │   ├── input.css      # Tailwind input
│   │   └── output.css     # Compiled CSS
│   └── js/
├── templates/
├── tailwind.config.js      # Tailwind configuration
├── package.json           # Node.js dependencies
├── build_assets.py        # Build script
└── dev_server.py          # Development server
```

## 🎯 Production Deployment

1. **Build Assets**
   ```bash
   python build_assets.py
   ```

2. **Set Environment Variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-secret-key
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Start Production Server**
   ```bash
   gunicorn mediwell_care.wsgi:application
   ```

## 🐛 Troubleshooting

### CSS Not Loading
- Check if `static/css/output.css` exists
- Run `python manage.py collectstatic`
- Verify `STATIC_URL` in settings

### Tailwind Classes Not Working
- Rebuild CSS: `npm run build-css-prod`
- Check `tailwind.config.js` content paths
- Verify template file paths in config

### Node.js Issues
- Update Node.js to latest LTS version
- Clear npm cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`
