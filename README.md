# 🧮 Calculadora de Divisas BCV para KDE Plasma

Una herramienta interactiva y autónoma diseñada para entornos Linux (especialmente optimizada para **CachyOS / Arch Linux** con escritorio **KDE Plasma**). Extrae las tasas oficiales en tiempo real del Banco Central de Venezuela, las almacena en un JSON histórico diario de forma inteligente (evitando datos basura) y provee una interfaz web local interactiva de conversión.

## 🚀 Características
- **Historial Diario Integrado:** Mantiene un registro cronológico sin duplicaciones.
- **Lógica Inteligente de Horarios:** Sabe que el BCV publica las tasas después de las 5:00 PM para el día siguiente, y rellena automáticamente los fines de semana.
- **Diseño Responsivo:** Interfaz oscura, limpia y cómoda.
- **Acceso Nativo:** Se integra directamente en el menú de aplicaciones del sistema.

## 📦 Instalación

Para instalar este proyecto en tu sistema, abre una terminal y ejecuta los siguientes comandos:

```bash
# 1. Clonar el repositorio
git clone https://github.com
cd TU_REPOSITORIO

# 2. Dar permisos al instalador y ejecutarlo
chmod +x install.sh
./install.sh
```

Al finalizar la instalación, presiona la tecla `Super` (Windows) y escribe **Calculadora BCV** para lanzar la aplicación.
