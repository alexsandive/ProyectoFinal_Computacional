# Dinámica Molecular

El código implementa un sistema conformado por un espacio rectangular con anchura y altura definibles, y una cantidad de discos a elección con cierto radio propuesto. Estos parten con una velocidad y posición aleatorios. Los discos chocan de forma elástica con las paredes, y entre ellos también. Los discos no poseen rotación. No se consideran fuerzas de fricción ni de otro tipo.

# Metodología utilizada en el código

El código implementa una **simulación de colisiones entre discos en dos dimensiones**. Para lograrlo, utiliza una combinación de modelado físico básico, integración temporal, detección de colisiones y animación. La información a continuación se presenta en el orden que se leería el código normalmente (de arriba a abajo).

---

## 1. Representación de cada disco

El código define una clase `Disco` que encapsula toda la información relevante de cada partícula:

- Posición: `x_pos`, `y_pos`
- Velocidad: `x_vel`, `y_vel`
- Radio y color
- Historial de posiciones (`x_poss`) para análisis posterior

Cada instancia de `Disco` puede:

- Moverse en el plano.
- Detectar y ejecutar colisiones con paredes.
- Detectar y ejecutar colisiones con otros discos.

---

## 2. Movimiento de los discos

En cada paso temporal, el método `move()` actualiza la posición del disco mediante integración explícita:

\[
x \leftarrow x + v_x \cdot dt,\qquad y \leftarrow y + v_y ; dt
\]

Este es un método sencillo y directo que permite avanzar la simulación cuadro a cuadro. En cada actualización se almacena la nueva posición en el historial del centro de masa del disco de la posición en x.

---

## 3. Colisiones con las paredes

El método `check_colisionPared()` revisa si el disco viola los límites del contenedor.  
Si lo hace:

- Se invierte la velocidad en el eje correspondiente.
- Se corrige la posición para evitar que el disco quede "incrustado" de la pared.

Esto mantiene a todos los discos confinados dentro del área delimitada.

---

## 4. Colisiones entre discos

El método `colisionDiscos()`:

1. Calcula la distancia entre los dos discos.
2. Comprueba si la distancia es menor o igual a la suma de los radios para determinar la colisión.
3. Se hace un cambio de coordenadas a polares. Esto proyecta las velocidades de ambos discos en:
   - Componente radial, que es línea que conecta los centros
   - Componente tangencial
4. En una colisión elástica de masas iguales:
   - Las componentes radiales de las velocidades se intercambian.
   - Las tangenciales permanecen constantes.
5. Se vuelve a hacer el cambio de las velocidades en coordenadas cartesianas.
6. Se corrigen posiciones para evitar superposición.


---


## 5. Generación de la animación

El método `animarMovimiento()`:

1. Crea una figura de Matplotlib y dibuja un círculo para cada disco.
2. Se define un método `animar()` que en cada frame:
   - Mueve todos los discos.
   - Revisa colisiones con paredes.
   - Verifica colisiones entre discos, en este caso para un disco verifica todos los otros discos existentes.
   - Actualiza la posición gráfica de cada disco.
3. Usa `FuncAnimation` para reproducir la simulación en tiempo real.

---

## 6. Histograma de posiciones

Tras la simulación, el método `histograma()`:

1. Reúne todas las posiciones x almacenadas en `x_poss`.
2. Construye un histograma con Matplotlib.
3. Muestra la distribución espacial recorrida por los discos.

Este análisis permite visualizar qué regiones del contenedor fueron visitadas con mayor frecuencia.

---

## 7. Flujo general de la simulación

1. Se crea la instancia `DiscoSimulation`.
2. Se generan los discos sin superposición inicial (`creacionDiscos()`).
3. Se ejecuta la animación (`animarMovimiento()`).
4. Se analiza la distribución espacial (`histograma()`).


---

## 8. Extra: Optimización mediante "spatial hashing" aplicado en el programa `Discos_optimizado.py`

El método `check_ColisionDisco()` evita revisar colisiones entre todas las parejas posibles de discos.

Para ello:

- Se divide el espacio en una cuadrícula.
- Cada disco se asigna a una celda según su posición.
- Solo se revisan colisiones entre discos que comparten celda o están en celdas vecinas.

Esto reduce enormemente el número de comparaciones necesarias y acelera la simulación.

### Referencias
- Halliday, D., Resnick, R., & Walker, J. (2014). *Fundamentos de Física* (10.ª ed.). Wiley.

