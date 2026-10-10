"""
main.py
-------
Funcionamiento interno del sistema de reservas Decameron (interfaz con Tkinter).
Todo lo visual (colores, fuentes, textos, imágenes) está en decoracion.py.
"""

import json
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

import decoracion as d

# Precio base por persona por noche (USD) de cada hotel (ilustrativo)
PRECIO_BASE = {1: 180, 2: 150, 3: 140}

# Tipos de habitación: nombre -> multiplicador del precio
TIPOS_HABITACION = {
    "Estandar": 1.0,
    "Superior": 1.3,
    "Suite": 1.8,
}

MAX_PERSONAS = 10
MAX_NOCHES = 30


# ---------------------------------------------------------------------------
# Persistencia (las reservas se guardan junto al programa / .exe)
# ---------------------------------------------------------------------------
def carpeta_datos():
    if getattr(sys, "frozen", False):  # corriendo como .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


ARCHIVO_RESERVAS = os.path.join(carpeta_datos(), "reservas.json")


def cargar_reservas():
    if os.path.exists(ARCHIVO_RESERVAS):
        try:
            with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def guardar_reservas(reservas):
    with open(ARCHIVO_RESERVAS, "w", encoding="utf-8") as f:
        json.dump(reservas, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Lógica de negocio
# ---------------------------------------------------------------------------
def calcular_total(id_hotel, tipo_habitacion, personas, noches):
    return PRECIO_BASE[id_hotel] * TIPOS_HABITACION[tipo_habitacion] * personas * noches


# ---------------------------------------------------------------------------
# Aplicación
# ---------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(d.TITULO_VENTANA)
        self.geometry("1020x740")
        self.minsize(960, 700)
        self.configure(bg=d.COLOR_FONDO)
        d.aplicar_estilos(self)

        self.reservas = cargar_reservas()
        self.ids_hotel = list(d.HOTELES.keys())
        self.fotos = {}  # guarda las imágenes para que Tkinter no las borre

        d.crear_encabezado(self).pack(fill="x")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=12)

        self._crear_tab_hoteles()
        self._crear_tab_reservar()
        self._crear_tab_despacho()

        self._mostrar_vista_hotel()
        self._actualizar_total()
        self._refrescar_despacho()
    # ------------------------------------------------------------------ Hoteles
    def _crear_tab_hoteles(self):
        tab = tk.Frame(self.notebook, bg=d.COLOR_FONDO)
        self.notebook.add(tab, text=d.TAB_HOTELES)

        for id_hotel, hotel in d.HOTELES.items():
            foto = d.cargar_imagen(hotel["imagen"], 290, 190)
            self.fotos[("tarjeta", id_hotel)] = foto
            tarjeta = d.crear_tarjeta_hotel(
                tab, hotel, PRECIO_BASE[id_hotel], foto,
                lambda i=id_hotel: self._elegir_hotel(i),
            )
            tarjeta.pack(side="left", fill="both", expand=True, padx=8, pady=12)

    def _elegir_hotel(self, id_hotel):
        """Se llama al pulsar 'Reservar aqui' en una tarjeta."""
        self.cb_hotel.current(self.ids_hotel.index(id_hotel))
        self._al_cambiar_hotel()
        self.notebook.select(self.tab_reservar)

    # ------------------------------------------------------------------ Reservar
    def _crear_tab_reservar(self):
        self.tab_reservar = tk.Frame(self.notebook, bg=d.COLOR_FONDO)
        self.notebook.add(self.tab_reservar, text=d.TAB_RESERVAR)

        form = tk.Frame(self.tab_reservar, bg=d.COLOR_TARJETA, padx=24, pady=20)
        form.pack(side="left", fill="both", expand=True, padx=8, pady=12)
        vista = tk.Frame(self.tab_reservar, bg=d.COLOR_TARJETA, padx=16, pady=16)
        vista.pack(side="left", fill="y", padx=(0, 8), pady=12)

        self.var_nombre = tk.StringVar()
        self.var_personas = tk.StringVar(value="2")
        self.var_noches = tk.StringVar(value="3")
        self.var_tipo = tk.StringVar(value=list(TIPOS_HABITACION)[0])
        self.var_total = tk.StringVar()

        tk.Label(form, text="Nueva reserva", font=d.FUENTE_SUBTITULO,
                 bg=d.COLOR_TARJETA, fg=d.COLOR_PRIMARIO).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        def etiqueta(texto, fila):
            tk.Label(form, text=texto, font=d.FUENTE_BOLD, bg=d.COLOR_TARJETA,
                     fg=d.COLOR_TEXTO).grid(row=fila, column=0, sticky="w", pady=10)

        etiqueta("Nombre del cliente", 1)
        tk.Entry(form, textvariable=self.var_nombre, font=d.FUENTE_TEXTO, width=28).grid(
            row=1, column=1, sticky="w", padx=12)

        etiqueta("Hotel", 2)
        self.cb_hotel = ttk.Combobox(
            form, state="readonly", width=30, font=d.FUENTE_TEXTO,
            values=[f"{h['nombre']} - {h['pais']}" for h in d.HOTELES.values()],
        )
        self.cb_hotel.current(0)
        self.cb_hotel.grid(row=2, column=1, sticky="w", padx=12)
        self.cb_hotel.bind("<<ComboboxSelected>>", lambda e: self._al_cambiar_hotel())

        etiqueta(f"Personas (1-{MAX_PERSONAS})", 3)
        tk.Spinbox(form, from_=1, to=MAX_PERSONAS, textvariable=self.var_personas,
                   width=8, font=d.FUENTE_TEXTO).grid(row=3, column=1, sticky="w", padx=12)

        etiqueta(f"Duracion en noches (1-{MAX_NOCHES})", 4)
        tk.Spinbox(form, from_=1, to=MAX_NOCHES, textvariable=self.var_noches,
                   width=8, font=d.FUENTE_TEXTO).grid(row=4, column=1, sticky="w", padx=12)

        etiqueta("Tipo de habitacion", 5)
        ttk.Combobox(form, state="readonly", width=18, font=d.FUENTE_TEXTO,
                     textvariable=self.var_tipo,
                     values=list(TIPOS_HABITACION)).grid(row=5, column=1, sticky="w", padx=12)

        tk.Label(form, textvariable=self.var_total, font=d.FUENTE_TOTAL,
                 bg=d.COLOR_TARJETA, fg=d.COLOR_PRECIO).grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(24, 12))

        d.crear_boton(form, d.TXT_CONFIRMAR, self._confirmar_reserva).grid(
            row=7, column=0, columnspan=2, sticky="w")

        # Recalcular el total cada vez que cambia algo
        for var in (self.var_personas, self.var_noches, self.var_tipo):
            var.trace_add("write", lambda *args: self._actualizar_total())

        # Vista previa del hotel elegido
        self.lbl_vista_foto = tk.Label(vista, bg=d.COLOR_TARJETA)
        self.lbl_vista_foto.pack()
        self.lbl_vista_nombre = tk.Label(vista, font=d.FUENTE_SUBTITULO, bg=d.COLOR_TARJETA)
        self.lbl_vista_nombre.pack(pady=(10, 0))
        self.lbl_vista_ciudad = tk.Label(vista, font=d.FUENTE_TEXTO, bg=d.COLOR_TARJETA,
                                         fg=d.COLOR_TEXTO_SUAVE)
        self.lbl_vista_ciudad.pack()

    def _id_hotel_actual(self):
        return self.ids_hotel[self.cb_hotel.current()]

    def _al_cambiar_hotel(self):
        self._mostrar_vista_hotel()
        self._actualizar_total()

    def _mostrar_vista_hotel(self):
        hotel = d.HOTELES[self._id_hotel_actual()]
        foto = d.cargar_imagen(hotel["imagen"], 300, 200)
        self.fotos["vista"] = foto
        if foto is not None:
            self.lbl_vista_foto.config(image=foto, text="", width=0, height=0)
        else:
            self.lbl_vista_foto.config(image="", text=d.TXT_SIN_FOTO, bg=hotel["color"],
                                       fg="white", font=d.FUENTE_SUBTITULO,
                                       width=30, height=10)
        self.lbl_vista_nombre.config(text=hotel["nombre"], fg=hotel["color"])
        self.lbl_vista_ciudad.config(text=f"{hotel['ciudad']} | {hotel['pais']}")

    @staticmethod
    def _leer_numero(variable, minimo, maximo):
        """Devuelve el entero de la variable o None si no es válido."""
        try:
            valor = int(variable.get())
        except ValueError:
            return None
        return valor if minimo <= valor <= maximo else None

    def _actualizar_total(self):
        personas = self._leer_numero(self.var_personas, 1, MAX_PERSONAS)
        noches = self._leer_numero(self.var_noches, 1, MAX_NOCHES)
        if personas is None or noches is None:
            self.var_total.set("Total: --")
            return
        total = calcular_total(self._id_hotel_actual(), self.var_tipo.get(), personas, noches)
        self.var_total.set(f"Total: ${total:,.0f} USD")

    def _confirmar_reserva(self):
        cliente = self.var_nombre.get().strip()
        personas = self._leer_numero(self.var_personas, 1, MAX_PERSONAS)
        noches = self._leer_numero(self.var_noches, 1, MAX_NOCHES)

        if not cliente:
            messagebox.showwarning("Datos incompletos", "Escribe el nombre del cliente.")
            return
        if personas is None:
            messagebox.showwarning("Datos invalidos",
                                   f"Las personas deben ser un numero entre 1 y {MAX_PERSONAS}.")
            return
        if noches is None:
            messagebox.showwarning("Datos invalidos",
                                   f"Las noches deben ser un numero entre 1 y {MAX_NOCHES}.")
            return

        id_hotel = self._id_hotel_actual()
        tipo = self.var_tipo.get()
        reserva = {
            "id": max((r["id"] for r in self.reservas), default=0) + 1,
            "cliente": cliente,
            "hotel": d.HOTELES[id_hotel]["nombre"],
            "personas": personas,
            "noches": noches,
            "habitacion": tipo,
            "total": calcular_total(id_hotel, tipo, personas, noches),
        }
        self.reservas.append(reserva)
        try:
            guardar_reservas(self.reservas)
        except OSError as error:
            messagebox.showerror("Error al guardar", f"No se pudo guardar la reserva:\n{error}")
            return

        self._refrescar_despacho()
        messagebox.showinfo(
            "Reserva confirmada",
            f"Reserva N° {reserva['id']}\n\n"
            f"Cliente: {cliente}\nHotel: {reserva['hotel']}\n"
            f"Personas: {personas}\nNoches: {noches}\nHabitacion: {tipo}\n\n"
            f"Total: ${reserva['total']:,.0f} USD",
        )
        self.var_nombre.set("")
        self.notebook.select(self.tab_despacho)

    # ------------------------------------------------------------------ Despacho
    def _crear_tab_despacho(self):
        self.tab_despacho = tk.Frame(self.notebook, bg=d.COLOR_FONDO)
        self.notebook.add(self.tab_despacho, text=d.TAB_DESPACHO)

        marco = tk.Frame(self.tab_despacho, bg=d.COLOR_FONDO)
        marco.pack(fill="both", expand=True, padx=8, pady=12)

        columnas = (
            ("id", "N°", 50), ("cliente", "Cliente", 170), ("hotel", "Hotel", 200),
            ("personas", "Personas", 80), ("noches", "Noches", 80),
            ("habitacion", "Habitacion", 110), ("total", "Total (USD)", 120),
        )
        self.tabla = ttk.Treeview(marco, columns=[c[0] for c in columnas],
                                  show="headings", selectmode="browse")
        for clave, titulo, ancho in columnas:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, anchor="center")

        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")

        pie = tk.Frame(self.tab_despacho, bg=d.COLOR_FONDO)
        pie.pack(fill="x", padx=8, pady=(0, 12))
        self.lbl_resumen = tk.Label(pie, font=d.FUENTE_TOTAL, bg=d.COLOR_FONDO,
                                    fg=d.COLOR_PRIMARIO)
        self.lbl_resumen.pack(side="left")
        d.crear_boton(pie, d.TXT_CANCELAR_RESERVA, self._cancelar_reserva,
                      color=d.COLOR_PELIGRO, color_hover="#E74C3C",
                      color_texto="white").pack(side="right")

    def _refrescar_despacho(self):
        self.tabla.delete(*self.tabla.get_children())
        for r in self.reservas:
            self.tabla.insert("", "end", values=(
                r["id"], r["cliente"], r["hotel"], r["personas"], r["noches"],
                r["habitacion"], f"${r['total']:,.0f}",
            ))
        total = sum(r["total"] for r in self.reservas)
        self.lbl_resumen.config(
            text=f"{len(self.reservas)} reserva(s)  |  Total general: ${total:,.0f} USD")

    def _cancelar_reserva(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Cancelar reserva", "Selecciona primero una reserva de la tabla.")
            return
        id_reserva = int(self.tabla.item(seleccion[0])["values"][0])
        if not messagebox.askyesno("Cancelar reserva",
                                   f"¿Seguro que quieres cancelar la reserva N° {id_reserva}?"):
            return
        self.reservas = [r for r in self.reservas if r["id"] != id_reserva]
        guardar_reservas(self.reservas)
        self._refrescar_despacho()


if __name__ == "__main__":
    App().mainloop()
