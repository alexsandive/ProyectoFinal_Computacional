#!/usr/bin/env python
"""
Dinámica Molecular

Implementa un sistema conformado por una caja de lado L y N discos de radio r. Estos parten con una velocidad y posición aleatorios. Los discos pueden chocar de forma elástica con las paredes, y entre ellos también. Los discos no poseen rotación.
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import random

class Disco:
    """
    Clase utilizada para representar un disco.

    Guarda la información propia del disco (posición, velocidad, radio y color).
    Determina el movimiento de cada disco; actualiza su posición, comprueba y maneja las colisiones con paredes y con otros discos.
    """

    def __init__(self, x_pos, y_pos, radio, color, x_vel, y_vel):
        """
        Inicia cada instancia de los discos. Crea además un historial de las posiciones tomadas por cada disco.

        Args:
            x_pos (float): Posición en x del disco
            y_pos (float): Posición en y del disco
            radio (float): Radio del disco
            color (string): Color del disco
            x_vel (float): Velocidad en x del disco
            y_vel (float): Velocidad en y del disco
            
        Example:
            >>> Disco(0, 0, 1, "red", 1, 2)
            >>> Produce una instancia de un disco rojo de radio 1, ubicado en el centro del cuadro, con velocidad (1, 2)
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radio = radio
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_poss = [x_pos]
        self.y_poss = [y_pos]

    def move(self, dt):
        """
        Actualiza la posición del disco

        Args:
            dt (float): Paso del tiempo

        Example:
            >>> self.x_pos = 1.0
            >>> self.y_pos = 0.0
            >>> self.x_vel = 3.0
            >>> self.y_vel = -1.0
            >>> dt = 0.01
            >>> self.move(0.01)
            >>> Nuevas posiciones: self.x_pos = 1.03, self.y_pos = -0.01
        """
        self.x_pos += self.x_vel * dt
        self.y_pos += self.y_vel * dt
        self.x_poss.append(self.x_pos)
        self.y_poss.append(self.y_pos)

    def check_colisionPared(self, ancho, altura):
        """
        Comprueba colisiones con las paredes. En caso de chocar con una pared, invierte la velocidad perpendicular a la pared. Además, recoloca el disco fuera de la pared

        Args:
            ancho (float): Ancho de la caja
            altura (float): Alto de la caja

        Example:
            >>> ancho = 10
            >>> largo = 10
            >>> self.r = 1
            >>> self.x_pos = 4.01
            >>> self.y_pos = 0
            >>> Nueva velocidad: self.x_vel = -self.x_vel
            >>> Nueva posición: self.x_pos = 3.99
        """
        if self.x_pos - self.radio <= -ancho / 2:
            self.x_vel = abs(self.x_vel)  # Rebote positivo
            self.x_pos = -ancho / 2 + self.radio + ancho/1000
            self.x_poss[-1] = self.x_pos
        elif self.x_pos + self.radio >= ancho / 2:
            self.x_vel = -abs(self.x_vel)  # Rebote negativo
            self.x_pos = ancho / 2 - self.radio - ancho/1000
            self.x_poss[-1] = self.x_pos
            
        if self.y_pos - self.radio <= -altura / 2:
            self.y_vel = abs(self.y_vel)
            self.y_pos = -altura / 2 + self.radio + altura/1000
            self.y_poss[-1] = self.y_pos
        elif self.y_pos + self.radio >= altura / 2:
            self.y_vel = -abs(self.y_vel)
            self.y_pos = altura / 2 - self.radio - altura/1000
            self.y_poss[-1] = self.y_pos


    def check_colisionDisco(self, otro_disco):
        """
        Comprueba la colisión con otros discos. Cuando choca, intercambia las velocidades radiales de los discos, y mantiene la velocidad tangencial constante. Separa ligeramente ambos discos, para evitar errores.

        Args:
            otro_disco (instance): El disco con el que se colisiona

        Example:
            >>> self.r = 1.0
            >>> self.x_pos = 0.0
            >>> self.y_pos = 0.0
            >>> self.x_vel = 2.0
            >>> self.y_vel = 0.0
            >>> otro_disco.x
            >>> otro_disco.x_pos = 0.95
            >>> otro_disco.y_pos = 0.0
            >>> otro_disco.x_vel = -5.0
            >>> otro_disco.y_vel = 0.0
            >>> Nuevas velocidades: self.x_vel = -5.0, otro_disco.x_vel = 2.0
            >>> Nuevas posiciones: self.x_pos = -0.025, otro_disco.x_pos = 0.975
        """
        dx = otro_disco.x_pos - self.x_pos
        dy = otro_disco.y_pos - self.y_pos
        distancia = np.sqrt(dx**2 + dy**2)

        if distancia <= (self.radio + otro_disco.radio) and distancia > 0:
            # Convirtiendo la velocidad a coordenadas polares
            # Vector radial unitario
            rx = dx / distancia # cos(θ)
            ry = dy / distancia # sen(θ) 
            # Vector angular (theta) unitario
            tx = -ry # -sen(θ)
            ty = rx # cos(θ)

            # Cambio para el disco 1
            v1r = self.x_vel * rx + self.y_vel * ry
            v1t = self.x_vel * tx + self.y_vel * ty
            # Cambio para el disco 2
            v2r = otro_disco.x_vel * rx + otro_disco.y_vel * ry
            v2t = otro_disco.x_vel * tx + otro_disco.y_vel * ty
            
            # En colisión elástica de masas iguales, las velocidades radiales se intercambian
            v1r_new = v2r
            v2r_new = v1r
            # Las velocidades angulares se mantienen
            v1t_new = v1t
            v2t_new = v2t
            
            # Convertir de nuevo a coordenadas cartesianas
            self.x_vel = v1r_new * rx + v1t_new * tx
            self.y_vel = v1r_new * ry + v1t_new * ty
            otro_disco.x_vel = v2r_new * rx + v2t_new * tx
            otro_disco.y_vel = v2r_new * ry + v2t_new * ty
            
            # Separar discos para evitar superposición
            overlap = (self.radio + otro_disco.radio - distancia) / 2.0
            self.x_pos -= overlap * rx
            self.y_pos -= overlap * ry
            otro_disco.x_pos += overlap * rx
            otro_disco.y_pos += overlap * ry
            
            #Actualizar historial de posiciones
            self.x_poss[-1] = self.x_pos
            self.y_poss[-1] = self.y_pos
            otro_disco.x_poss[-1] = otro_disco.x_pos
            otro_disco.y_poss[-1] = otro_disco.y_pos
            
            return True
        return False

class DiscoSimulation:
    """
    Inicia y genera la simulación.
    """
    def __init__(self, N, height, width, radio, dt):
        """
        Inicia los parámetros que se mantienen constantes en la simulación.

        Args:
            N (int): Número de discos
            height (float): Altura de la caja.
            width (float): Ancho de la caja.
            radio (float): Radio de los discos.
            dt (float): Paso del tiempo.

        Example:
            >>> DiscoSimulation(500, 10, 10, 0.01, 0.5)
            >>> Crea una simulación con 500 discos de radio 0.01, ubicados dentro de una caja de tamaño 10x10. El paso del tiempo es de 0.5.
        """
        self.N = N
        self.altura = height
        self.ancho = width
        self.radio = radio
        self.pasoTemp = dt
        self.discos = []

    def creacionDiscos(self):
        """
        Intenta crear cada uno de los discos solicitados. Siempre procura que los discos no inicien superpuestos. Si no lo logra crear, lo anuncia con un mensaje.
        """
        Max = 1000
        for i in range(self.N):
            for intento in range(Max):
                    x_pos = random.uniform(-self.ancho / 2 + self.radio, self.ancho / 2 - self.radio)
                    y_pos = random.uniform(-self.altura / 2 + self.radio, self.altura / 2 - self.radio)
                    color = random.choice(['red', 'blue', 'green', 'pink', 'purple', 'orange'])
                    x_vel = random.uniform(-3, 3)
                    y_vel = random.uniform(-3, 3)
                    
                    # Asegurar velocidad mínima
                    while abs(x_vel) < 0.5 and abs(y_vel) < 0.5:
                        x_vel = random.uniform(-3, 3)
                        y_vel = random.uniform(-3, 3)

                    disco = Disco(x_pos, y_pos, self.radio, color, x_vel, y_vel)
                    
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


    def animarMovimiento(self):
        """
        Anima la simulación. Calcula las posiciones de los discos. Maneja las colisiones.
        """
        fig, ax = plt.subplots()
        ax.set_xlim(-self.ancho / 2, self.ancho / 2)
        ax.set_ylim(-self.altura / 2, self.altura / 2)
        ax.set_aspect('equal')
        ax.set_title('Colisión de discos en 2D')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        patches_list = []
        for disco in self.discos:
            circle = patches.Circle((disco.x_pos, disco.y_pos), radius=disco.radio, color=disco.color, alpha=0.7)
            ax.add_patch(circle)
            patches_list.append(circle)

        def init():
            """
            Inicializa la posición inicial de los discos.
            """
            return patches_list
        
        def animar(i):
            """
            Calcula y renderiza cada uno de los frames. Actualiza la posición de los discos, comprueba si existen choques y llama a las funciones pertinentes en cada caso. Finalmente dibuja las posiciones actualizadas de cada disco.
            """
            # Mover todos los discos
            for disco in self.discos:
                disco.move(self.pasoTemp)
                disco.check_colisionPared(self.ancho, self.altura)

            # Verificar colisiones entre discos (optimizado)
            for k in range(len(self.discos)):
                for j in range(k + 1, len(self.discos)):
                    self.discos[k].check_colisionDisco(self.discos[j])

            # Actualizar posiciones visuales
            for idx, disco in enumerate(self.discos):
                patches_list[idx].center = (disco.x_pos, disco.y_pos)

            return patches_list

        ani = animation.FuncAnimation(fig, animar, init_func=init, frames=500, interval=50, blit=True, repeat=True)
        plt.show()


    def histograma(self, bins = 50):
        """
        Dibuja el histograma correspondiente a las posiciones en x de todos los discos.
        """
        posiciones_x = []

        for disco in self.discos:
            posiciones_x.extend(disco.x_poss)

        plt.figure(figsize=(10, 6))
        n, bins, patches = plt.hist(posiciones_x, bins=bins, alpha=0.7, color='red', edgecolor='black')
        
        plt.xlabel('Posición en el eje X')
        plt.ylabel('Frecuencia')
        plt.title(f'Histograma de posiciones de centros de discos (Eje X)\n{self.N} discos')
        plt.grid(True, alpha=0.3)
        
        plt.show() 


sim = DiscoSimulation(10, 10, 10, 0.5, 0.03)
sim.creacionDiscos()
sim.animarMovimiento()
sim.histograma(50)
sim.histograma(500)
