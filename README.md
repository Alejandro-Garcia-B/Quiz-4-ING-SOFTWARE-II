# 🏝️ Decameron - Sistema de Reservas

Aplicación de escritorio en **Python (Tkinter)** para reservar hoteles Decameron de
Latinoamérica. Muestra cada hotel con su foto, permite reservar eligiendo número de
personas, duración y tipo de habitación, y tiene un despacho con todas las reservas.

## Hoteles disponibles

| # | Hotel | País |
|---|-------|------|
| 1 | Decameron Barú (Cartagena) | Colombia |
| 2 | Decameron Panamá | Panamá |
| 3 | Decameron Punta Sal | Perú |

## Estructura del proyecto

```
decameron-reservas/
├── main.py            # Lógica: reservas, cálculo de precios, ventana y guardado
├── decoracion.py      # Visual: colores, fuentes, textos, imágenes y widgets
├── imagenes/          # Fotos de los hoteles (puedes reemplazarlas por las tuyas)
├── requirements.txt
├── README.md
└── .gitignore
```

## Requisitos

- Python 3.8 o superior (con Tkinter, que viene incluido en Windows y macOS)
- Pillow: `pip install -r requirements.txt` (permite usar fotos JPG y ajustarlas)

## Cómo ejecutarlo

```bash
git clone https://github.com/Alejandro-Garcia-B/Quiz-4-ING-SOFTWARE-II.git
cd decameron-reservas
pip install -r requirements.txt
python main.py
```

## Cómo se usa

La ventana tiene tres pestañas:

1. **Hoteles**: tarjetas con foto, ubicación, descripción y precio. El botón
   *Reservar aquí* lleva al formulario con ese hotel ya elegido.
2. **Reservar**: nombre del cliente, hotel, personas, noches y tipo de habitación
   (Estándar, Superior o Suite). El total se calcula en vivo.
3. **Despacho**: tabla con todas las reservas, el total general y un botón para
   cancelar la reserva seleccionada.

## Cálculo del precio

```
total = precio base del hotel × multiplicador de habitación × personas × noches
```

| Habitación | Multiplicador |
|------------|---------------|
| Estándar | x1.0 |
| Superior | x1.3 |
| Suite | x1.8 |

> Los precios son ilustrativos, no corresponden a tarifas reales.

