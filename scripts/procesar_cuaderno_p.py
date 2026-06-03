import cv2
import os
from PIL import Image
import glob

def optimizar_bitacora(ruta_carpeta, archivo_pdf_salida):
    # Buscar todas las imágenes en la carpeta (ordenadas)
    extensiones = ('*.jpg', '*.jpeg', '*.png', '*.JPG')
    imagenes_rutas = []
    for ext in extensiones:
        imagenes_rutas.extend(glob.glob(os.path.join(ruta_carpeta, ext)))
    imagenes_rutas.sort(reverse=True)
    
    paginas_optimizadas = []
    
    for i, ruta_img in enumerate(imagenes_rutas):
        print(f"Procesando página {i+1}/{len(imagenes_rutas)}: {os.path.basename(ruta_img)}")
        
        # 1. Leer en escala de grises
        #img = cv2.imread(ruta_img, cv2.IMREAD_GRAYSCALE)
        img_color = cv2.imread(ruta_img)

        img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
        
        # 2. Redimensionar si es muy grande (ej. si el ancho supera 1600px)
        ancho_deseado = 1275
        if img_color.shape[1] > ancho_deseado:
            escala = ancho_deseado / img_color.shape[1]
            alto = int(img_color.shape[0] * escala)
            img_color = cv2.resize(img_color, (ancho_deseado, alto), interpolation=cv2.INTER_AREA)
        
        # Convertir a PIL (Modo 'L' es Escala de Grises de 8 bits, no binarizado)
        img_pil = Image.fromarray(img_color)

        # LA MAGIA: Convertir a modo 'P' (Paleta de colores optimizada) 
        # Esto reduce los 16 millones de colores a solo los 16 más importantes de la página
        img_paletizada = img_pil.convert('P', palette=Image.ADAPTIVE, colors=16)
        paginas_optimizadas.append(img_paletizada)


        # 3. Umbral Adaptativo: Convierte a Blanco y Negro puro adaptándose a la luz
        #img_binaria = cv2.adaptiveThreshold(
        #    img, 
        #    255, 
        #    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #    cv2.THRESH_BINARY, 
        #    21, # El tamaño del bloque. Debe ser un número impar. Define el tamaño del área vecina que se analiza para decidir si un píxel es texto o fondo. 
        #    7, # Es la constante que se resta de la media calculada. Si el texto se está borrando (está quedando "muy blanco"), disminuye este valor a 7, 5 o 3. Esto forzará al algoritmo a ser más permisivo con los trazos claros o lápices tenues.
        #)
        #
        ## 4. Convertir a formato PIL para poder compilar el PDF
        #img_pil = Image.fromarray(img_binaria).convert('1') # '1' es para bits binarios (B/N)
        #paginas_optimizadas.append(img_pil)
        
    # 5. Guardar todas las páginas procesadas en un único PDF compacto
    if paginas_optimizadas:
        paginas_optimizadas[0].save(
            archivo_pdf_salida,
            save_all=True,
            append_images=paginas_optimizadas[1:],
            optimize=True,
            #bits=1, # Forzar 1 bit por píxel
            dpi=(300,300)
        )
        print(f"» Éxito. Bitácora consolidada en: {archivo_pdf_salida}")
        print(f"» Tamaño final aproximado: {os.path.getsize(archivo_pdf_salida) / (1024*1024):.2f} MB")

# Ejemplo de uso:
# optimizar_bitacora("/tus_fotos/bitacora_01", "bitacora_01_optimizada.pdf")

if __name__ == '__main__':
    raise Exception('Falla la calidad de las imagenes')
    
    from argparse import ArgumentParser

    parser = ArgumentParser('procesar_cuaderno')
    parser.add_argument('--entrada', help='Directorio con las imagenes a procesar')
    parser.add_argument('--output', help='Nombre del documento PDF con el contenido de las imagenes')

    args = parser.parse_args()

    entrada_dir = args.entrada 
    output_file = args.output 

    optimizar_bitacora(entrada_dir, output_file)


