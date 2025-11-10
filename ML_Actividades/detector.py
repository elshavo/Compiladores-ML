import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectar_lineas(ruta_imagen):
    """
    Carga una imagen, aplica kernels para detectar líneas horizontales
    y verticales, y muestra los resultados.
    """
    
    # --- 1. Cargar la imagen ---
    # Cargar la imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
        return

    # --- 2. Definir los Kernels ---
    
    # Kernel para detectar líneas horizontales
    # Este kernel tiene valores positivos en la fila central
    # y negativos en las filas superior e inferior.
    # Resalta las líneas que son brillantes y están rodeadas de oscuridad.
    kernel_horizontal = np.array([
        [-1, 0, -1],
        [ 2, 0,  2],
        [-1, 0, -1]
    ], dtype=np.float32)

    # Kernel para detectar líneas verticales
    # Es el kernel horizontal rotado 90 grados.
    kernel_vertical = np.array([
        [-1, 2, -1],
        [0, 0, 0],
        [-1, 2, -1]
    ], dtype=np.float32)

    # --- 3. Aplicar los Kernels (Convolución) ---
    
    # Usamos cv2.filter2D para aplicar la convolución del kernel con la imagen
    # El -1 indica que la profundidad de bits de salida será la misma que la de entrada.
    img_horizontal = cv2.filter2D(img, -1, kernel_horizontal)
    img_vertical = cv2.filter2D(img, -1, kernel_vertical)

    # --- 4. Mostrar los resultados ---
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(img_horizontal, cmap='gray')
    plt.title('Líneas Horizontales')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(img_vertical, cmap='gray')
    plt.title('Líneas Verticales')
    plt.axis('off')

    plt.suptitle('Detección de Líneas con Kernels Manuales')
    plt.show()

# --- EJECUCIÓN DEL CÓDIGO ---

# Reemplaza 'tu_imagen.jpg' con la ruta a tu propia imagen.
# Para esta prueba, asegúrate de tener una imagen con líneas claras
# (por ejemplo, una cuadrícula, una hoja de cuaderno, o la fachada de un edificio).
try:
    detectar_lineas('manzana.webp') 
except FileNotFoundError:
    print("Error: El archivo 'tu_imagen.png' no se encontró.")
    print("Por favor, reemplaza 'tu_imagen.png' con la ruta a una imagen válida.")