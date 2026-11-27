# Exploración Inteligente para la Ciencia de Datos

## Sumativa 1 – Fase 1

### Factores asociados a la supervivencia de los pasajeros del Titanic: un análisis exploratorio reproducible

## 1. Identificación académica

| Antecedente | Descripción |
|---|---|
| Universidad | Universidad Andrés Bello |
| Programa | Magíster en Ciencia de Datos e Inteligencia Artificial |
| Asignatura | MCDI503 – Exploración Inteligente para la Ciencia de Datos |
| Evaluación | Sumativa 1 – Fase 1 |
| Docente | Raúl Alonso |
| Año | 2026 |

## 2. Integrantes y contribuciones

| Integrante | Contribución principal |
|---|---|
| Hernán Saavedra | Configuración del proyecto, diagnóstico inicial, supervivencia general, integración, validación técnica e informe final. |
| Lenin Morales Salas | Calidad de datos, análisis univariado, decisiones exploratorias y transformaciones. |
| Rodrigo Gómez | Análisis bivariado, supervivencia según características de los pasajeros e interpretación de resultados. |

## 3. Descripción del proyecto

El proyecto desarrolla un análisis exploratorio de datos (EDA) sobre el conjunto de datos Titanic, con el propósito de identificar patrones y asociaciones descriptivas entre la supervivencia y las características demográficas, familiares y socioeconómicas registradas.

El análisis considera la calidad de los datos, distribuciones, valores faltantes, valores extremos, transformaciones justificadas y visualizaciones reproducibles.

## 4. Objetivo general

Explorar los factores asociados a la supervivencia de los pasajeros del Titanic mediante técnicas de análisis exploratorio de datos, documentando las decisiones metodológicas, los principales hallazgos y las limitaciones del estudio.

## 5. Conjunto de datos

- Fuente: repositorio seaborn-data.
- Registros originales: 891.
- Variables originales: 15.
- Variable de interés: survived.
- Archivo original: datos/titanic.csv.

Fuente original: https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv

## 6. Principales resultados

| Indicador | Resultado |
|---|---:|
| Supervivencia general | 38,38 % |
| Supervivencia femenina | 74,20 % |
| Supervivencia masculina | 18,89 % |
| Supervivencia en primera clase | 62,96 % |
| Supervivencia en segunda clase | 47,28 % |
| Supervivencia en tercera clase | 24,24 % |
| Supervivencia en grupos familiares de 2 a 4 integrantes | 57,88 % |
| Registros con edad disponible | 714 |

Los resultados corresponden a asociaciones descriptivas dentro del conjunto de datos analizado y no permiten establecer relaciones causales.

## 7. Decisiones metodológicas

| ID | Decisión |
|---|---|
| D1 | Conservar registros idénticos ante la ausencia de un identificador único. |
| D2 | Excluir variables redundantes de la copia de análisis. |
| D3 | Excluir la variable deck debido a su elevado porcentaje de datos faltantes. |
| D4 | Mantener los valores faltantes de edad sin imputación. |
| D5 | Conservar los registros sin información del puerto de embarque. |
| D6 | Construir la variable family_size para representar el tamaño del grupo familiar. |

El conjunto de datos original se conserva sin modificaciones.

## 8. Organización del repositorio

- **datos/**: conjunto de datos original y datos transformados.
- **notebooks/**: notebooks individuales y notebook final.
- **figuras/**: visualizaciones generadas durante el análisis.
- **informes/**: informe académico complementario.
- **scripts/**: scripts de descarga, integración y preparación.
- **requirements.txt**: dependencias del proyecto.

## 9. Instalación y reproducibilidad

### Clonar el repositorio

```bash
git clone https://github.com/hernansaavedrag/exploracion-inteligente-datos.git
cd exploracion-inteligente-datos
```

### Crear el entorno virtual

```bash
python -m venv .venv
```

### Activar el entorno virtual en Windows mediante Git Bash

```bash
source .venv/Scripts/activate
```

### Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### Descargar los datos si no están disponibles

```bash
python scripts/descargar_datos.py
```

### Registrar el kernel

```bash
python -m ipykernel install --user --name exploracion-datos --display-name "Python 3.11 - Magister EDA"
```

### Ejecutar el notebook completo

```bash
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=exploracion-datos --ExecutePreprocessor.timeout=600 notebooks/fase1_eda_final.ipynb
```

Se recomienda utilizar Python 3.11.

## 10. Entregables académicos

- [Notebook definitivo ejecutado](notebooks/fase1_eda_final.ipynb)
- [Informe académico complementario](informes/Informe_Sumativa1_Fase1_Titanic_Final.pdf)

## 11. Trabajo colaborativo

El desarrollo se organizó mediante ramas individuales de Git, commits identificables y una rama de integración grupal:

- hernan-fase1
- lenin-fase1
- rodrigo-fase1
- fase1-integracion
- main

Esta metodología permite mantener la trazabilidad de los aportes individuales y consolidar los resultados en una entrega grupal reproducible.

## 12. Limitaciones y próximos pasos

El análisis reconoce la presencia de datos faltantes, posibles sesgos de selección, ausencia de identificadores únicos y potenciales factores de confusión.

Como continuación, se propone profundizar en el análisis multivariado, evaluar estrategias alternativas de tratamiento de datos faltantes y explorar modelos predictivos de supervivencia.

## 13. Referencias

Las referencias bibliográficas completas, en formato APA 7, se encuentran en el notebook definitivo y en el informe académico complementario.

---

Magíster en Ciencia de Datos e Inteligencia Artificial
Universidad Andrés Bello – 2026