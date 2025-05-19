import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk

# Завантаження змінних середовища
load_dotenv()
PORT = os.getenv('SERVER_PORT', '3000')  # Використовуємо порт 3000

class RobotManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Менеджер роботів")
        self.photos = []
        self.current_tab = None
        self.robot_list = self.load_robots()  # Завантажуємо список роботів для керування та видалення

        # Зображення зверху для інтуїтивного керування
        try:
            self.icon_image = Image.open("icon_robot.jpg")  # Заміни на шлях до власного зображення
            self.icon_image = self.icon_image.resize((200, 100), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(self.icon_image)
            self.icon_label = tk.Label(master, image=self.icon_photo)
            self.icon_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(master, text="Зображення не знайдено", font=("Arial", 12)).pack(pady=10)

        # Рамка для кнопок
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        # Кнопки у формі квадратиків
        self.add_button = tk.Button(self.button_frame, text="Додати нового робота", width=20, height=5, command=self.show_add_tab)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.manage_button = tk.Button(self.button_frame, text="Керувати роботами", width=20, height=5, command=self.show_manage_tab)
        self.manage_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Видалити робота", width=20, height=5, command=self.show_delete_tab)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        # Фрейм для вкладок
        self.tab_frame = tk.Frame(master)
        self.tab_frame.pack(pady=10, fill="both", expand=True)

        # Ініціалізація вкладок
        self.add_tab = None
        self.manage_tab = None
        self.delete_tab = None

    def load_robots(self):
        try:
            response = requests.get(f"http://localhost:{PORT}/robots")
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Помилка", f"Не вдалося завантажити список роботів. Статус-код: {response.status_code}")
                return []
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка з'єднання: {e}")
            return []

    def show_add_tab(self):
        if self.add_tab is None:
            self.add_tab = tk.Frame(self.tab_frame)
            tk.Label(self.add_tab, text="Додати нового робота", font=("Arial", 14, "bold")).pack(pady=5)

            # Поля для введення
            tk.Label(self.add_tab, text="Хто зробив робота:").pack()
            self.author_entry = tk.Entry(self.add_tab)
            self.author_entry.pack()

            tk.Label(self.add_tab, text="Назва робота:").pack()
            self.name_entry = tk.Entry(self.add_tab)
            self.name_entry.pack()

            tk.Label(self.add_tab, text="Опис робота:").pack()
            self.desc_text = tk.Text(self.add_tab, height=5, width=50)
            self.desc_text.pack()

            # Кнопка для завантаження фото
            self.upload_btn = tk.Button(self.add_tab, text="Додати фото", command=self.upload_photos)
            self.upload_btn.pack(pady=5)

            # Фрейм для перегляду фото
            self.photo_frame = tk.Frame(self.add_tab)
            self.photo_frame.pack(pady=5)
            self.photo_labels = []

            # Кнопка для відправлення
            self.submit_btn = tk.Button(self.add_tab, text="Додати робота", command=self.submit_robot)
            self.submit_btn.pack(pady=5)

        self.hide_all_tabs()
        self.add_tab.pack(fill="both", expand=True)
        self.current_tab = self.add_tab

    def show_manage_tab(self):
        if self.manage_tab is None:
            self.manage_tab = tk.Frame(self.tab_frame)
            tk.Label(self.manage_tab, text="Керувати роботами", font=("Arial", 14, "bold")).pack(pady=5)

            # Список роботів для редагування
            self.robot_listbox = tk.Listbox(self.manage_tab, height=10, width=50)
            self.robot_listbox.pack(pady=5)
            self.update_robot_list()

            # Поля для редагування
            tk.Label(self.manage_tab, text="Новий автор:").pack()
            self.new_author_entry = tk.Entry(self.manage_tab)
            self.new_author_entry.pack()

            tk.Label(self.manage_tab, text="Нова назва:").pack()
            self.new_name_entry = tk.Entry(self.manage_tab)
            self.new_name_entry.pack()

            tk.Label(self.manage_tab, text="Новий опис:").pack()
            self.new_desc_text = tk.Text(self.manage_tab, height=5, width=50)
            self.new_desc_text.pack()

            # Кнопка для завантаження нового фото
            self.manage_upload_btn = tk.Button(self.manage_tab, text="Оновити фото", command=self.upload_new_photos)
            self.manage_upload_btn.pack(pady=5)

            # Кнопка для збереження змін
            self.save_btn = tk.Button(self.manage_tab, text="Зберегти зміни", command=self.save_changes)
            self.save_btn.pack(pady=5)

        self.hide_all_tabs()
        self.manage_tab.pack(fill="both", expand=True)
        self.current_tab = self.manage_tab

    def show_delete_tab(self):
        if self.delete_tab is None:
            self.delete_tab = tk.Frame(self.tab_frame)
            tk.Label(self.delete_tab, text="Видалити робота", font=("Arial", 14, "bold")).pack(pady=5)

            # Список роботів для видалення
            self.delete_listbox = tk.Listbox(self.delete_tab, height=10, width=50)
            self.delete_listbox.pack(pady=5)
            self.update_robot_list()

            # Кнопка для видалення
            self.delete_btn = tk.Button(self.delete_tab, text="Видалити обраного робота", command=self.delete_robot)
            self.delete_btn.pack(pady=5)

        self.hide_all_tabs()
        self.delete_tab.pack(fill="both", expand=True)
        self.current_tab = self.delete_tab

    def hide_all_tabs(self):
        if self.add_tab: self.add_tab.pack_forget()
        if self.manage_tab: self.manage_tab.pack_forget()
        if self.delete_tab: self.delete_tab.pack_forget()

    def upload_photos(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        for file in files:
            if file not in self.photos:
                self.photos.append(file)
                img = Image.open(file)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label = tk.Label(self.photo_frame, image=photo)
                label.image = photo  # Зберігаємо посилання, щоб уникнути очищення GC
                label.pack(side=tk.LEFT, padx=5)
                self.photo_labels.append(label)
        messagebox.showinfo("Фото завантажені", f"Обрано {len(self.photos)} фото")

    def upload_new_photos(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        self.photos.extend(files)  # Додаємо нові фото до списку
        messagebox.showinfo("Успіх", "Фото додано для оновлення!")

    def submit_robot(self):
        author = self.author_entry.get()
        name = self.name_entry.get()
        desc = self.desc_text.get("1.0", tk.END).strip()

        if not author or not name or not desc or not self.photos:
            messagebox.showerror("Помилка", "Заповни всі поля і вибери фото")
            return

        files = [('images', (os.path.basename(photo), open(photo, 'rb'), 'image/jpeg')) for photo in self.photos]
        data = {'author': author, 'name': name, 'description': desc}

        try:
            print(f"Sending request to http://localhost:{PORT}/add_robot")
            response = requests.post(f"http://localhost:{PORT}/add_robot", data=data, files=files, timeout=5)
            print(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                messagebox.showinfo("Успіх", "Робота додано!")
                self.author_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.desc_text.delete("1.0", tk.END)
                for label in self.photo_labels:
                    label.destroy()
                self.photos = []
                self.photo_labels = []
                self.robot_list = self.load_robots()  # Оновлюємо список роботів
                self.update_robot_list()
            else:
                messagebox.showerror("Помилка", f"Статус-код: {response.status_code}")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Помилка", f"Не вдалося підключитися до сервера. Переконайся, що сервер запущений на localhost:{PORT}.")
        except requests.exceptions.Timeout:
            messagebox.showerror("Помилка", f"Сервер не відповідає (тайм-аут) на localhost:{PORT}.")
        except Exception as e:
            messagebox.showerror("Помилка з'єднання", str(e))

    def update_robot_list(self):
        if self.manage_tab and hasattr(self, 'robot_listbox'):
            self.robot_listbox.delete(0, tk.END)
            for i, robot in enumerate(self.robot_list):
                name = robot.get('name', 'Робот без назви')  # Використовуємо get із значенням за замовчуванням
                self.robot_listbox.insert(tk.END, f"{name} (ID: {i})")
        if self.delete_tab and hasattr(self, 'delete_listbox'):
            self.delete_listbox.delete(0, tk.END)
            for i, robot in enumerate(self.robot_list):
                name = robot.get('name', 'Робот без назви')  # Використовуємо get із значенням за замовчуванням
                self.delete_listbox.insert(tk.END, f"{name} (ID: {i})")

    def save_changes(self):
        selected_index = self.robot_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            robot = self.robot_list[index]
            new_author = self.new_author_entry.get()
            new_name = self.new_name_entry.get()
            new_desc = self.new_desc_text.get("1.0", tk.END).strip()

            # Формуємо дані для оновлення
            data = {}
            if new_author:
                data['author'] = new_author
            if new_name:
                data['name'] = new_name
            if new_desc:
                data['description'] = new_desc

            # Якщо є нові фото, додаємо їх
            files = [('images', (os.path.basename(photo), open(photo, 'rb'), 'image/jpeg')) for photo in self.photos] if self.photos else []

            try:
                response = requests.put(f"http://localhost:{PORT}/update_robot/{index}", data=data, files=files, timeout=5)
                if response.status_code == 200:
                    messagebox.showinfo("Успіх", "Робота оновлено!")
                    self.robot_list = self.load_robots()  # Оновлюємо список
                    self.update_robot_list()
                    self.new_author_entry.delete(0, tk.END)
                    self.new_name_entry.delete(0, tk.END)
                    self.new_desc_text.delete("1.0", tk.END)
                    self.photos = []  # Очищаємо список фото після оновлення
                else:
                    messagebox.showerror("Помилка", f"Статус-код: {response.status_code}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Помилка", f"Не вдалося підключитися до сервера. Переконайся, що сервер запущений на localhost:{PORT}.")
            except requests.exceptions.Timeout:
                messagebox.showerror("Помилка", f"Сервер не відповідає (тайм-аут) на localhost:{PORT}.")
            except Exception as e:
                messagebox.showerror("Помилка з'єднання", str(e))

    def delete_robot(self):
        selected_index = self.delete_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            try:
                response = requests.delete(f"http://localhost:{PORT}/delete_robot/{index}", timeout=5)
                if response.status_code == 200:
                    messagebox.showinfo("Успіх", "Робота видалено!")
                    self.robot_list = self.load_robots()  # Оновлюємо список
                    self.update_robot_list()
                else:
                    messagebox.showerror("Помилка", f"Статус-код: {response.status_code}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Помилка", f"Не вдалося підключитися до сервера. Переконайся, що сервер запущений на localhost:{PORT}.")
            except requests.exceptions.Timeout:
                messagebox.showerror("Помилка", f"Сервер не відповідає (тайм-аут) на localhost:{PORT}.")
            except Exception as e:
                messagebox.showerror("Помилка з'єднання", str(e))

root = tk.Tk()
app = RobotManager(root)
root.mainloop()