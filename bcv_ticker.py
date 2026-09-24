#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import urllib3
import json
import os
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obtener_fechas_vigencia():
    """
    Calcula para qué fechas aplica la tasa actual según la hora y el día del BCV.
    Toma en cuenta que después de las 5:00 PM (17:00) la tasa es para el siguiente día hábil.
    """
    ahora = datetime.now()
    hora_bcv_cambio = 17  # 5:00 PM

    # Si ya pasó la hora de actualización, la tasa aplica a partir de "mañana"
    if ahora.hour >= hora_bcv_cambio:
        fecha_base = ahora + timedelta(days=1)
    else:
        fecha_base = ahora

    # Si la fecha base cae viernes, sábado o domingo, esa tasa cubre todo el fin de semana largo hasta el lunes
    # dia_semana: 0=Lunes, 4=Viernes, 5=Sábado, 6=Domingo
    dia_semana = fecha_base.weekday()

    fechas_a_registrar = []

    if dia_semana == 4: # Es Viernes (Aplica para Viernes, Sábado, Domingo y Lunes)
        for i in range(4):
            f = fecha_base + timedelta(days=i)
            fechas_a_registrar.append(f.strftime("%Y-%m-%d"))
    elif dia_semana == 5: # Es Sábado (Aplica para Sábado, Domingo y Lunes)
        for i in range(3):
            f = fecha_base + timedelta(days=i)
            fechas_a_registrar.append(f.strftime("%Y-%m-%d"))
    elif dia_semana == 6: # Es Domingo (Aplica para Domingo y Lunes)
        for i in range(2):
            f = fecha_base + timedelta(days=i)
            fechas_a_registrar.append(f.strftime("%Y-%m-%d"))
    else:
        # Días normales entre semana (Lunes, Martes, Miércoles, Jueves)
        fechas_a_registrar.append(fecha_base.strftime("%Y-%m-%d"))

    return fechas_a_registrar

def actualizar_historial_inteligente():
    url = "https://bcv.org.ve"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
    ruta_guardado = os.path.expanduser("~/.local/share/bcv-calculator/tasas.json")

    # 1. Cargar el historial existente
    historial = {}
    if os.path.exists(ruta_guardado):
        try:
            with open(ruta_guardado, 'r') as f:
                historial = json.load(f)
        except Exception:
            historial = {}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code != 200:
            print("❌ No se pudo conectar con el portal del BCV.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        tasas_dia = {}
        divisas = {'USD': 'dolar', 'EUR': 'euro'}

        for codigo, id_html in divisas.items():
            contenedor = soup.find('div', id=id_html)
            if contenedor:
                val_box = contenedor.find('strong')
                if val_box:
                    valor = float(val_box.text.strip().replace('.', '').replace(',', '.'))
                    tasas_dia[codigo] = valor

        if tasas_dia:
            # 2. Obtener el rango de fechas que cubrirá esta tasa extraída
            fechas_destino = obtener_fechas_vigencia()
            cambios_realizados = False

            for fecha in fechas_destino:
                # Verificamos si la fecha ya existe y si tiene los mismos valores exactos
                if fecha in historial:
                    guardado = historial[fecha]
                    if guardado.get('USD') == tasas_dia['USD'] and guardado.get('EUR') == tasas_dia['EUR']:
                        continue # Si es idéntico, saltamos para evitar sobreescritura basura

                # Si es una fecha nueva o cambió la tasa, la agregamos/actualizamos
                historial[fecha] = tasas_dia
                cambios_realizados = True
                print(f"📝 Tasa asignada a la fecha: {fecha}")

            # 3. Guardar en el archivo únicamente si hubo novedades
            if cambios_realizados:
                # Ordenar el JSON por fechas (opcional, para mantener el archivo visualmente impecable)
                historial_ordenado = dict(sorted(historial.items()))

                with open(ruta_guardado, 'w') as f:
                    json.dump(historial_ordenado, f, indent=2)
                print("✅ ¡Archivo tasas.json actualizado con éxito!")
            else:
                print("ℹ️ No se detectaron fechas nuevas ni cambios de tasas en el BCV. Todo al día.")

    except Exception as e:
        print(f"❌ Error al procesar la actualización: {e}")

if __name__ == "__main__":
    actualizar_historial_inteligente()
