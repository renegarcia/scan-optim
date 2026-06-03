import cv2
import os
from PIL import Image
import glob

def optimizar_con_resaltado_gris(ruta_carpeta, archivo_pdf_salida):
    extensiones = ('*.jpg', '*.jpeg', '*.png', '*.JPG')
    imagenes_rutas = []
    for ext in extensiones:
        imagenes_rutas.extend(glob.glob(os.path.join(ruta_carpeta, ext)))
    imagenes_rutas.sort()
    
    paginas_optimizadas = []
    
    for i,ruta_img in enumerate(imagenes_rutas):
        print(f"Procesando página {i+1}/{len(imagenes_rutas)}: {os.path.basename(ruta_img)}")
        # 1. Leer a color (BGR)
        img_color = cv2.imread(ruta_img)
        
        # 2. Extraer SOLO el canal Azul (Índice 0 en OpenCV)
        # El amarillo se oscurece drásticamente en este canal
        img_canal_azul = img_color[:, :, 0]
        
        # 3. Redimensionar a tus 2000px deseados
        ancho_deseado = 2000
        if img_canal_azul.shape[1] > ancho_deseado:
            escala = ancho_deseado / img_canal_azul.shape[1]
            alto = int(img_canal_azul.shape[0] * escala)
            img_canal_azul = cv2.resize(img_canal_azul, (ancho_deseado, alto), interpolation=cv2.INTER_AREA)
        
        # 4. Ecualizar un poco el contraste para que el fondo vuelva a ser blanco
        # pero el "bloque" del resaltador se note oscuro
        img_contraste = cv2.equalizeHist(img_canal_azul)
        
        # Convertir a PIL (Modo 'L' es Escala de Grises de 8 bits, no binarizado)
        img_pil = Image.fromarray(img_contraste).convert('L')
        paginas_optimizadas.append(img_pil)
        
    if paginas_optimizadas:
        # Guardamos con compresión para escala de grises
        paginas_optimizadas[0].save(
            archivo_pdf_salida, 
            format='PDF',
            save_all=True, 
            append_images=paginas_optimizadas[1:],
            optimize=True, 
            dpi=(300, 300),
        )
        print("PDF guardado conservando el resaltado en gris oscuro.")

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

    optimizar_con_resaltado_gris(entrada_dir, output_file)


