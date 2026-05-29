#!/bin/bash

BASE_DIR=$(dirname "$(readlink -f "$0")")

DESTINO_APP="$HOME/apps/traker_clima"

echo "Eliminando version antigua si existe..."
rm -f "$DESTINO_APP/TrakerClima"
rm -f "$DESTINO_APP/notificador"

mkdir -p "$DESTINO_APP"

echo "📦 Iniciando el proceso de empaquetado..."

echo "🖥️ Compilando el Menú Principal..."
pyinstaller --onefile --windowed --noconsole \
    --hidden-import="PIL._tkinter_finder" \
    --collect-all customtkinter \
    "$BASE_DIR/menu_interfaz.py" --name TrakerClima

echo "🔔 Compilando el Notificador de Clima..."
pyinstaller --onefile "$BASE_DIR/recordatorio.py" --name notificador --collect-all plyer

echo "✅ ¡Compilación exitosa!"

echo "📦 Copiando ejecutables..."
cp "$BASE_DIR/dist/TrakerClima" "$DESTINO_APP/"
cp "$BASE_DIR/dist/notificador" "$DESTINO_APP/"

chmod +x "$DESTINO_APP/"*

#copiando recursos

if [ -d "$BASE_DIR/notificacion" ]; then
    cp -r "$BASE_DIR/notificacion" "$DESTINO_APP/"
    echo "Sonido copiado"
else
    echo "No se encontro la caperta notificacion"
fi

if [ -f "$BASE_DIR/icon.png" ]; then
    cp "$BASE_DIR/icon.png" "$DESTINO_APP/"
    echo "Icono copiado"
else
    echo "No se econtro el archivo icon.png"
fi 

echo "Limpiando"
rm -rf "$BASE_DIR/build"
rm -rf "$BASE_DIR/dist"
rm -f "$BASE_DIR"/*.spec

echo "Empaquetado completo"

echo "⚙️ Configurando el servicio de Linux (Systemd User)..."

DIR_SERVICIOS="$HOME/.config/systemd/user"
mkdir -p "$DIR_SERVICIOS"

# Crear el archivo de servicio de forma dinámica
cat <<EOF > "$DIR_SERVICIOS/traker_clima.service"
[Unit]
Description=Servicio de Notificaciones de Tracker Clima
After=graphical-session.target

[Service]
Type=simple
ExecStart=$DESTINO_APP/notificador
WorkingDirectory=$DESTINO_APP
Restart=always
RestartSec=10
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/%U

[Install]
WantedBy=graphical-session.target
EOF

echo "🔄 Recargando systemd y activando el servicio..."
systemctl --user daemon-reload

# Habilitar (para que inicie con la PC) y arrancar (iniciar ahora mismo)
systemctl --user enable traker_clima.service
systemctl --user restart traker_clima.service

systemctl --user status traker_clima.service

echo "🚀 ¡Servicio instalado y corriendo en segundo plano!"

