from pathlib import Path
import nbformat

root = Path(__file__).resolve().parent.parent
src = root / 'notebooks/fase1_eda_integrado.ipynb'
dst = root / 'notebooks/fase1_eda_perfeccionado.ipynb'
nb = nbformat.read(src, as_version=4)
if len(nb.cells) != 63 or 'tipo_estadistico' not in nb.cells[8].source or 'SHA-256' not in nb.cells[61].source:
    raise ValueError('La estructura no coincide con el notebook integrado revisado.')
if dst.exists():
    raise FileExistsError(f'Ya existe {dst}; conservar o renombrar antes de repetir.')

def add(i, text):
    nb.cells[i].source += '\n\n' + text.strip() + '\n'

add(0, 'El enfoque combina resúmenes robustos, visualizaciones y revisión de calidad antes del modelamiento, en línea con Bruce et al. (2020). La fuente de los registros es Waskom (s. f.).')
add(1, 'Pandas facilita la manipulación tabular (The pandas development team, s. f.) y seaborn permite representar distribuciones y relaciones estadísticas (Waskom, 2021).')
desc = {'survived':'Supervivencia: 0 no, 1 sí','pclass':'Clase del boleto: 1, 2 o 3','sex':'Sexo registrado','age':'Edad en años','sibsp':'Hermanos y cónyuges a bordo','parch':'Padres e hijos a bordo','fare':'Tarifa registrada del boleto','embarked':'Puerto de embarque: C, Q o S','class':'Clase del boleto en texto','who':'Categoría hombre, mujer o niño','adult_male':'Indicador de hombre adulto','deck':'Cubierta registrada','embark_town':'Nombre del puerto de embarque','alive':'Supervivencia en texto','alone':'Sin hermanos, cónyuges, padres o hijos registrados a bordo'}
nb.cells[8].source = nb.cells[8].source.rsplit('\ndiccionario',1)[0] + '\n\ndescripciones = ' + repr(desc) + '\ndiccionario.insert(0, "descripcion", pd.Series(descripciones))\ndisplay(diccionario)'
add(12,'Eliminar filas idénticas reduciría el tamaño de la muestra sin garantizar que se eliminen registros de la misma persona. Se privilegia conservar información y documentar la incertidumbre.')
add(15,'Las tablas cruzadas respaldan la selección de una representación por concepto. `who` y `adult_male` se conservan como atributos auxiliares relacionados con sexo y edad, no como variables independientes por definición.')
add(18,'La ausencia de cubierta alcanza 19,0 %, 91,3 % y 97,6 % en primera, segunda y tercera clase, respectivamente. Imputar o asignar una categoría desconocida son alternativas, pero no recuperan la cubierta real. Se excluye del análisis principal sin eliminar pasajeros.')
add(21,'La ausencia de edad es 13,9 %, 6,0 % y 27,7 % por clase. Imputar con la media podría reducir artificialmente la dispersión; eliminar filas de todo el análisis descartaría información válida de otras variables. Se utilizan 714 casos disponibles únicamente para comparaciones de edad. La distribución desigual de faltantes no demuestra por sí sola un mecanismo específico de ausencia.')
add(30,'**Variables auxiliares:** `family_group` agrupa tamaños 1, 2–4 y 5 o más para evitar fragmentar excesivamente los grupos; `age_group` utiliza intervalos cerrados a la derecha (0–12, más de 12 hasta 18, más de 18 hasta 35, más de 35 hasta 60 y más de 60); conserva las edades faltantes. `log_fare = log(1 + fare)` se incorpora en §11.4 para visualizar tarifas asimétricas sin perder ceros. Estas transformaciones no sustituyen las variables originales conservadas.')
add(40,'La regla de 1,5 veces el rango intercuartílico (Bruce et al., 2020) identifica 11 edades extremas entre 714 observadas (1,54 %) y 116 tarifas extremas entre 891 registros (13,02 %). Son observaciones para revisar, no errores demostrados. La tarifa alcanza 512,33 y la edad 80 años; se conservan porque no existe evidencia suficiente para descartarlas. Los gráficos de caja complementan los histogramas al mostrar dispersión y colas.')
add(49,'La brecha por sexo es 55,31 puntos porcentuales. Entre primera y tercera clase alcanza 38,72 puntos. En mujeres, las tasas por clase son 96,81 %, 92,11 % y 50,00 %; en hombres, 36,89 %, 15,74 % y 13,54 %. La comparación conjunta (figura 6) muestra que la diferencia por sexo persiste descriptivamente en las tres clases, aunque su magnitud cambia. Los denominadores de cada combinación deben considerarse antes de interpretar las tasas. No se han estimado efectos ajustados ni interacciones estadísticas.')
add(52,'Los tramos intermedios registran 42,86 %, 38,27 % y 40,00 %, respectivamente. La diferencia entre los extremos es 35,24 puntos porcentuales, pero el tramo mayor de 60 años solo contiene 22 casos. La igualdad de medianas no implica igualdad de distribuciones. Los resultados de la figura 7 sugieren explorar relaciones no lineales en una fase posterior, considerando el posible sesgo por edades faltantes.')
add(55,'Los denominadores son 537, 292 y 62 pasajeros, con 163, 169 y 10 sobrevivientes. La brecha entre grupos de 2–4 y viajeros sin familiares registrados es 27,53 puntos porcentuales. Los tamaños 8 y 11 tienen solo 6 y 7 observaciones, respectivamente. La tabla siguiente muestra que los tamaños 7, 8 y 11 corresponden íntegramente a tercera clase; por ello conviene evaluar conjuntamente clase y tamaño familiar antes de atribuir diferencias a este último.')
add(59,'Los IQR por clase son 62,58, 13,00 y 7,75; primera clase presenta la mayor dispersión. Las medianas de no sobrevivientes frente a sobrevivientes son 44,75 frente a 77,96 en primera, 13,00 frente a 21,00 en segunda y 8,05 frente a 8,52 en tercera. La figura 9 muestra que la asociación descriptiva entre tarifa y supervivencia varía por clase. No se demuestra que pagar más cause una mayor supervivencia.')
nb.cells[60].source = '''## 12. Síntesis de hallazgos
| Pregunta | Evidencia | Respuesta |
|---|---|---|
| P1. Supervivencia general | §10, figura 1 | 342/891 (38,38 %) sobrevivieron. |
| P2. Sexo | §11.1, figura 6 | Mujeres 74,20 %; hombres 18,89 %. |
| P3. Clase | §11.1, figura 6 | Primera 62,96 %, segunda 47,28 %, tercera 24,24 %. |
| P4. Edad | §11.2, figura 7 | Hasta 12 años: 57,97 %; mayores de 60: 22,73 %; 714 edades válidas. |
| P5. Calidad | §7–8, D1–D6 | 107 filas adicionales idénticas; cubierta 77,22 % y edad 19,87 % faltantes; tres recodificaciones excluidas. |
| P6. Distribuciones | §9, figuras 2–5 | Edad: mediana 28; tarifa: mediana 14,45 y media 32,20; 537 pasajeros sin familiares registrados. |
| P7. Familia y tarifa | §11.3–11.4, figuras 8–9 | Supervivencia 30,35 %, 57,88 % y 16,13 % por grupo familiar; medianas tarifarias 60,29, 14,25 y 8,05 por clase. |

## 13. Supuestos y limitaciones
Se asume que las codificaciones del CSV describen los registros disponibles. No se conoce un diseño de muestreo que permita generalizar a todas las personas a bordo. La falta de identificadores impide confirmar duplicaciones reales o identificar familias únicas. La ausencia de edad y cubierta varía por clase; los análisis con casos disponibles pueden presentar sesgo de selección. Las tasas de grupos pequeños son sensibles a pocos registros. La tarifa registrada no permite establecer el costo individual de boletos compartidos. Las comparaciones son descriptivas y no controlan factores de confusión ni demuestran causalidad.

## 14. Conclusiones y próximos pasos
El análisis responde las siete preguntas y conserva las 891 observaciones originales. Las diferencias por sexo y clase son marcadas: la supervivencia femenina supera a la masculina en 55,31 puntos porcentuales y la primera clase supera a la tercera en 38,72 puntos. La edad y el tamaño familiar muestran patrones descriptivos no monotónicos que no se resumen adecuadamente con una sola media. La tarifa presenta asimetría positiva y diferencias entre clases. Las decisiones D1–D6 mantienen trazabilidad y evitan imputaciones o eliminaciones de filas sin evidencia suficiente.

En una fase posterior se propone estudiar el mecanismo de ausencia de edad, comparar estrategias de imputación y realizar análisis de sensibilidad respecto de filas idénticas y valores extremos. También conviene evaluar asociaciones ajustadas por sexo, clase, edad y tamaño familiar, y controlar redundancias o fuga de información antes de cualquier modelamiento. Estas propuestas no constituyen resultados de esta fase.

## 15. Reproducibilidad y referencias
Ejecutar desde la raíz o notebooks/ con las dependencias de requirements.txt y el archivo versionado datos/titanic.csv. Reiniciar el kernel y ejecutar todas las celdas. Las nueve figuras se guardan en figuras/ y la copia analítica en datos/titanic_eda_f1.csv. Se registra la huella SHA-256 del CSV original y se verifica que el DataFrame original no se modificó. Los notebooks individuales se conservan como antecedentes de los aportes. Las decisiones metodológicas requieren ratificación del equipo.
'''
add(61, 'ruta_salida = raiz_proyecto / "datos" / "titanic_eda_f1.csv"\ntitanic_eda.to_csv(ruta_salida, index=False)\nassert pd.read_csv(ruta_salida).shape == titanic_eda.shape\nprint("CSV analítico:", ruta_salida.relative_to(raiz_proyecto))')
for c in nb.cells:
    if c.cell_type == 'code':
        compile(c.source, '<celda>', 'exec')
        c.outputs = []
        c.execution_count = None
nbformat.validate(nb)
nbformat.write(nb, dst)
print(f'Generado: {dst} ({len(nb.cells)} celdas). Ejecutar desde cero.')
