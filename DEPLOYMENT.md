# YAAN v1.0 - Deployment Guide

Complete guide for deploying YAAN in various environments.

## 📋 Table of Contents

- [Quick Start (Local)](#quick-start-local)
- [Installation Methods](#installation-methods)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [System Requirements](#system-requirements)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start (Local)

### Method 1: One-Click Installer (Recommended)

**Windows:**
```powershell
# Download and run installer
.\install.ps1

# Start YAAN
.\start.ps1
```

**Linux/Mac:**
```bash
# Make installer executable
chmod +x install.sh

# Run installer
./install.sh

# Start YAAN
./start.sh
```

### Method 2: Manual Installation

**1. Clone Repository**
```bash
git clone https://github.com/yashsiwacha/YAAN.git
cd YAAN
```

**2. Create Virtual Environment**
```bash
# Windows
python -m venv backend\venv
backend\venv\Scripts\activate

# Linux/Mac
python3 -m venv backend/venv
source backend/venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r backend/requirements.txt
```

**4. Run YAAN**
```bash
cd backend
python main.py
```

**5. Open Browser**
```
http://localhost:8000
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

**1. Install Docker**
- Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: `sudo apt install docker.io docker-compose`
- Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop)

**2. Start YAAN**
```bash
docker-compose up -d
```

**3. Access YAAN**
```
http://localhost:8000
```

**4. View Logs**
```bash
docker-compose logs -f
```

**5. Stop YAAN**
```bash
docker-compose down
```

### Using Docker CLI

**Build Image:**
```bash
docker build -t yaan:v1.0 .
```

**Run Container:**
```bash
docker run -d \
  --name yaan \
  -p 8000:8000 \
  -v $(pwd)/backend/data:/app/backend/data \
  -v $(pwd)/backend/logs:/app/backend/logs \
  yaan:v1.0
```

**Stop Container:**
```bash
docker stop yaan
docker rm yaan
```

---

## 🌐 Production Deployment

### Option 1: Linux Server (systemd)

**1. Create Service File**
```bash
sudo nano /etc/systemd/system/yaan.service
```

**2. Service Configuration**
```ini
[Unit]
Description=YAAN - Your AI Assistant Network
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/YAAN/backend
Environment="PATH=/path/to/YAAN/backend/venv/bin"
ExecStart=/path/to/YAAN/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**3. Enable and Start**
```bash
sudo systemctl daemon-reload
sudo systemctl enable yaan
sudo systemctl start yaan
sudo systemctl status yaan
```

**4. View Logs**
```bash
sudo journalctl -u yaan -f
```

### Option 2: Windows Service

**Using NSSM (Non-Sucking Service Manager):**

**1. Download NSSM**
```
https://nssm.cc/download
```

**2. Install Service**
```powershell
nssm install YAAN "C:\Path\To\YAAN\backend\venv\Scripts\python.exe" "C:\Path\To\YAAN\backend\main.py"
```

**3. Configure Service**
```powershell
nssm set YAAN AppDirectory "C:\Path\To\YAAN\backend"
nssm set YAAN DisplayName "YAAN AI Assistant"
nssm set YAAN Description "Your AI Assistant Network v1.0"
nssm set YAAN Start SERVICE_AUTO_START
```

**4. Start Service**
```powershell
nssm start YAAN
```

### Option 3: Nginx Reverse Proxy

**1. Install Nginx**
```bash
sudo apt install nginx
```

**2. Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/yaan
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**3. Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/yaan /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 4: Cloud Deployment

#### AWS EC2

**1. Launch EC2 Instance**
- Ubuntu 22.04 LTS
- t2.small or larger
- Open port 8000 (or 80 with Nginx)

**2. SSH and Install**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
git clone https://github.com/yashsiwacha/YAAN.git
cd YAAN
./install.sh
```

**3. Set up systemd service** (see above)

#### Google Cloud Platform

**1. Create VM Instance**
```bash
gcloud compute instances create yaan-vm \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=e2-small \
  --zone=us-central1-a
```

**2. SSH and Deploy**
```bash
gcloud compute ssh yaan-vm
# Follow installation steps above
```

#### Azure

**1. Create VM**
```bash
az vm create \
  --resource-group YAANGroup \
  --name yaan-vm \
  --image UbuntuLTS \
  --size Standard_B1s \
  --generate-ssh-keys
```

**2. SSH and Deploy**
```bash
ssh azureuser@your-vm-ip
# Follow installation steps above
```

---

## ⚙️ System Requirements

### Minimum Requirements
- **OS**: Windows 10+, Linux (Ubuntu 20.04+), macOS 11+
- **CPU**: 2 cores
- **RAM**: 2GB
- **Storage**: 500MB
- **Python**: 3.10+

### Recommended Requirements
- **OS**: Windows 11, Linux (Ubuntu 22.04), macOS 12+
- **CPU**: 4 cores
- **RAM**: 4GB
- **Storage**: 1GB
- **Python**: 3.12

### Network Requirements
- **Ports**: 8000 (default)
- **Internet**: Not required (fully offline)

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Server Configuration
PORT=8000
HOST=127.0.0.1

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/yaan.log

# Database
DATA_DIR=data/
```

### Custom Port

**Method 1: Environment Variable**
```bash
export PORT=8080
python main.py
```

**Method 2: Modify main.py**
```python
# In backend/main.py
if __name__ == "__main__":
    uvicorn.run(server.app, host="127.0.0.1", port=8080)
```

---

## 🐛 Troubleshooting

### Port Already in Use

**Find Process Using Port:**
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

**Kill Process:**
```bash
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

### Virtual Environment Issues

**Recreate venv:**
```bash
# Remove old venv
rm -rf backend/venv

# Create new
python3 -m venv backend/venv

# Reinstall dependencies
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### Permission Denied (Linux/Mac)

```bash
chmod +x install.sh
chmod +x start.sh
```

### Python Version Issues

**Check Version:**
```bash
python --version
python3 --version
```

**Install Correct Version:**
```bash
# Ubuntu/Debian
sudo apt install python3.12

# Mac
brew install python@3.12
```

### Module Not Found

```bash
# Activate venv
source backend/venv/bin/activate  # Linux/Mac
backend\venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Database Locked

**Reset Databases:**
```bash
rm backend/data/*.db
# Databases will be recreated on next start
```

---

## 📊 Monitoring

### View Logs

**Real-time Logs:**
```bash
tail -f backend/logs/yaan.log
```

**Check Status:**
```bash
# systemd
sudo systemctl status yaan

# Docker
docker ps
docker logs yaan -f
```

### Health Check

```bash
curl http://localhost:8000/
```

---

## 🔄 Updates

### Update YAAN

```bash
# Stop service
./stop.sh  # or docker-compose down

# Pull latest changes
git pull origin main

# Reinstall dependencies
source backend/venv/bin/activate
pip install -r backend/requirements.txt --upgrade

# Restart service
./start.sh  # or docker-compose up -d
```

---

## 🔐 Security Recommendations

### For Public Deployment

1. **Use HTTPS** with SSL/TLS certificates (Let's Encrypt)
2. **Set up firewall** rules
3. **Enable authentication** (add auth layer if needed)
4. **Regular backups** of data directory
5. **Keep Python and dependencies updated**
6. **Use environment variables** for sensitive config
7. **Limit file permissions**

### Firewall Configuration

**Ubuntu (UFW):**
```bash
sudo ufw allow 8000
sudo ufw enable
```

**CentOS (firewalld):**
```bash
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

---

## 📦 Backup & Restore

### Backup

```bash
# Backup data
tar -czf yaan-backup-$(date +%Y%m%d).tar.gz backend/data/

# Backup everything
tar -czf yaan-full-backup-$(date +%Y%m%d).tar.gz \
  backend/data/ \
  backend/logs/ \
  backend/.env
```

### Restore

```bash
# Extract backup
tar -xzf yaan-backup-20260217.tar.gz -C backend/

# Restart YAAN
./start.sh
```

---

## 💡 Performance Optimization

### Resource Limits (Docker)

```yaml
# In docker-compose.yml
services:
  yaan:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Database Optimization

Databases are automatically optimized. For large datasets:
- Regular VACUUM operations
- Periodic backups
- Monitor database size

---

## 📞 Support

- **Documentation**: See README.md and other guides
- **Issues**: https://github.com/yashsiwacha/YAAN/issues
- **Discussions**: https://github.com/yashsiwacha/YAAN/discussions

---

## 📄 License

MIT License - See LICENSE file for details

---

**Last Updated**: February 17, 2026  
**YAAN Version**: 1.0.0
