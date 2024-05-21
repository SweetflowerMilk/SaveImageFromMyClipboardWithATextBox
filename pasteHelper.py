import os
import tkinter as tk
from tkinter import Text, Menu, filedialog, messagebox
from PIL import Image, ImageGrab, ImageTk
import pyautogui
import time


class ImageTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image and Text Input")
        self.root.geometry("800x600")

        self.text_box = Text(root, wrap='word')
        self.text_box.pack(expand='yes', fill='both')

        # 将 Ctrl+V 绑定到 paste_image 方法
        self.root.bind("<Control-v>", self.paste_image)
        # 将 Ctrl+S 绑定到 save_text 方法
        self.root.bind("<Control-s>", self.save_text)

        # 添加菜单
        self.menu = Menu(root)
        self.root.config(menu=self.menu)

        # 文件菜单
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Text (Ctrl+S)", command=self.save_text)
        self.file_menu.add_command(label="Set Save Path", command=self.set_save_path)

        # 设置默认保存路径
        self.default_save_path = "D:\\desktop"
        self.save_path = self.default_save_path

        # 添加窗口关闭时的处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 加载上次保存的图片
        self.load_last_saved_image()

    def paste_image(self, event=None):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(self.save_path, f"pasted_image_{timestamp}.png")
                image.save(image_path, 'PNG')
                print(f"Image pasted and saved to {image_path}")

                # 显示刚刚保存的图片
                self.show_image(image_path)
        except Exception as e:
            print(f"Error: {e}")

        # 检查是否按下了 Ctrl+Shift+S
        if event and event.state == 12 and event.keysym.lower() == "s":
            self.save_clipboard_image()

    def save_clipboard_image(self):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(self.save_path, f"clipboard_image_{timestamp}.png")
                image.save(image_path, 'PNG')
                print(f"Clipboard image saved to {image_path}")
                self.show_image(image_path)
        except Exception as e:
            print(f"Error: {e}")

    def save_text(self, event=None):
        text = self.text_box.get("1.0", "end-1c")
        if text:
            filename = filedialog.asksaveasfilename(initialdir=self.default_save_path, title="Save Text",
                                                    filetypes=[("Text files", "*.txt")])
            if filename:
                with open(filename, "w") as file:
                    file.write(text)
                print(f"Text saved to {filename}")
                self.root.destroy()

    def set_save_path(self):
        # 弹出选择保存路径对话框
        save_path = filedialog.askdirectory(initialdir=self.default_save_path)
        if save_path:
            # 保存选择的路径
            self.save_path = save_path

    def on_closing(self):
        text = self.text_box.get("1.0", "end-1c")
        if text:
            answer = messagebox.askyesnocancel("Save Text", "Do you want to save the text before closing?")
            if answer is True:
                self.save_text()
            elif answer is False:
                self.root.destroy()
        else:
            self.root.destroy()

    def load_last_saved_image(self):
        # 尝试加载上次保存的图片
        last_saved_images = [f for f in os.listdir(self.save_path) if f.startswith("clipboard_image_")]
        if last_saved_images:
            last_saved_image_path = os.path.join(self.save_path, last_saved_images[-1])
            self.show_image(last_saved_image_path)

    def show_image(self, image_path):
        # 显示图片到界面上
        image = Image.open(image_path)
        image.thumbnail((200, 200))
        imgtk = ImageTk.PhotoImage(image=image)
        self.image_label = tk.Label(self.root, image=imgtk)
        self.image_label.image = imgtk
        self.image_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTextApp(root)
    root.mainloop()
