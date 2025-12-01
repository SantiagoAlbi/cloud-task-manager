FROM nginx:1.29.3-alpine

# Copiar archivos estáticos a nginx
COPY index.html /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/

# Exponer puerto
EXPOSE 80

# Nginx corre automáticamente
