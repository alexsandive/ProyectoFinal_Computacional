# Tutorial

## Uso básico

```python
from Discos import *
# Hacer una simulación de 100 discos en un espacio de 32x32

sim = DiscoSimulation(100, 32, 32, 1, 0.03)
sim.creacionDiscos()
sim.animarMovimiento()
sim.histograma(500)
```
Esto produce una simulación y un histograma

![Vista de la simulación descrita](https://raw.githubusercontent.com/alexsandive/ProyectoFinal_Computacional/main/Evidencias/Simulación100discos.png)
![Histograma producido de la simulación descrita pasados 20 minutos](https://raw.githubusercontent.com/DnSalasAr/ProyectoFinal_Computacional/main/Evidencias/Histograma100discos.png)

