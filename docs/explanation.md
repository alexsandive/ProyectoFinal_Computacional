# Dinámica Molecular

El código implementa un sistema conformado por un espacio rectangular con anchura y altura definibles, y una cantidad de discos a elección con cierto radio propuesto. Estos parten con una velocidad y posición aleatorios. Los discos chocan de forma elástica con las paredes, y entre ellos también. Los discos no poseen rotación. No se consideran fuerzas de fricción ni de otro tipo.

---

## Método `move`: dinámica del movimiento

El método `move` actualiza la posición del disco según su velocidad:

$$
x(t+\Delta t) = x(t) + v_x \;\Delta t
$$

$$
y(t+\Delta t) = y(t) + v_y \;\Delta t
$$

No se aplica fuerza, de modo que la velocidad permanece constante mientras no haya colisiones. Podemos notar que es una aplicación directa de las fórmulas de movimiento rectilíneo uniforme para la posición final de una patícula movimento. El movimiento de cada partícula se modelo a partir de la cinemática del movimiento uniforme. El cálculo a nivel computacional se conoce como *método de Euler explícito*, válido cuando:

* Las partículas se mueven en trayectorias rectas entre colisiones.
* Las escalas de tiempo son pequeñas para evitar errores numéricos grandes.



## Método `checkColisionPared`: choque con paredes

Cuando un disco llega a una pared, parte de su posición probablemnete se encuentre fuera del dominio. El modelo usa **colisiones perfectamente elásticas** con las paredes para calcular el ángulo y la velocidad después de la colsiión. Teóricamente se considera que una partícula que rebota o colisiona con una superficie uniforme simplemente se refleja, entonces se optó por reflejar la velocidad de la partícula en el eje correspondiente, de esta manera el ángulo de entrada es igual al ángulo de salida.

### Condiciones de choque

Para una pared vertical:

$$
x \le r \quad\text{o}\quad x \ge L - r
$$

Para una pared horizontal:

$$
y \le r \quad\text{o}\quad y \ge H - r
$$

### Efecto de la colisión

La componente perpendicular se invierte:

$$
v_x \rightarrow -v_x \quad\text{(pared vertical)}
$$

$$
v_y \rightarrow -v_y \quad\text{(pared horizontal)}
$$

Esto implementa el principio de conservación de energía cinética en una colisión elástica, donde solo cambia la dirección de la velocidad. Es por eso que, si todos los discos tienen el mismo tamaño y las paredes son rígidas, la energía total del sistema permanece constante.


## Método `colisionDiscos`: colisiones elásticas entre dos discos

Se detecta la colisión comparando la distancia entre centros:

$$
\text{colisiona si: } \quad d = \| \vec r_2 - \vec r_1 \| \le r_1 + r_2
$$

### Descomposición de velocidades

En una colisión elástica entre partículas de igual masa:

1. Se define un vector normal:

$$
\hat n = \dfrac{\vec r_2 - \vec r_1}{d}
$$

2. Se proyectan las velocidades sobre:
    - la dirección normal $\hat n$,
    - la dirección tangencial $\hat t$.

3. En la colisión:
    - **las componentes tangenciales permanecen iguales**,  
    - **las normales se intercambian**.

La manera más sencilla de hacer estos cálculos es pasar a coordenadas polares y luego volver a cartesianas.
Este resultado proviene de aplicar:

* Conservación del momento lineal,
* Conservación de energía cinética,
* Masas iguales.

De esta manera, el intercambio de velocidades permite que el programa colisione discos desde cualquier dirección y sin necesidad de calcular el ángulo después de la colisión. También esto permite no pasar por cálculos más profundo de centro de masa ni de energías de manera explícitya. 


## Animación con `FuncAnimation`

La animación se basa en la función `update(frame)` que:

1. Actualiza posición de cada disco (`move`).
2. Verifica colisiones contra paredes.
3. Verifica colisiones entre discos.
4. Actualiza las posiciones gráficas en la figura.

`FuncAnimation(fig, update, frames=..., interval=...)` llama a `update` repetidamente y redibuja la escena.

Teóricamente, `FuncAnimation` no entiende "física"; simplemente ejecuta un *loop de renderizado*. Toda la dinámica proviene de los métodos anteriores.


## El histograma y su significado físico

En la simulación, el histograma se genera **a partir de las posiciones del centro de masa de los discos en la coordenada $x$**. A diferencia de un histograma de velocidades, aquí **no se estudia la energía**, sino la **estructura espacial del sistema**. Este histograma toma todos los valores de cada disco, desde que inicia la simulación, hasta un tiempo $t$ donde se acaba la simualción:

$$
x_0,\; x_1,\; x_2,\; \dots,\; x_t
$$

y se distribuyen en un conjunto de columnas que representan un conteo sobre cada punto del eje horizontal.

Esto permite observar:

* Regiones donde se acumulan más discos,
* Regiones donde casi no hay partículas,
* La evolución temporal de la densidad,
* Si la dinámica tiende a una distribución uniforme,
* Si aparecen "racimos" o fluctuaciones locales de densidad.

Los discos tienden a acumularse en los lados, el histograma debería aproximarse a una distribución relativamente plana en el centro. Cualquier desviación persistente puede indicar:
* Errores numéricos,
* Inestabilidades,
* Efectos de borde,
* Fluctuaciones estadísticas.

Este histograma tiene como objetivo estudiar el comportamiento de las partículas en un entorno descrito como cerrado y con colisiones elásticas. Un ejemplo de esto sería un gas que presente un moviemiento browniano.

---

# Extra: **Spatial Hashing** (optimización añadida)

El *spatial hashing* **no forma parte del código original**, pero se incorpora para hacer eficiente el proceso de detección de colisiones. El chequeo directo de colisiones entre todos los pares de discos tiene complejidad:

$$
O(N^2)
$$

pues debemos comparar cada disco con todos los demás. Este método termina siendo ineficiente a grandes escalas, produciendo una simulación más lenta y poco útil.


## Idea del método

El espacio se divide en una cuadrícula de celdas. Cada disco se inserta en una celda basada en sus coordenadas:

$$
\text{celda}(x,y)=\left(\left\lfloor\frac{x}{s}\right\rfloor,\left\lfloor\frac{y}{s}\right\rfloor\right)
$$

donde $s$ es el tamaño de la celda (normalmente, algo mayor que el diámetro del disco). Para encontrar posibles colisiones de un disco basta con **examinar su celda** y las celdas vecinas, que si acomoda en cuadrado, como una matriz, se volverían **8 celdas vecinas**. Esto reduce el número de comparaciones drásticamente.


## ¿Por qué se llama "hashing"?

Porque la celda `(i, j)` se almacena en un diccionario / hashmap como clave:

`hash[(i, j)] = [lista de discos en esa celda]`


Esto permite acceso O(1) esperado.

*Spatial hashing* no cambia la física.  
Solo optimiza el número de colisiones que deben evaluarse.  
Es uno de los métodos estándar en simulaciones físicas para videojuegos y animación.

### Referencias
- Halliday, D., Resnick, R., & Krane, K. (2005). *Física* (5.ª ed.). Wiley.
- Mirtich, B. (1997). Efficient algorithms for two-phase collision detection. Practical motion planning in robotics: current approaches and future directions, 203-223.
- Teschner, M., Heidelberger, B., Müller, M., Pomerantes, D., & Gross, M. H. (2003). Optimized spatial hashing for collision detection of deformable objects. In Vmv (Vol. 3, pp. 47-54).