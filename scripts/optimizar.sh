#!/bin/bash
# Uso: ./optimizar.sh /ruta/carpeta_con_fotos nombre_salida.pdf

CARPETA=$1
SALIDA=$2

echo "Procesando imágenes de $CARPETA..."

# 1. Convertir, binarizar (limpiar fondo) y redimensionar temporalmente
# 2. Unificar todo en un único PDF altamente comprimido
magick "$CARPETA"/*.{jpg} \
       -colorspace gray \
       -threshold 60% \
       -resize 1500x \
       -compress Group4 \
       "$SALIDA"

echo "¡Listo! Archivo guardado como $SALIDA"
