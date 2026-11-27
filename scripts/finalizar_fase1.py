
from pathlib import Path
import nbformat

raiz = Path(__file__).resolve().parent.parent

origen = raiz / "notebooks" / "fase1_eda_perfeccionado.ipynb"
destino = raiz / "notebooks" / "fase1_eda_final.ipynb"

nb = nbformat.read(origen, as_version=4)

# 1. Incorporar el nombre del docente
docente = "**Docente:** Raúl Alonso"

if "Raúl Alonso" not in nb.cells[0].source:
    nb.cells[0].source += "\n\n" + docente

# 2. Incorporar fundamentación académica
fundamentacion = (
    "El proceso exploratorio sigue un enfoque de EDA mínimo "
    "viable, orientado a formular preguntas, examinar la "
    "calidad de los datos, justificar las decisiones "
    "metodológicas y documentar los hallazgos de manera "
    "reproducible (Paraíso, 2026)."
)

for celda in nb.cells:
    if celda.cell_type == "markdown":
        if "contexto" in celda.source.lower():
            if fundamentacion not in celda.source:
                celda.source += "\n\n" + fundamentacion
            break

# 3. Incorporar referencia bibliográfica docente
referencia = (
    "Paraíso, S. (2026). *Resumen aplicado del libro: "
    "EDA mínimo viable* [Apunte]. Universidad Andrés Bello."
)

referencias = [
    celda for celda in nb.cells
    if celda.cell_type == "markdown"
    and "referencias" in celda.source.lower()
]

if not referencias:
    raise ValueError("No se encontró la sección de referencias.")

ultima = referencias[-1]

if referencia not in ultima.source:
    ultima.source += "\n\n" + referencia

# 4. Validar estructura y ejecución
nbformat.validate(nb)

codigo = [
    celda for celda in nb.cells
    if celda.cell_type == "code"
]

sin_ejecutar = [
    celda for celda in codigo
    if celda.execution_count is None
]

errores = [
    salida
    for celda in codigo
    for salida in celda.get("outputs", [])
    if salida.output_type == "error"
]

assert not sin_ejecutar, "Existen celdas sin ejecutar."
assert not errores, "Existen errores de ejecución."

# 5. Guardar versión final sin sobrescribir el original
if destino.exists():
    raise FileExistsError(destino)

nbformat.write(nb, destino)

print("=" * 60)
print("CIERRE ACADEMICO FASE 1")
print("=" * 60)
print("Docente: Raúl Alonso")
print("Referencia docente incorporada")
print("Total de celdas:", len(nb.cells))
print("Celdas de codigo:", len(codigo))
print("Celdas sin ejecutar:", len(sin_ejecutar))
print("Errores:", len(errores))
print("Archivo generado:", destino)
print("VALIDACION CORRECTA")
