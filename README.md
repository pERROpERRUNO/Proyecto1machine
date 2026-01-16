# Demostración de Regresión Lineal y No Lineal con Manim

Este proyecto consiste en una demostración visual y animada de los conceptos de **regresión lineal** y **regresión no lineal (polinómica)** utilizando la librería **Manim Community** para Python.

El objetivo es mostrar gráficamente cómo los algoritmos de optimización ajustan modelos matemáticos a conjuntos de datos reales y ruidosos.

---

##  Autores – Grupo 6
- Meza León, Ricardo Manuel  
- Ramos Bonilla, Miguel Angel  
- Silva Azañero, Mateo Alejandro  

---

##  Contenido de la Animación

La demostración se divide en tres actos principales:
- Regresión Lineal Optimizada: Visualización de la función $y = wx + b$ ajustándose dinámicamente. Incluye la representación del MSE (Error Cuadrático Medio) mediante cuadrados de colores que cambian según la magnitud del error.
- Regresión No Lineal (Polinomial): Ajuste de una parábola ($y = ax^2 + bx + c$) a datos curvos, mostrando la flexibilidad de los modelos de grado superior.
- Comparativa Final: Una demostración visual de Underfitting (subajuste) vs. un modelo ideal, permitiendo entender por qué la complejidad del modelo debe coincidir con la naturaleza de los datos.

---

##  Requisitos del Sistema
Para ejecutar esta animación, es necesario tener instalados los siguientes componentes en el sistema:

### Dependencias de Software
* **Python 3.9+**: Lenguaje de programación base.
* **MiKTeX / LaTeX**: **Requisito crítico** para la generación de fórmulas matemáticas ($y = wx + b$).

### Librerías de Python
Instala las bibliotecas de cálculo y animación mediante el siguiente comando:

```bash
pip install manim numpy
```
## Como ejecutar la Animación

* Abre una terminal (PowerShell o CMD) en la carpeta donde guardaste el archivo proj.py.
* Ejecuta el siguiente comando:

```bash
python -m manim -pqh proj.py RegressionDemo
```
### Significado de los parámetros:
* -p: Reproduce el video automáticamente al finalizar.
* -qh: Calidad Alta (1080p). Para una renderización rápida de prueba, puedes usar -ql (Calidad Baja).


