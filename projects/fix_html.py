import os
import chardet

def convert_to_utf8(file_path):
    """Convierte un archivo a UTF-8 si no está en esa codificación."""
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)  # detecta codificación
        encoding = result['encoding']

    if encoding is None:
        print(f"No se pudo detectar codificación de {file_path}, se saltea.")
        return

    text = raw.decode(encoding, errors='replace')

    # Guardar de nuevo en UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Convertido a UTF-8: {file_path}")


def ensure_meta_and_favicon(file_path):
    """Revisa y agrega meta charset, viewport y favicon si faltan."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Charset
    if '<meta charset="UTF-8">' not in content:
        content = content.replace("<head>", '<head>\n  <meta charset="UTF-8">')
        modified = True

    # Viewport
    if 'name="viewport"' not in content:
        content = content.replace("<head>", '<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        modified = True

    # Favicon
    if 'rel="SHORTCUT ICON"' not in content and 'rel="icon"' not in content:
        content = content.replace("<head>", '<head>\n  <link rel="SHORTCUT ICON" href="../../recursos/favicon.ico">')
        modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Corregido encabezado en {file_path}")


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                convert_to_utf8(path)
                ensure_meta_and_favicon(path)


if __name__ == "__main__":
    ruta = input("Carpeta donde están los HTML: ")
    process_directory(ruta)

