import tkinter as tk
from tkinter import messagebox
import random

class RadarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Radar de Caza de Aviones")

        # Configuración del tamaño de la ventana
        width, height = 600, 400
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black")
        self.canvas.pack()

        # Lista para almacenar los aviones en el radar
        self.enemies = []

        # Botón para disparar
        self.shoot_button = tk.Button(root, text="Disparar", command=self.shoot)
        self.shoot_button.pack(side=tk.BOTTOM)

        # Crear aviones iniciales
        for _ in range(5):
            self.create_enemy()

        # Iniciar la animación
        self.animate()

    def create_enemy(self):
        x, y = random.randint(0, 600), random.randint(0, 400)
        size = random.randint(10, 20)
        enemy_id = self.canvas.create_oval(x - size, y - size, x + size, y + size, fill="red")
        self.enemies.append((enemy_id, x, y))

    def move_enemies(self):
        for i, (enemy_id, x, y) in enumerate(self.enemies):
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            new_x, new_y = x + dx, y + dy
            self.canvas.move(enemy_id, dx, dy)
            if not (0 <= new_x < 600 and 0 <= new_y < 400):
                self.canvas.delete(enemy_id)
                del self.enemies[i]

    def animate(self):
        self.move_enemies()
        self.root.after(50, self.animate)

    def shoot(self):
        x, y = self.canvas.winfo_pointerxy()
        for i, (enemy_id, enemy_x, enemy_y) in enumerate(self.enemies):
            if abs(enemy_x - x) < 20 and abs(enemy_y - y) < 20:
                self.canvas.delete(enemy_id)
                del self.enemies[i]
                messagebox.showinfo("Disparo", "¡Impacto! Avión eliminado.")
                return
        messagebox.showwarning("Disparo", "No hay aviones cerca para disparar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RadarApp(root)
    root.mainloop()
