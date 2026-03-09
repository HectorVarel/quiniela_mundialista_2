
from PIL import Image
import base64
import io
import sqlite3

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # Leer el contenido de la imagen
        image_content = image_file.read()
        
        # Convertir la imagen a base64
        base64_image = base64.b64encode(image_content).decode("utf-8")
        
        return base64_image


def base64_to_image(base64_string):
    # Decodificar la cadena base64 a bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Convertir los bytes a un objeto de imagen
    image = Image.open(io.BytesIO(image_bytes))
    
    # Mostrar la imagen
    image.show()


equipos = ["mexico", "sudafrica", "corea", "m1", "m2", "m3", "m4", "m5", "m6",
           "canada", "qatar", "suiza", "brasil", "marruecos", "haiti",
           "escocia", "eua", "paraguay", "australia", "alemania", "curazao",
           "costa_de_marfil", "ecuador", "holanda", "japon", "tunez", "belgica",
           "egipto", "iran", "nueva_zelanda", "espania", "cabo_verde",
           "arabia_saudita", "uruguay", "francia", "senegal", "noruega", 
           "argentina", "argelia", "austria", "jordania", "portugal",
           "uzbekistan", "colombia", "inglaterra", "croacia", "ghana", "panama"]
equipos = ["inglaterra"]
for e in equipos:
    # Ruta de la imagen a convertir
    image_path = f"C:/Users/varel/Pictures/escudos_equipos/w2560/{e}.png"

    # Convertir la imagen a base64
    base64_image = image_to_base64(image_path)

    # Imprimir el resultado
    print(len(base64_image))

    """
    # Función para guardar la cadena base64 en un archivo de texto
    def save_base64_to_txt(base64_string, txt_path):
        with open(txt_path, "w") as text_file:
            text_file.write(base64_string)
        print(f"Base64 guardado en {txt_path}")

    # Ruta del archivo de texto donde se guardará la cadena base64
    txt_path = "C:/Users/varel/Documents/ProjectDjango/quiniela_editable/san_luis_base64.txt"

    # Guardar la cadena base64 en el archivo de texto
    save_base64_to_txt(base64_image, txt_path)
    """
    #"""

    # Cadena base64 de la imagen

    # Convertir la cadena base64 a imagen y mostrarla
    #base64_to_image(base64_image)

    # Conectar a la base de datos
    conn = sqlite3.connect('C:/Users/varel/Documents/ProjectDjango/quiniela_mundialista_2/db.sqlite3')

    # Crear un cursor
    cursor = conn.cursor()

    # Ejecutar la actualización
    cursor.execute(f"UPDATE llenar_quiniela_equipos_fotos SET {e} = '{base64_image}';")

    # Confirmar la transacción
    conn.commit()

    # Cerrar la conexión
    conn.close()
    #"""