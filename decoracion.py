"""
decoracion.py
-------------
Todo lo VISUAL de la aplicación: colores, fuentes, textos, imágenes
y los widgets ya decorados (encabezado, tarjetas de hotel, botones).
La lógica de las reservas vive en main.py.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageTk  # Pillow permite usar JPG y redimensionar
except ImportError:
    Image = ImageTk = None

# ---------------------------------------------------------------------------
# COLORES
# ---------------------------------------------------------------------------
COLOR_FONDO = "#EAF4F8"
COLOR_PRIMARIO = "#0B3C5D"
COLOR_ACENTO = "#F5A623"
COLOR_ACENTO_HOVER = "#FFB946"
COLOR_TARJETA = "#FFFFFF"
COLOR_TEXTO = "#1F2D3D"
COLOR_TEXTO_SUAVE = "#6B7C8D"
COLOR_PRECIO = "#1B8A5A"
COLOR_TAB = "#CFE3EC"
COLOR_PELIGRO = "#C0392B"

# ---------------------------------------------------------------------------
# FUENTES
# ---------------------------------------------------------------------------
FUENTE_TITULO = ("Segoe UI", 22, "bold")
FUENTE_SLOGAN = ("Segoe UI", 11, "italic")
FUENTE_SUBTITULO = ("Segoe UI", 14, "bold")
FUENTE_TEXTO = ("Segoe UI", 10)
FUENTE_BOLD = ("Segoe UI", 10, "bold")
FUENTE_TAB = ("Segoe UI", 11, "bold")
FUENTE_TOTAL = ("Segoe UI", 16, "bold")

# ---------------------------------------------------------------------------
# TEXTOS
# ---------------------------------------------------------------------------
TITULO_VENTANA = "Decameron - Sistema de Reservas"
TITULO_APP = "DECAMERON"
SLOGAN = "Todo incluido en el corazon de Latinoamerica"

TAB_HOTELES = "  Hoteles  "
TAB_RESERVAR = "  Reservar  "
TAB_DESPACHO = "  Despacho  "

TXT_ELEGIR = "Reservar aqui"
TXT_CONFIRMAR = "Confirmar reserva"
TXT_CANCELAR_RESERVA = "Cancelar reserva seleccionada"
TXT_SIN_FOTO = "Sin foto"

# ---------------------------------------------------------------------------
# HOTELES (presentación). Los precios y la lógica están en main.py
# Para usar tus propias fotos, reemplaza los archivos de la carpeta
# "imagenes" (o cambia el nombre de archivo aquí).
# ---------------------------------------------------------------------------
HOTELES = {
    1: {
        "nombre": "Decameron Baru",
        "ciudad": "Cartagena - Isla de Baru",
        "pais": "Colombia",
        "descripcion": "Resort frente al Caribe colombiano con playas de arena "
                       "blanca, snorkel y todo incluido.",
        "imagen": "baru.jpg",
        "color": "#00A3B5",
    },
    2: {
        "nombre": "Decameron Panama",
        "ciudad": "Playa Blanca - Rio Hato",
        "pais": "Panama",
        "descripcion": "Resort en la costa del Pacifico panameño con piscinas, "
                       "shows nocturnos y mucho sol.",
        "imagen": "panama.jpg",
        "color": "#E8743B",
    },
    3: {
        # Nota: no tengo constancia de un Decameron en Chile, por eso este
        # tercer hotel es el de Punta Sal (Peru). Puedes cambiarlo aqui.
        "nombre": "Decameron Punta Sal",
        "ciudad": "Punta Sal - Tumbes",
        "pais": "Peru",
        "descripcion": "Resort en el norte peruano, con mar calido casi todo el "
                       "año y atardeceres inolvidables.",
        "imagen": "punta_sal.jpg",
        "color": "#9B59B6",
    },
}

# ---------------------------------------------------------------------------
# IMÁGENES
# ---------------------------------------------------------------------------
def ruta_recurso(ruta_relativa):
    """Funciona tanto en Python normal como dentro de un .exe de PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, ruta_relativa)


EXTENSIONES = (".jpg", ".jpeg", ".png", ".gif", ".webp")


def buscar_imagen(nombre):
    """
    Busca la foto por su nombre (sin importar la extension ni mayusculas) en la
    carpeta "imagenes" y tambien junto a este archivo. Devuelve la ruta o None.
    """
    base_buscada = os.path.splitext(nombre)[0].lower()
    for carpeta in (ruta_recurso("imagenes"), ruta_recurso("")):
        if not os.path.isdir(carpeta):
            continue
        for archivo in os.listdir(carpeta):
            base, extension = os.path.splitext(archivo)
            if base.lower() == base_buscada and extension.lower() in EXTENSIONES:
                return os.path.join(carpeta, archivo)
    return None


def cargar_imagen(nombre_archivo, ancho, alto):
    """
    Devuelve una imagen lista para Tkinter, recortada y ajustada a ancho x alto.
    Si no existe el archivo (o no se puede abrir) devuelve None y avisa en consola.
    OJO: quien la use debe guardarla en una variable, o Tkinter la borra.
    """
    ruta = buscar_imagen(nombre_archivo)
    if ruta is None:
        print(f"[decoracion] No encontre la foto '{nombre_archivo}'. "
              f"La busque en: {ruta_recurso('imagenes')}")
        return None
    try:
        if Image is not None:
            img = Image.open(ruta).convert("RGB")
            # recorte centrado para llenar el recuadro sin deformar la foto
            proporcion = max(ancho / img.width, alto / img.height)
            nuevo = (int(img.width * proporcion), int(img.height * proporcion))
            img = img.resize(nuevo, Image.LANCZOS)
            izq = (img.width - ancho) // 2
            sup = (img.height - alto) // 2
            img = img.crop((izq, sup, izq + ancho, sup + alto))
            return ImageTk.PhotoImage(img)
        # Sin Pillow solo funcionan PNG y GIF (y sin ajustar el tamaño)
        return tk.PhotoImage(file=ruta)
    except Exception as error:
        print(f"[decoracion] No pude abrir '{ruta}': {error}. "
              f"Si es JPG/WEBP, instala Pillow con: pip install pillow")
        return None


# ---------------------------------------------------------------------------
# ESTILOS Y WIDGETS DECORADOS
# ---------------------------------------------------------------------------
def aplicar_estilos(root):
    estilo = ttk.Style(root)
    estilo.theme_use("clam")
    estilo.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
    estilo.configure("TNotebook.Tab", font=FUENTE_TAB, padding=(18, 8),
                     background=COLOR_TAB, foreground=COLOR_TEXTO)
    estilo.map("TNotebook.Tab",
               background=[("selected", COLOR_ACENTO)],
               foreground=[("selected", COLOR_TEXTO)])
    estilo.configure("Treeview", font=FUENTE_TEXTO, rowheight=28,
                     background="white", fieldbackground="white")
    estilo.configure("Treeview.Heading", font=FUENTE_BOLD,
                     background=COLOR_PRIMARIO, foreground="white")
    estilo.map("Treeview.Heading", background=[("active", COLOR_PRIMARIO)])
    estilo.configure("TCombobox", padding=4)


def crear_encabezado(parent):
    marco = tk.Frame(parent, bg=COLOR_PRIMARIO)
    tk.Label(marco, text=TITULO_APP, font=FUENTE_TITULO,
             bg=COLOR_PRIMARIO, fg="white").pack(pady=(14, 0))
    tk.Label(marco, text=SLOGAN, font=FUENTE_SLOGAN,
             bg=COLOR_PRIMARIO, fg=COLOR_ACENTO).pack(pady=(0, 14))
    return marco


def crear_boton(parent, texto, comando, color=COLOR_ACENTO, color_hover=COLOR_ACENTO_HOVER,
                color_texto=COLOR_TEXTO):
    boton = tk.Button(parent, text=texto, command=comando, font=FUENTE_BOLD,
                      bg=color, fg=color_texto, activebackground=color_hover,
                      activeforeground=color_texto, relief="flat", bd=0,
                      cursor="hand2", padx=16, pady=8)
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color))
    return boton


def crear_tarjeta_hotel(parent, hotel, precio, foto, comando):
    """Tarjeta con foto, datos del hotel y botón de reservar."""
    tarjeta = tk.Frame(parent, bg=COLOR_TARJETA, highlightthickness=1,
                       highlightbackground=COLOR_TAB)

    if foto is not None:
        etiqueta = tk.Label(tarjeta, image=foto, bg=COLOR_TARJETA, bd=0)
    else:
        etiqueta = tk.Label(tarjeta, text=TXT_SIN_FOTO, bg=hotel["color"], fg="white",
                            font=FUENTE_SUBTITULO, width=28, height=8)
    etiqueta.pack()

    cuerpo = tk.Frame(tarjeta, bg=COLOR_TARJETA)
    cuerpo.pack(fill="both", expand=True, padx=12, pady=10)

    tk.Label(cuerpo, text=hotel["nombre"], font=FUENTE_SUBTITULO,
             bg=COLOR_TARJETA, fg=hotel["color"]).pack(anchor="w")
    tk.Label(cuerpo, text=f"{hotel['ciudad']}  |  {hotel['pais']}", font=FUENTE_TEXTO,
             bg=COLOR_TARJETA, fg=COLOR_TEXTO_SUAVE).pack(anchor="w", pady=(0, 6))
    tk.Label(cuerpo, text=hotel["descripcion"], font=FUENTE_TEXTO, bg=COLOR_TARJETA,
             fg=COLOR_TEXTO, wraplength=270, justify="left").pack(anchor="w")
    tk.Label(cuerpo, text=f"Desde ${precio} USD por persona/noche", font=FUENTE_BOLD,
             bg=COLOR_TARJETA, fg=COLOR_PRECIO).pack(anchor="w", pady=8)

    crear_boton(cuerpo, TXT_ELEGIR, comando).pack(fill="x", side="bottom")
    return tarjeta