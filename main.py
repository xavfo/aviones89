import tkinter as tk
import random
import math

class RadarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Radar de Caza de Aviones")

        self.width, self.height = 800, 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.center_x, self.center_y = self.width // 2, self.height // 2
        
        self.kills = 0
        self.kills_text = self.canvas.create_text(
            self.width - 100, 30, text="KILLS: 0", 
            fill="#00ff00", font=("Courier", 18, "bold")
        )

        self.focus_angle = 0
        self.focus_distance = 60

        self.trail_items = []
        self.reticle_lines = []
        self.draw_reticle()

        self.enemies = []

        self.shoot_button = tk.Button(root, text="DISPARAR", command=self.shoot, bg="#220000", fg="#00ff00", font=("Courier", 12, "bold"))
        self.shoot_button.pack(side=tk.BOTTOM, pady=10)

        for _ in range(5):
            self.create_enemy()

        self.root.bind("<Left>", lambda e: self.move_focus(-15))
        self.root.bind("<Right>", lambda e: self.move_focus(15))
        self.root.bind("<Up>", lambda e: self.change_distance(-20))
        self.root.bind("<Down>", lambda e: self.change_distance(20))
        self.root.bind("<space>", lambda e: self.shoot())
        self.root.focus_set()

        self.animate()

    def move_focus(self, delta):
        self.focus_angle = (self.focus_angle + delta) % 360
        self.add_trail()
        self.draw_reticle()

    def change_distance(self, delta):
        self.focus_distance = max(40, min(200, self.focus_distance + delta))
        self.add_trail()
        self.draw_reticle()

    def add_trail(self):
        fx = self.center_x + self.focus_distance * math.cos(math.radians(self.focus_angle - 90))
        fy = self.center_y + self.focus_distance * math.sin(math.radians(self.focus_angle - 90))
        
        item = self.canvas.create_text(
            fx, fy, text="+", fill="#ffff00", font=("Courier", 10)
        )
        self.trail_items.append(item)

    def draw_reticle(self):
        for item in self.reticle_lines:
            self.canvas.delete(item)
        self.reticle_lines = []

        r = 30
        self.reticle_lines.append(self.canvas.create_oval(
            self.center_x - r, self.center_y - r,
            self.center_x + r, self.center_y + r,
            outline="#00ff00", dash=(4, 4)
        ))

        self.reticle_lines.append(self.canvas.create_text(
            self.center_x, self.center_y, text="o", fill="#00ff00", font=("Courier", 14)
        ))

        for dist in [60, 100, 140]:
            self.reticle_lines.append(self.canvas.create_oval(
                self.center_x - dist, self.center_y - dist,
                self.center_x + dist, self.center_y + dist,
                outline="#00ff00", dash=(2, 4)
            ))

        for dist in [60, 100, 140]:
            self.reticle_lines.append(self.canvas.create_line(
                self.center_x, self.center_y - dist,
                self.center_x, self.center_y + dist,
                fill="#00ff00", dash=(1, 4)
            ))
            self.reticle_lines.append(self.canvas.create_line(
                self.center_x - dist, self.center_y,
                self.center_x + dist, self.center_y,
                fill="#00ff00", dash=(1, 4)
            ))

        self.reticle_lines.append(self.canvas.create_line(
            self.center_x - r - 10, self.center_y,
            self.center_x - r - 30, self.center_y,
            fill="#00ff00"
        ))
        self.reticle_lines.append(self.canvas.create_line(
            self.center_x + r + 10, self.center_y,
            self.center_x + r + 30, self.center_y,
            fill="#00ff00"
        ))
        self.reticle_lines.append(self.canvas.create_line(
            self.center_x, self.center_y - r - 10,
            self.center_x, self.center_y - r - 30,
            fill="#00ff00"
        ))
        self.reticle_lines.append(self.canvas.create_line(
            self.center_x, self.center_y + r + 10,
            self.center_x, self.center_y + r + 30,
            fill="#00ff00"
        ))

        fx = self.center_x + self.focus_distance * math.cos(math.radians(self.focus_angle - 90))
        fy = self.center_y + self.focus_distance * math.sin(math.radians(self.focus_angle - 90))
        self.focus_crosshair = self.canvas.create_line(fx - 10, fy, fx + 10, fy, fill="#ffff00", width=2)
        self.focus_crosshair_v = self.canvas.create_line(fx, fy - 10, fx, fy + 10, fill="#ffff00", width=2)

    def create_enemy(self):
        angle = random.randint(0, 359)
        dist = random.randint(80, 300)
        
        enemy = {
            'hits': 0,
            'angle': angle,
            'distance': dist,
            'text_items': []
        }
        self.enemies.append(enemy)
        self.update_enemy_draw(enemy)

    def update_enemy_draw(self, enemy):
        for item in enemy['text_items']:
            self.canvas.delete(item)
        enemy['text_items'] = []

        if enemy['hits'] >= 2:
            explosion = [
                " *** ",
                "*+*",
                " *** "
            ]
            color = "#ffff00"
        else:
            explosion = [
                "  /| ",
                "-(*)-",
                "  |/ "
            ]
            color = "#ff4400"

        x = self.center_x + enemy['distance'] * math.cos(math.radians(enemy['angle'] - 90))
        y = self.center_y + enemy['distance'] * math.sin(math.radians(enemy['angle'] - 90))
        
        size = 15
        for i, line in enumerate(explosion):
            enemy['text_items'].append(self.canvas.create_text(
                x, y - size + i * size, 
                text=line, fill=color, font=("Courier", 12)
            ))

    def move_enemies(self):
        pass

    def remove_enemy(self, enemy):
        for item in enemy['text_items']:
            self.canvas.delete(item)
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def shoot(self):
        target = self.find_target()
        
        if target:
            target['hits'] += 1
            self.update_enemy_draw(target)
            
            if target['hits'] >= 3:
                self.kills += 1
                self.canvas.itemconfigure(self.kills_text, text=f"KILLS: {self.kills}")
                self.remove_enemy(target)

    def find_target(self):
        closest = None
        min_diff = float('inf')
        
        for enemy in self.enemies:
            angle_diff = abs(enemy['angle'] - self.focus_angle)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            
            dist_diff = abs(enemy['distance'] - self.focus_distance)
            
            if dist_diff < 30 and angle_diff < 20:
                total_diff = dist_diff + angle_diff * 2
                if total_diff < min_diff:
                    min_diff = total_diff
                    closest = enemy
        
        return closest

    def animate(self):
        self.draw_reticle()
        
        while len(self.enemies) < 5:
            self.create_enemy()
        
        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = RadarApp(root)
    root.mainloop()