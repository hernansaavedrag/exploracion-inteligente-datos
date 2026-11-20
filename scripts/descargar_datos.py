import seaborn as sns
from pathlib import Path

# 1. Obtener el dataset Titanic
df = sns.load_dataset("titanic")

# 2. Definir la ruta del archivo CSV
ruta = Path(__file__).resolve().parent.parent / "datos" / "titanic.csv"

# 3. Guardar el dataset
df.to_csv(ruta, index=False)

# 4. Verificar los datos descargados
print("Dataset Titanic descargado correctamente")
print(f"Registros: {df.shape[0]}")
print(f"Variables: {df.shape[1]}")
print(f"Archivo guardado en: {ruta}")
print("\nPrimeros cinco registros:")
print(df.head())
