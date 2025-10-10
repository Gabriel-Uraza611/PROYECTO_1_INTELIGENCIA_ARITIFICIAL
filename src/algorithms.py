"""
ALGORITMOS DE BÚSQUEDA - El cerebro del proyecto
Responsabilidades:
- BEAM SEARCH: Encontrar camino limitando nodos por nivel
- DYNAMIC WEIGHTING: Ajustar peso de heurística dinámicamente
- Calcular f(n) = g(n) + h(n) + ε * (1 - (d(n)/N)) * h(n)
- Devolver el camino óptimo para la hormiga
"""