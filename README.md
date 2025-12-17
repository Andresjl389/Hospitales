# Hospitales

Guía breve para instalar y desplegar el backend en Ubuntu.

## Requisitos
- Python 3.13, pip y venv
- PostgreSQL 17 con usuario y BD creados
- Git, build-essential, libpq-dev, ffmpeg (para manejo de video)

Instala dependencias del sistema:
```bash
sudo apt update && sudo apt install -y python3.13 python3.13-venv python3-pip git build-essential libpq-dev ffmpeg postgresql
```

## Instalación y entorno
```bash
cd /opt
sudo git clone <repo-url> hospitales
sudo chown -R $USER hospitales
cd hospitales

python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Variables de entorno
Crea `/opt/hospitales/.env` con:
```
DB_HOST=localhost
DB_USER=hospitales_user
DB_PASSWORD=strongpassword
DB_PORT=5432
DB_ENGINE=postgresql
DB_NAME=hospitales
JWT_SECRET=supersecretjwtkey
```

## Base de datos
Ejemplo para crear usuario y base:
```bash
sudo -u postgres psql <<'SQL'
CREATE USER hospitales_user WITH PASSWORD 'strongpassword';
CREATE DATABASE hospitales OWNER hospitales_user;
GRANT ALL PRIVILEGES ON DATABASE hospitales TO hospitales_user;
SQL
```

Aplica migraciones desde la raíz del proyecto (venv activo):
```bash
alembic upgrade head
```

## Ejecutar en desarrollo
```bash
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```
Revisa la API en `http://<server>:8000/docs`. La CORS actual permite `https://hospitales-frontend.vercel.app`; ajusta `allow_origins` en `main.py` si necesitas más orígenes.

## Servicio systemd (producción)
Crea `/etc/systemd/system/hospitales.service`:
```
[Unit]
Description=Hospitales FastAPI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/hospitales
EnvironmentFile=/opt/hospitales/.env
ExecStart=/opt/hospitales/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```
Activa y revisa:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hospitales
journalctl -u hospitales -f
```

## Nginx como proxy (opcional recomendado)
```bash
sudo apt install -y nginx
```
Archivo `/etc/nginx/sites-available/hospitales`:
```
server {
  listen 80;
  server_name tu.dominio.com;

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
  location /media/ {
    alias /opt/hospitales/media/;
  }
}
```
Habilita y recarga:
```bash
sudo ln -s /etc/nginx/sites-available/hospitales /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```
Para HTTPS:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d tu.dominio.com
```

## Mantenimiento
- Actualizar código y deps: `git pull && source .venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && sudo systemctl restart hospitales`
- Logs: `journalctl -u hospitales -f`
- Respalda la base y protege `.env` y `JWT_SECRET`.
