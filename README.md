# Great Expectations - Demostración Básica y Avanzada

Este directorio contiene una demostración de la funcionalidad básica y avanzada de **Great Expectations** como herramienta para la elaboración y monitoreo de calidad de datos. Se utiliza un conjunto de datos sintéticos de transacciones de tarjetas de crédito para ilustrar cómo implementar expectativas de calidad de datos en las dimensiones de **exactitud** y **completitud**.

## Requisitos

- **Python 3.9** (asegúrate de tener esta versión instalada en tu sistema).
- Crear un ambiente virtual con `venv`.
- Instalar las dependencias listadas en el archivo `requirements.txt`.

## Configuración del Entorno

Sigue estos pasos para configurar el entorno y ejecutar el proyecto:

1. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_DIRECTORIO>

2. **Crear un ambiente virtual**:
   ```bash
   python3.9 -m venv .venv

3. **Activar el ambiente virtual**:
    ```bash
    source .venv/bin/activate

4. **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt

## Uso
1. Abre una terminal y navega al directorio GreatExpectations/. 
2. Inicia Jupyter Notebook para ejecutar los notebooks desde el navegador:

    ```bash
    jupyter notebooks

3. Abre el archivo **BasicDemostrationGE.ipynb** y ejecuta las celdas para realizar las validaciones de calidad de datos.