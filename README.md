# PROYECTO_1_INTELIGENCIA_ARITIFICIAL
### Profesor: Joshua Triana Madrid
## Desarrolladores:
> Gabriel Uraza - 2359594-3743
> Juan Bolaños  - 2380616-3743
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


