import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import random, csv

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

    def check_wall_collision(self, width, height):
        
        if self.x_pos - self.radio <= -width / 2:
            self.x_vel = abs(self.x_vel)  # Rebote positivo
            self.x_pos = -width / 2 + self.radio
        elif self.x_pos + self.radio >= width / 2:
            self.x_vel = -abs(self.x_vel)  # Rebote negativo
            self.x_pos = width / 2 - self.radio
            
        if self.y_pos - self.radio <= -height / 2:
            self.y_vel = abs(self.y_vel)
            self.y_pos = -height / 2 + self.radio
        elif self.y_pos + self.radio >= height / 2:
            self.y_vel = -abs(self.y_vel)
            self.y_pos = height / 2 - self.radio

    def check_disk_collision(self, other_disk):
        
        dx = self.x_pos - other_disk.x_pos
        dy = self.y_pos - other_disk.y_pos
        distance = np.sqrt(dx**2 + dy**2)

        if distance < self.radio + other_disk.radio and distance > 0:
            # Vector normal unitario
            nx = dx / distance
            ny = dy / distance
            # Vector tangente unitario
            tx = -ny
            ty = nx
            # Proyectar velocidades en normal y tangente para disco 1
            v1n = self.x_vel * nx + self.y_vel * ny
            v1t = self.x_vel * tx + self.y_vel * ty
            # Proyectar velocidades en normal y tangente para disco 2
            v2n = other_disk.x_vel * nx + other_disk.y_vel * ny
            v2t = other_disk.x_vel * tx + other_disk.y_vel * ty
            
            # En colisión elástica de masas iguales, las velocidades normales se intercambian
            v1n_new = v2n
            v2n_new = v1n
            # Las velocidades tangenciales se mantienen
            v1t_new = v1t
            v2t_new = v2t
            
            # Convertir de nuevo a coordenadas cartesianas
            self.x_vel = v1n_new * nx + v1t_new * tx
            self.y_vel = v1n_new * ny + v1t_new * ty
            other_disk.x_vel = v2n_new * nx + v2t_new * tx
            other_disk.y_vel = v2n_new * ny + v2t_new * ty
            
            overlap = (self.radio + other_disk.radio - distance) / 2.0
            self.x_pos -= overlap * nx
            self.y_pos -= overlap * ny
            other_disk.x_pos += overlap * nx
            other_disk.y_pos += overlap * ny
            
            
            self.x_poss[-1] = self.x_pos
            self.y_poss[-1] = self.y_pos
            other_disk.x_poss[-1] = other_disk.x_pos
            other_disk.y_poss[-1] = other_disk.y_pos
            
            return True
        return False




class DiscoSimulation:
    
    def __init__(self, N, height, width, radio):
        self.N = N  
        self.altura = height
        self.ancho = width
        self.radio = radio
        self.discos = []

    def disk_creation(self):
        max_attempts = 1000
        for _ in range(self.N):
            for attempt in range(max_attempts):
                    x_pos = random.uniform(-self.ancho/2 + self.radio, self.ancho/2 - self.radio)
                    y_pos = random.uniform(-self.altura/2 + self.radio, self.altura/2 - self.radio)
                    color = random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange'])
                    x_vel = random.uniform(-3, 3)
                    y_vel = random.uniform(-3, 3)
                    
                    # Asegurar velocidad mínima
                    while abs(x_vel) < 0.5 and abs(y_vel) < 0.5:
                        x_vel = random.uniform(-3, 3)
                        y_vel = random.uniform(-3, 3)

                    disco = Disco(x_pos, y_pos, self.radio, color, x_vel, y_vel)
                    
                    # Verificar colisiones con discos existentes
                    collision = False
                    for other in self.discos:
                        dist = np.sqrt((disco.x_pos - other.x_pos)**2 + (disco.y_pos - other.y_pos)**2)
                        if dist < disco.radio + other.radio:
                            collision = True
                            break
                    
                    if not collision:
                        self.discos.append(disco)
                        break
                    elif attempt == max_attempts - 1:
                        print(f"Advertencia: No se pudo colocar el disco {_+1} después de {max_attempts} intentos")
                        
            return self.discos

    def animate_movement(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-self.ancho/2, self.ancho/2)
        ax.set_ylim(-self.altura/2, self.altura/2)
        ax.set_aspect('equal')
        ax.set_title('Dinámica Molecular - Discos en 2D')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        patches_list = []
        for disco in self.discos:
            circle = patches.Circle((disco.x_pos, disco.y_pos), radius=disco.radio, 
                                  color=disco.color, alpha=0.7)
            ax.add_patch(circle)
            patches_list.append(circle)

        def init():
            return patches_list

        def animate(i):
            dt = 0.05
            # Mover todos los discos
            for disco in self.discos:
                disco.move(dt)
                disco.check_wall_collision(self.ancho, self.altura)

            # Verificar colisiones entre discos (optimizado)
            for i in range(len(self.discos)):
                for j in range(i + 1, len(self.discos)):
                    self.discos[i].check_disk_collision(self.discos[j])

            # Actualizar posiciones visuales
            for idx, disco in enumerate(self.discos):
                patches_list[idx].center = (disco.x_pos, disco.y_pos)

            return patches_list

        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=500, interval=50, blit=True, repeat=True)
        plt.show()
        return ani


    def get_positions(self):
        positions = []
        for disco in self.discos:
            positions.append((disco.x_poss, disco.y_poss))

        return positions
    def calculate_energy(self):
        energy = 0.0
        for disco in self.discos:
            energy += 0.5 * (disco.x_vel**2 + disco.y_vel**2)  # masa = 1
        return energy

def time_to_wall_collision(disk, width, height):
    tx_min = float('inf')
    ty_min = float('inf')
    if disk.x_vel > 0:
        tx_min = (width / 2 - disk.radio - disk.x_pos) / disk.x_vel
    elif disk.x_vel < 0:
        tx_min = (-width / 2 + disk.radio - disk.x_pos) / disk.x_vel
    if disk.y_vel > 0:
        ty_min = (height / 2 - disk.radio - disk.y_pos) / disk.y_vel
    elif disk.y_vel < 0:
        ty_min = (-height / 2 + disk.radio - disk.y_pos) / disk.y_vel

    return min(tx_min, ty_min)

def time_to_disk_collision(disk1, disk2):
    R_rel = np.array([disk1.x_pos - disk2.x_pos, disk1.y_pos - disk2.y_pos])
    V_rel = np.array([disk1.x_vel - disk2.x_vel, disk1.y_vel - disk2.y_vel])
    R_rel_dot_V_rel = np.dot(R_rel, V_rel)
    V_rel_square = np.dot(V_rel, V_rel)
    R_rel_square = np.dot(R_rel, R_rel)
    sum_radius = disk1.radio + disk2.radio
    if V_rel_square == 0:
        return float('inf')
    a = V_rel_square
    b = 2 * R_rel_dot_V_rel
    c = R_rel_square - sum_radius**2
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return float('inf')
    t1 = (-b - np.sqrt(discriminant)) / (2 * a)
    t2 = (-b + np.sqrt(discriminant)) / (2 * a)
    if t1 > 0 and t2 > 0:
        return min(t1, t2)
    elif t1 > 0:
        return t1
    elif t2 > 0:
        return t2
    else:
        return float('inf')

def determine_collision_event(disks, width, height):
    min_time = float('inf')
    event_type = None
    disk_indices = (None, None)

    for i, disk1 in enumerate(disks):
        t_wall_collision = time_to_wall_collision(disk1, width, height)
        if t_wall_collision < min_time:
            min_time = t_wall_collision
            event_type = 'wall_collision'
            disk_indices = (i, None)

        for j in range(i + 1, len(disks)):
            disk2 = disks[j]
            t_disk_collision = time_to_disk_collision(disk1, disk2)
            if t_disk_collision < min_time:
                min_time = t_disk_collision
                event_type = 'disk_collision'
                disk_indices = (i, j)

    return event_type, disk_indices, min_time



def save_data(array, file_csv):
    with open(file_csv, mode='w', newline='') as file_csv:

        writer_csv = csv.writer(file_csv)

        for row in array:

            writer_csv.writerow(row)

def run_and_save_data(N, M, file_csv):
    
    Radius = np.sqrt(4/N)*0.5

    sim = DiscoSimulation(N, 5, 5, Radius)

    disks = sim.disk_creation()

    sim.animate_movement()

    while True:

        print("Transcurrieron " + str(len(disks[0].x_poss)) + " instantes de tiempo")

        if len(disks[0].x_poss) > M:

            positions = [[sim.get_positions()[j][0][i] for i in range(M)] for j in range(N)]

            if __name__ == "__main__":

                save_data(positions, file_csv)

                print("Lista de tamaño " + str(len(positions)) + " x " + str(len(positions[0])) + f" guardada en {file_csv}.")
        break



run_and_save_data(25, 6000, "data25.csv")


def Histogram(N, divisions, file_csv):
    
    all_positions_str = []

    with open(file_csv, 'r') as file_csv:

        lector_csv = csv.reader(file_csv)

        for row in lector_csv:

            all_positions_str.extend(row)

    all_positions = [float(i) for i in all_positions_str]

    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    weights = np.ones_like(all_positions) / len(all_positions)

    plt.hist(all_positions, bins=divisions, weights=weights)

    plt.gca().set(title=f'Histograma de probabilidad para {N} discos', ylabel='Probabilidad')

    plt.xlim(-2.5, 2.5)

    plt.xlabel("Posición x")

    plt.show()

Histogram(25, 100, "data25.csv")                                           
