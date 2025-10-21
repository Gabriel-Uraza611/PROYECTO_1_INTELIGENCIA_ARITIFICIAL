# PROYECTO_1_INTELIGENCIA_ARITIFICIAL
### Profesor: Joshua Triana Madrid

---
## Desarrolladores

<p align="center">
  <a href="https://github.com/Gabriel-Uraza611" target="_blank">
    <img src="https://github.com/Gabriel-Uraza611.png?size=100" alt="Foto de Perfil de Gabriel-Uraza611" width="100" height="100" style="border-radius: 50%;">
  </a>
  <br>
  <b>Gabriel Uraza - 2359594</b>
  <br>
  <a href="https://github.com/Gabriel-Uraza611" target="_blank">
    @Gabriel-Uraza611
  </a>
</p>

--- <p align="center">
  <a href="https://github.com/juanjo380" target="_blank">
    <img src="https://github.com/juanjo380.png?size=100" alt="Foto de Perfil de juanjo380" width="100" height="100" style="border-radius: 50%;">
  </a>
  <br>
  <b>Juan Bolaños - 2380616</b>
  <br>
  <a href="https://github.com/juanjo380" target="_blank">
    @juanjo380
  </a>
</p>

--- <p align="center">
  <a href="https://github.com/juanjounivalle18" target="_blank">
    <img src="https://github.com/juanjounivalle18.png?size=100" alt="Foto de Perfil de juanjounivalle18" width="100" height="100" style="border-radius: 50%;">
  </a>
  <br>
  <b>Juan José Millan - 2266393</b>
  <br>
  <a href="https://github.com/juanjounivalle18" target="_blank">
    @juanjounivalle18
  </a>
</p>

--- <p align="center">
  <a href="https://github.com/ALEJANDRO807" target="_blank">
    <img src="https://github.com/ALEJANDRO807.png?size=100" alt="Foto de Perfil de ALEJANDRO807" width="100" height="100" style="border-radius: 50%;">
  </a>
  <br>
  <b>Alejandro Luna - 2359418</b>
  <br>
  <a href="https://github.com/ALEJANDRO807" target="_blank">
    @ALEJANDRO807
  </a>
</p>

# Descripción del Problema

Este proyecto aborda un problema clásico de búsqueda en inteligencia artificial, donde **una hormiga debe encontrar el hongo mágico** dentro de un entorno lleno de obstáculos y posibles peligros como **venenos**.

El agente (la hormiga) explora el entorno aplicando **dos algoritmos de búsqueda informada** —variaciones de los estudiados en clase— para hallar la ruta óptima hasta el objetivo.

---

## 🔹 1. Beam Search (Búsqueda en Haz o Viga)

El algoritmo **Beam Search** es una variante **informada y optimizada** de la búsqueda en anchura (*Breadth-First Search*), que **limita el número de nodos explorados por nivel** según un parámetro llamado **amplitud de la viga** o **β (beta)**.

En cada nivel del árbol de búsqueda, solo se conservan los **β nodos más prometedores**, evaluados según una función heurística (por ejemplo, $h(n)$ o $f(n)$).
Los demás nodos se **descartan permanentemente**, lo que reduce el uso de memoria y acelera la búsqueda, a costa de sacrificar la garantía de optimalidad.

###  Fórmula general

$$
f(n) = g(n) + h(n)
$$

Donde:
- $g(n)$: costo acumulado desde el estado inicial hasta el nodo $n$,
- $h(n)$: estimación heurística del costo restante hasta el objetivo,
- Solo se expanden los $\beta$ nodos con los valores más bajos de $f(n)$.

---

## 🔹 2. Dynamic Weighting (Ponderación Dinámica)

**Dynamic Weighting** es una extensión del algoritmo **Weighted A\***, en la que el **peso de la heurística varía dinámicamente** según la profundidad del nodo dentro del árbol de búsqueda.

En lugar de usar un peso fijo $\varepsilon$ para controlar la influencia de la heurística, se introduce un **factor adaptativo** que **reduce el peso de $h(n)$** a medida que el agente se acerca al objetivo.

Esto permite al agente **explorar con mayor libertad al inicio** (priorizando la heurística) y **refinar el camino cerca del objetivo** (priorizando el costo real acumulado), equilibrando **eficiencia y optimalidad**.

### Fórmula de evaluación

$$
f(n) = g(n) + h(n) + \varepsilon \left(1 - \frac{d(n)}{N}\right) h(n)
$$

Donde:
- $g(n)$: costo acumulado desde el inicio hasta $n$,
- $h(n)$: valor heurístico estimado hasta la meta,
- $\varepsilon$: peso máximo inicial de la heurística,
- $d(n)$: profundidad actual del nodo $n$,
- $N$: profundidad máxima esperada o límite de búsqueda.

---

## Comparación conceptual

| Característica | Beam Search | Dynamic Weighting |
|----------------|-------------|-------------------|
| **Tipo de búsqueda** | Heurística limitada | Heurística adaptativa |
| **Parámetro clave** | Amplitud de viga $\beta$ | Peso dinámico $\varepsilon\,(1 - d(n)/N)$ |
| **Ventaja** | Ahorra memoria y tiempo | Balancea velocidad y precisión |
| **Desventaja** | Puede descartar el camino óptimo | Requiere cálculo de profundidad |
| **Optimalidad** | No garantizada | Potencialmente óptima (si se ajusta bien $\varepsilon$) |

---

*Ambos métodos representan enfoques heurísticos que equilibran entre la eficiencia de búsqueda y la calidad de la solución, ofreciendo diferentes estrategias para la toma de decisiones del agente en entornos complejos.*

