# Ubigeo Perú 2026 🇵🇪

Base de datos completa y normalizada de los Departamentos, Provincias y Distritos del Perú (UBIGEO), actualizada al año **2026**. 

Este repositorio proporciona la información estructurada con sus respectivas llaves foráneas (`department_id`, `province_id`) lista para ser integrada en cualquier sistema de bases de datos, APIs o aplicaciones web.

## 📄 Fuente de los Datos
Los datos originales fueron extraídos del **Directorio Nacional de Municipalidades Provinciales y Distritales (2026)** publicado por el Instituto Nacional de Estadística e Informática (INEI).
🔗 [Enlace oficial al documento del INEI](https://www.gob.pe/institucion/inei/informes-publicaciones/3908763-directorio-nacional-de-municipalidades-provinciales-y-distritales-abril-2026)

## 📂 Estructura de Formatos Disponibles
Para facilitar su uso en cualquier tecnología, la base de datos ya se encuentra procesada y exportada en los siguientes formatos dentro de sus respectivas carpetas:

* `/csv` - Archivos separados por comas (ideal para análisis de datos y Excel).
* `/json` - Formato ligero de intercambio de datos (ideal para APIs y NoSQL).
* `/php_arrays` - Arreglos nativos listos para incluir en proyectos PHP.
* `/sql` - Consultas `INSERT INTO` listas para poblar bases de datos relacionales (MySQL, PostgreSQL).
* `/xml` - Estructura de etiquetas para sistemas legacy o integraciones SOAP.
* `/yaml` - Formato legible por humanos, útil para configuraciones.

## 🛠️ Estructura de las Tablas (Relacional)

* **Departamentos:** `id` (2 dígitos), `name`
* **Provincias:** `id` (4 dígitos), `name`, `department_id`
* **Distritos:** `id` (6 dígitos), `name`, `province_id`, `department_id`

---

## 🚀 ¿Cómo ejecutar el script generador?
Si deseas ver cómo se limpiaron los datos o generar los archivos por tu cuenta a partir del Excel original, puedes ejecutar el script de Python `normalizador.py`.

### Prerrequisitos
Asegúrate de tener instalado [Python 3.8+](https://www.python.org/downloads/) en tu sistema.

### Paso a paso

**1. Clonar el repositorio**
```bash
git clone https://github.com/leandrofrancisco03/ubigeo-peru-2026.git
cd ubigeo-peru-2026
```

**2. Crear y activar un entorno virtual**
Es una buena práctica para no interferir con las librerías globales de tu sistema.
* En **Windows**:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
* En **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

**3. Instalar las dependencias**
El proyecto incluye un archivo `requirements.txt` con las versiones exactas de las librerías necesarias (`pandas`, `openpyxl`, `pyyaml`).
```bash
pip install -r requirements.txt
```

**4. Ejecutar el script normalizador**
```bash
python normalizador.py
```

Al finalizar, verás un mensaje de confirmación y todas las carpetas se habrán generado automáticamente con la data limpia y estructurada.

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si encuentras alguna anomalía en los nombres de los distritos o deseas agregar un nuevo formato de exportación, siéntete libre de hacer un *Fork* del repositorio y enviar un *Pull Request*.
