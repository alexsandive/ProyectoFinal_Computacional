# Tutorial

## Uso básico

Para ejecutar una simualción se deben definir los parametros de la simulación, mediante la creación de un objeto de clase `DiscoSimulation`. Esta clase recibe los parametros en el siguiente orden:
    
1. La **primera entrada** es la **cantidad de discos** que se quieren simular. Esto representa la cantidad de partículas a estudiar.
    
2. La **segunda entrada** es la **altura** del espacio limitante. En la simulación se divide en 2 y los límites van desde el valor dividido entre 2 negativo, hasta el valor dividido entre 2 positivo.
    
3. La **tercera entrada** es el **ancho** del espacio limitante. En la simulación se divide en 2 y los límites van desde el valor dividido entre 2 negativo, hasta el valor dividido entre 2 positivo.
    
4. La **cuarta entrada** representa el **radio** de los discos.
   
5. La **quinta entrada** representa el **salto en el tiempo** (un **dt**). Este salto no puede ser ni muy grande ni muy pequeño, se recomiendan valores entre 0,03 y 0,05.


Una vez declarado el objeto con todos estos valores se invocan los siguientes métodos:
   
1. Primero se llama al método de creación de discos: `<objectname>.creacionDiscos()`.
   
2. Seguidamente se invoca la animación: `<objectname>.animarMovimiento()`.
    
3. Finalmente se llama al método que realiza el histograma, con `n` el número de columnas en el histograma: `<objectname>.histograma(n)`.


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
![Histograma producido de la simulación descrita pasados 20 minutos](https://raw.githubusercontent.com/alexsandive/ProyectoFinal_Computacional/main/Evidencias/Histograma100discos.png)

## Uso especializado

Si se desea **cambiar** aspectos en específico de los discos de la simulación como el **radio** o la **velocidad** se cambian en el método de `creacionDiscos`. Las variables `x_vel` y `y_vel` son las que definen las **velocidades iniciales** de los discos, estas se pueden **ajustar los límites** para que sean mayores a 3. También debajo de donde se definen se declara una cota inferior, esta también se puede ajustar para que sea mayor o menor. Si se desea ajustar para tener **diferentes radios**, se debe **declarar una nueva variable** y que presente los valores deseados. En este ejemplo se usará un radio aleatorio. 

```python
Max = 1000
        for i in range(self.N):
            for intento in range(Max):
                x_pos = random.uniform(-self.ancho / 2 + self.radio, self.ancho / 2 - self.radio)
                y_pos = random.uniform(-self.altura / 2 + self.radio, self.altura / 2 - self.radio)
                color = random.choice(['red', 'blue', 'green', 'pink', 'purple', 'orange'])
                x_vel = random.uniform(-10, 10) # Nuevos valores máximos de la velocidad en x
                y_vel = random.uniform(-10, 10) # Nuevos valores máximos de la velocidad en y
                r_rand = random.uniform(1,3) # Declaración de una variable que tiene valores aleatorios por encima de 0

                # Asegurar velocidad mínima
                while abs(x_vel) < 1 and abs(y_vel) < 1: # Nueva cota inferior
                    x_vel = random.uniform(-10, 10) # Nuevos valores máximos 
                    y_vel = random.uniform(-10, 10) # Nuevos valores máximos

                disco = Disco(x_pos, y_pos, r_rand, color, x_vel, y_vel) # Se usa la nueva variable para los radios de los discos
                    
                # Verificar colisiones con discos existentes
                colision = False
                for other in self.discos:
                    dist = np.sqrt((disco.x_pos - other.x_pos)**2 + (disco.y_pos - other.y_pos)**2)
                    if dist < disco.radio + other.radio:
                        colision = True
                        break
                    
                if not colision:
                    self.discos.append(disco)
                    break
                elif intento == Max - 1:
                    print(f"Advertencia: No se pudo colocar el disco {i+1} después de {Max} intentos")
```
![Vista de la simulación descrita](https://raw.githubusercontent.com/alexsandive/ProyectoFinal_Computacional/main/Evidencias/DiscosdiferenteR.png)
