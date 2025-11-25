#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import random

class Disco:
    """
    Clase utilizada para representar un disco.

    """

    def __init__(self, x_pos, y_pos, radio, color, x_vel, y_vel):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radio = radio
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_poss = [x_pos]  
        self.y_poss = [y_pos]  

    def move(self, dt):
        
        self.x_pos += self.x_vel * dt 
        self.y_pos += self.y_vel * dt
        self.x_poss.append(self.x_pos)  
        self.y_poss.append(self.y_pos)  

    def check_colisionPared(self, ancho, altura):
        
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
    
    def __init__(self, N, height, width, radio, dt):
        self.N = N  
        self.altura = height
        self.ancho = width
        self.radio = radio
        self.pasoTemp = dt
        self.discos = []

    def creacionDiscos(self):
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
            return patches_list
        
        def animar(i):
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


sim = DiscoSimulation(100, 50, 50, 1, 0.03)
sim.creacionDiscos()
sim.animarMovimiento()
sim.histograma(50)
sim.histograma(500)
