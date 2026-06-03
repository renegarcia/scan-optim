#!/bin/fish
# Uso: ./optimizar.sh /ruta/carpeta_con_fotos nombre_salida.pdf

set CARPETA $argv[1]
set SALIDA $argv[2]

if test ! -d "$SALIDA"
    echo "Error: $SALIDA no es un directorio: $SALIDA" >&2
    exit 1
end

if not ls -- $CARPETA/*.{jpg,jpeg,png} >/dev/null 2>&1
    echo "No hay archivos" >/dev/stderr
    exit 1
end

echo "Procesando imágenes de $CARPETA..."

for f in $CARPETA/*.{jpg,png}
    # nombre base sin extensión:
    set filename (basename -- $f .jpg)

    # construir salida con nueva extensión .webp
    set outpath $SALIDA/$filename.webp

    #echo $f
    magick "$f" -quality 80 "$outpath"
end
