from pathlib import Path
import nbformat as n
import re

root = Path(__file__).resolve().parent.parent
p = root / 'notebooks'
h,l,r = [n.read(p / f, as_version=4) for f in ['fase1_eda.ipynb','f1_sumativo_grupo1.ipynb','rodrigo_analisis_bivariado.ipynb']]
if [len(x.cells) for x in (h,l,r)] != [14,64,16]:
    raise ValueError('Cambió la estructura de los notebooks; revisar índices antes de integrar.')
cells=[]
def md(s): cells.append(n.v4.new_markdown_cell(s))
def code(s): cells.append(n.v4.new_code_cell(s))
def src(nb,i): return nb.cells[i].source
md(src(h,0).replace('Lenin Morales\n','Lenin Morales Salas\n').replace('5. ¿Qué variables presentan valores faltantes y cómo podrían afectar el análisis?', '5. ¿Qué variables presentan valores faltantes, redundancias o filas idénticas?\n6. ¿Cómo se distribuyen edad, tarifa y tamaño familiar?\n7. ¿Cómo varía la supervivencia según tamaño familiar y la tarifa según clase?'))
md(src(h,1)); code(src(l,3)); md(src(h,3)); code(src(h,4)+'\ntitanic_raw = df.copy(deep=True)\n(raiz_proyecto / "figuras").mkdir(exist_ok=True)')
md(src(h,5)); code(src(h,6).replace('df.describe(include=["str", "bool"])','df.describe(include=["object", "string", "bool", "category"])'))
md(src(l,9)); code(src(l,10).replace('1 > 2 > 3','1: primera, 2: segunda, 3: tercera'))
md(src(h,7).split('### 7.2.')[0].replace('107 filas con valores idénticos','107 filas adicionales con valores idénticos'))
md('''## 8. Decisiones y transformaciones (pregunta 5)
Se trabaja sobre una copia independiente. Las decisiones siguientes son la propuesta metodológica de integración, sujeta a ratificación del equipo. Se conservan los datos originales.''')
code(src(l,24)); md('### D1. Filas idénticas\nSin identificador individual no se puede confirmar duplicación real. Se conservan todas las filas.'); code(src(l,26)); code('registrar("D1", "Filas idénticas", "Conservar", "No existe identificador individual", f"Filas: {len(titanic_eda)}")')
md('### D2. Redundancia\nSe conservan survived, class y embarked por su utilidad interpretativa. alone se mantiene como indicador derivado para comprobación, no como información independiente.'); code(src(l,30)); code('titanic_eda = titanic_eda.drop(columns=["alive", "pclass", "embark_town"])\nregistrar("D2", "Redundancia", "Excluir alive, pclass, embark_town", "Recodificaciones de variables conservadas", f"Columnas: {titanic_eda.shape[1]}")')
md('### D3. Cubierta\nSe excluye deck de la copia por su elevada ausencia y su distribución desigual entre clases.'); code(src(l,34)); code('titanic_eda = titanic_eda.drop(columns=["deck"])\nregistrar("D3", "Cubierta", "Excluir deck", "77,22 % faltante", f"Columnas: {titanic_eda.shape[1]}")')
md('### D4. Edad\nSe mantienen los nulos; se utilizan casos disponibles para edad. La ausencia desigual por clase puede sesgar las comparaciones.'); code(src(l,38)); code('registrar("D4", "Edad", "Sin imputación", "Evitar alterar la distribución observada", f"Nulos: {titanic_eda.age.isna().sum()}")')
md('### D5. Puerto de embarque\nSe mantienen los dos registros con puerto desconocido para no perder información de otras variables.'); code('display(titanic_raw[titanic_raw.embarked.isna()])\nregistrar("D5", "Embarque", "Conservar nulos", "No es variable central", f"Nulos: {titanic_eda.embarked.isna().sum()}")')
md(src(l,43).replace('## D6.', '### D6.').replace('*(P2, P4)*','*(preguntas 6 y 7)*')); code(src(l,44)); code(src(l,50)); code('display(pd.DataFrame(registro_decisiones))')
md('### 8.1. Variables auxiliares para visualización\nSe ordena la clase y se agrupan tamaños familiares y edades. Los intervalos etarios son cerrados a la derecha; se conserva la edad continua.'); code('''orden_clases = ["First", "Second", "Third"]
titanic_eda["class"] = pd.Categorical(titanic_eda["class"], categories=orden_clases, ordered=True)
titanic_eda["family_group"] = pd.cut(titanic_eda.family_size, [0,1,4,np.inf], labels=["Solo (1)", "Familia pequeña (2-4)", "Familia numerosa (5+)"])
titanic_eda["age_group"] = pd.cut(titanic_eda.age, [0,12,18,35,60,np.inf], include_lowest=True, labels=["0–12", ">12–18", ">18–35", ">35–60", ">60"])
assert titanic_raw.shape == (891,15)
assert len(titanic_eda) == 891
assert titanic_eda.age_group.notna().sum() == 714''')
md('## 9. Análisis univariado (pregunta 6)\nSe examinan distribuciones, dispersión y valores extremos mediante histogramas, cajas y frecuencias. La regla IQR identifica observaciones para revisión, no errores confirmados.'); code(src(l,13).replace('["survived", "pclass", "age", "sibsp", "parch", "fare"]','["age", "sibsp", "parch", "fare", "family_size"]').replace('titanic_raw','titanic_eda')); code(src(l,14));
def plot(s,num,name):
    s=re.sub(r'Figura \d+([A-C]?)',lambda m:f'Figura {num}{m[1]}',s)
    return s.replace('plt.show()',f'fig.savefig(raiz_proyecto / "figuras" / "{num:02d}_{name}.png", dpi=300, bbox_inches="tight")\nplt.show()')
code(plot(src(l,16).replace('sns.histplot(titanic_raw["pclass"], discrete=True, ax=axes[1, 1], color="darkorchid")','sns.countplot(data=titanic_raw, x="class", order=orden_clases, ax=axes[1, 1], color="darkorchid")').replace('Distribución de pclass','Frecuencia por clase'),2,'distribuciones')); code(plot(src(l,17),3,'cajas')); code(src(l,18)); code(plot(src(l,21),4,'categoricas')); code(plot(src(l,46),5,'familia'))
md('''La edad observada tiene media 29,70 y mediana 28 años. La tarifa tiene media 32,20 y mediana 14,45, coherentes con una cola derecha pronunciada. Los valores extremos no se eliminan sin evidencia de error. Predominan hombres (577 de 891), tercera clase (491 de 891) y pasajeros sin familiares registrados (537 de 891). Las comparaciones deben utilizar tasas dentro de cada grupo, no solo conteos absolutos.''')
for i in range(8,13):
    s=src(h,i)
    if h.cells[i].cell_type=='markdown': md(s.replace('8.','10.'))
    else: code(s.replace('df[','titanic_eda['))
md('## 11. Análisis bivariado\nSe comparan tasas y tamaños de grupo sin pruebas de hipótesis ni atribución causal.')
texts=[('11.1','Sexo y clase (preguntas 2 y 3)','Las mujeres presentan 74,20 % de supervivencia frente a 18,89 % de los hombres. Por clase, las tasas son 62,96 %, 47,28 % y 24,24 %. El cruce muestra diferencias descriptivas dentro de cada clase; no demuestra efectos independientes.'),('11.2','Edad (pregunta 4)','Entre los 714 casos con edad conocida, ambas medianas son 28 años. Las medias son 28,34 en sobrevivientes y 30,63 en no sobrevivientes. El tramo hasta 12 años presenta 57,97 % y el superior a 60 años 22,73 % (22 casos). La ausencia de edad limita la comparación.'),('11.3','Tamaño familiar (pregunta 7)','Los grupos de 2–4 integrantes presentan 57,88 % de supervivencia frente a 30,35 % sin familiares registrados y 16,13 % en grupos de 5 o más. La composición por clase y los tamaños pequeños pueden influir en el patrón. No se identifica a familias únicas ni se demuestra un efecto de la evacuación.'),('11.4','Tarifa y clase (pregunta 7)','Las medianas por clase son 60,29, 14,25 y 8,05. En primera clase, las medianas de sobrevivientes y no sobrevivientes son 77,96 y 44,75. Existen 15 tarifas cero cuyo origen no puede determinarse con estas variables. La transformación log1p facilita la visualización sin eliminar ceros.')]
for j,(section,title,interpretation) in enumerate(texts):
    md(f'### {section}. {title}\n'+src(r,3+3*j).split('### Acción')[1].strip().replace('diagramas de caja/violín','diagramas de caja'))
    s=src(r,4+3*j).replace('axes[0].set_xticklabels(["No sobrevivió (0)", "Sobrevivió (1)"])','axes[0].set_xticks([0, 1], ["No sobrevivió (0)", "Sobrevivió (1)"])').replace('Boxplot + Stripplot','Boxplot')
    code(plot(s,6+j,['sexo_clase','edad','familia_supervivencia','tarifas'][j])); md(interpretation)
    if j==2: code(src(l,57))
md('''## 12. Síntesis de hallazgos
| Pregunta | Evidencia | Resultado |
|---|---|---|
| 1 | §10, figura 1 | 342 de 891 sobrevivieron (38,38 %). |
| 2–3 | §11.1, figura 6 | Diferencias por sexo y clase. |
| 4 | §11.2, figura 7 | Diferencias entre tramos etarios, con 714 edades válidas. |
| 5 | §7–8 | 107 filas adicionales idénticas, redundancias y faltantes documentados. |
| 6 | §9, figuras 2–5 | Tarifa asimétrica y predominio de pasajeros sin familiares registrados. |
| 7 | §11.3–11.4, figuras 8–9 | Mayor supervivencia en grupos familiares pequeños y diferencias tarifarias por clase. |

## 13. Limitaciones
El dataset no abarca a todas las personas a bordo ni contiene identificadores individuales. Los faltantes de edad y cubierta no se distribuyen uniformemente entre clases. Los subgrupos pequeños tienen tasas sensibles a pocos casos. No se controlan factores de confusión ni se establecen relaciones causales. La tarifa registrada no permite identificar el costo individual de boletos compartidos.

## 14. Conclusiones y próximos pasos
El EDA permitió caracterizar la calidad de los datos, conservar los registros originales y describir asociaciones de supervivencia con sexo, clase, edad y tamaño familiar. En fases posteriores conviene evaluar mecanismos de ausencia de edad, estrategias de imputación y estabilidad de las asociaciones mediante métodos inferenciales o predictivos, sin anticipar sus resultados.

## 15. Reproducibilidad y referencias
Ejecutar desde la raíz o notebooks/ con las dependencias de requirements.txt y el archivo versionado datos/titanic.csv. Reiniciar el kernel y ejecutar todas las celdas. Las figuras se guardan en figuras/. Los notebooks individuales se conservan como antecedentes de los aportes.''')
code('''import hashlib
print("SHA-256 del CSV original:", hashlib.sha256(ruta_datos.read_bytes()).hexdigest())
pd.testing.assert_frame_equal(titanic_raw, pd.read_csv(ruta_datos))
assert titanic_eda.survived.sum() == 342
assert len(registro_decisiones) == 6
print("Dimensiones finales:", titanic_eda.shape)
print("Validaciones correctas")''')
md(src(l,63).replace('- Paraíso, S. (2026). *Resumen aplicado del libro: EDA mínimo viable* [Apunte]. Universidad Andrés Bello.\n','').replace('The pandas development team. (2024).','The pandas development team. (s. f.).'))
out=n.v4.new_notebook(cells=cells,metadata=h.metadata)
n.validate(out)
for c in cells:
    if c.cell_type=='code': compile(c.source,'<celda>','exec')
    if re.search(r'\b(COMPLETAR|TODO)\b',c.source): raise ValueError('Marcador de plantilla detectado')
path=p/'fase1_eda_integrado.ipynb'
if path.exists(): raise FileExistsError(f'Ya existe {path}; no se sobrescribe.')
n.write(out,path)
print(f'Generado: {path} ({len(cells)} celdas). Ejecutar desde cero para validar resultados.')
