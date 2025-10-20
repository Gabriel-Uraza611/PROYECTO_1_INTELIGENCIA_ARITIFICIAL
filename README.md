# PROYECTO_1_INTELIGENCIA_ARITIFICIAL
### Profesor: Joshua Triana Madrid

---
## Desarrolladores

<p align="center">
  <a href="https://github.com/Gabriel-Uraza611" target="_blank">
    <img src="https://github.com/Gabriel-Uraza611.png?size=100" alt="Foto de Perfil de Gabriel-Uraza611" width="100" height="100" style="border-radius: 50%;">
  </a>
  <br>
  <b>Gabriel Uraza 2359594</b>
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
  <b>Juan Bolaños 2380616</b>
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
  <b>Juan José Millan 2266393</b>
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
  <b>Alejandro Luna</b>
  <br>
  <a href="https://github.com/ALEJANDRO807" target="_blank">
    @ALEJANDRO807
  </a>
</p>

### Descripción: 
Vamos a resolver un problema clásico, donde la hormiga debe encontrar el hongo mágico, y
puede pasar por venenos.
El agente va a aplicar estas dos variaciones de los algoritmos que vimos en clase:
  1. Beam Search: Es una versión de la búsqueda informada que limita la cantidad de nodos
  que se mantienen en cada nivel (la "amplitud de la viga" o β). En cada nivel del árbol,
  solo se expanden los β nodos más prometedores (según h(n) o f(n)), y el resto se
  descartan permanentemente.
  2. Dynamic Weighting: En lugar de un peso fijo ε como en Weighted A*, esta técnica ajusta
  el peso de la heurística dinámicamente. Por ejemplo, f(n) = g(n) + h(n) + ε * (1 - (d(n)/N))
  * h(n), donde d(n) es la profundidad. Da más peso a h(n) al principio de la búsqueda
  (para alejarse rápido de la raíz) y menos peso cerca de la meta (para refinar la
  búsqueda y garantizar optimalidad)


