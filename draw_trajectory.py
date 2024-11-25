import tkinter as tk
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Drawing App")
        
        self.canvas = tk.Canvas(root, bg="white", width=400, height=400)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.save)

        self.image = Image.new("RGB", (400, 400), "white")
        self.draw_image = ImageDraw.Draw(self.image)
        self.last_x, self.last_y = None, None
        self.trajectory = []  # 用于保存轨迹

    def draw(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=2)
            self.draw_image.line((self.last_x, self.last_y, x, y), fill="black", width=2)
        
        # 保存轨迹
        self.trajectory.append((x, y))

        self.last_x, self.last_y = x, y

    def save(self, event):
        self.last_x, self.last_y = None, None

        # 保存图像
        self.image.save("drawing.png")
        
        # 保存轨迹到文件
        with open("trajectory.txt", "w") as f:
            for point in self.trajectory:
                f.write(f"{point[0]}, {point[1]}\n")
        
        # 清空轨迹
        self.trajectory = []

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()