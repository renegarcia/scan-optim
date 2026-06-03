# Convertir fotos a pdf en escala de grises


Usa este comando (asumiendo que las fotos están en JPG y nombradas secuencialmente como img001.jpg … img089.jpg). Ejecuta desde la carpeta con las imágenes:

1. Convertir a escala de grises y redimensionar (salida en carpeta optimized/):

```sh
mkdir -p optimized
for f in *.jpg; do convert "$f" -colorspace Gray -strip -interlace Plane -quality 85 -resize 1500x "optimized/$f"; done
```

2. Opcional) Comprobar tamaño/visual y luego unir en PDF optimizado como si fuera un escaneo:

```sh
cd optimized
convert -density 200 -compress jpeg *.jpg -quality 85 ../cuaderno_scan.pdf
``` 

**Notas breves:**

* -resize 1500x limita ancho/alto máximo a 1500 px sin agrandar imágenes más pequeñas.
* -colorspace Gray convierte a escala de grises; -strip quita metadatos; -quality y -compress jpeg reducen tamaño.
* Ajusta -density (p. ej. 150 o 200) para controlar resolución del PDF final.
* Si prefieres mejor suavizado de texto, reemplaza convert por magick según tu versión de ImageMagick.

## Convertir fotos a webp 

```sh
mkdir -p webp
for f in *.jpg; do cwebp -q 80 "$f" -o "webp/${f%.*}.webp"; done
magick webp/*.webp -density 200 cuaderno_webp.pdf
```

Si prefieres mantener escala de grises 

```sh
mkdir -p webp
for f in *.jpg; do
  magick "$f" -colorspace Gray -resize 1500x -strip -quality 80 "webp/${f%.*}.webp"
done
magick webp/*.webp -density 200 cuaderno_webp.pdf
```

