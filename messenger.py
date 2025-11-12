import socket
import threading
import struct
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
import random

class MulticastMessenger:
    def __init__(self, workstation_id, multicast_group='224.1.1.1', port=5007):
        self.workstation_id = workstation_id
        self.multicast_group = multicast_group
        self.port = port
        self.running = True
        
        # Настройка multicast сокета
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Присоединение к multicast группе
        self.join_multicast_group()
        
    def join_multicast_group(self):
        """Присоединение к multicast группе"""
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock.bind(('', self.port))
    
    def send_message(self, message):
        """Отправка сообщения в multicast группу"""
        message_data = f"{self.workstation_id}:{message}"
        self.sock.sendto(message_data.encode('utf-8'), 
                        (self.multicast_group, self.port))
    
    def listen_messages(self, callback):
        """Прослушивание сообщений"""
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode('utf-8')
                if ':' in message:
                    workstation, msg = message.split(':', 1)
                    if workstation != self.workstation_id:
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        callback(workstation, msg, timestamp)
            except Exception as e:
                if self.running:
                    print(f"Ошибка приема: {e}")

def get_local_ip():
    """Получение локального IP адреса"""
    try:
        # Создаем временное соединение чтобы получить локальный IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def generate_nickname_with_ip():
    """Генерация ника с добавлением IP адреса"""
    ip = get_local_ip()
    
    # Список прилагательных и существительных для генерации имени
    adjectives = ["Быстрый", "Умный", "Смелый", "Веселый", "Серьезный", "Тихий", 
                 "Громкий", "Светлый", "Темный", "Красный", "Синий", "Зеленый",
                 "Стремительный", "Мощный", "Ловкий", "Хитрый", "Добрый", "Сильный"]
    
    nouns = ["Кот", "Пес", "Тигр", "Лев", "Орел", "Сокол", "Волк", "Медведь", 
            "Дракон", "Феникс", "Единорог", "Грифон", "Ястреб", "РысЬ", "Сова",
            "Дельфин", "Кит", "Акула", "Скат", "Орёл"]
    
    # Используем хэш IP для детерминированного выбора
    ip_hash = sum(int(octet) for octet in ip.split('.'))
    random.seed(ip_hash)
    
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    
    # Формируем имя в формате: Прилагательное_Существительное@IP
    return f"{adjective}_{noun}@{ip}"

class MAXMessengerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MAX Messenger")
        self.root.geometry("400x600")
        self.root.configure(bg='#2b2b2b')
        
        # Генерация ника с IP адресом
        self.workstation_id = generate_nickname_with_ip()
        self.messenger = MulticastMessenger(self.workstation_id)
        
        self.setup_ui()
        self.start_listening()
        
    def setup_ui(self):
        # Стиль для темной темы MAX
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка цветов
        bg_color = '#2b2b2b'
        accent_color = '#0078d7'
        text_color = '#ffffff'
        input_bg = '#3c3c3c'
        
        # Главный фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(header_frame, text="MAX Messenger", 
                              font=('Segoe UI', 16, 'bold'), 
                              fg=accent_color, bg=bg_color)
        title_label.pack(side=tk.LEFT)
        
        # Информация о пользователе
        user_label = tk.Label(header_frame, text=f"Вы: {self.workstation_id}", 
                             font=('Segoe UI', 10), fg=text_color, bg=bg_color)
        user_label.pack(side=tk.RIGHT)
        
        # Область сообщений
        self.chat_area = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD,
            width=50,
            height=25,
            font=('Segoe UI', 10),
            bg=input_bg,
            fg=text_color,
            insertbackground=text_color,
            state=tk.DISABLED
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Фрейм ввода сообщения
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        self.message_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 10),
            bg=input_bg,
            fg=text_color,
            insertbackground=text_color
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', self.send_message)
        
        self.send_button = tk.Button(
            input_frame,
            text="➤",
            font=('Segoe UI', 12, 'bold'),
            bg=accent_color,
            fg=text_color,
            relief=tk.FLAT,
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Статус бар
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="✓ Подключено к сети",
            font=('Segoe UI', 8),
            fg='#00ff00',
            bg=bg_color
        )
        self.status_label.pack(side=tk.LEFT)
        
        # IP информация
        ip_info = tk.Label(
            status_frame,
            text=f"IP: {get_local_ip()}",
            font=('Segoe UI', 8),
            fg='#888888',
            bg=bg_color
        )
        ip_info.pack(side=tk.RIGHT)
        
        # Добавляем приветственное сообщение
        self.add_system_message("Добро пожаловать в MAX Messenger!")
        self.add_system_message(f"Ваш ник: {self.workstation_id}")
        self.add_system_message(f"Ваш IP адрес: {get_local_ip()}")
        
    def add_message(self, sender, message, timestamp, is_own=False):
        self.chat_area.config(state=tk.NORMAL)
        
        if is_own:
            # Свои сообщения
            self.chat_area.insert(tk.END, f"[{timestamp}] ", 'time')
            self.chat_area.insert(tk.END, "Вы", 'own_sender')
            self.chat_area.insert(tk.END, f": {message}\n", 'own_message')
        else:
            # Сообщения других
            self.chat_area.insert(tk.END, f"[{timestamp}] ", 'time')
            self.chat_area.insert(tk.END, f"{sender}", 'other_sender')
            self.chat_area.insert(tk.END, f": {message}\n", 'other_message')
        
        # Настройка тегов для стилизации
        self.chat_area.tag_configure('time', foreground='#888888')
        self.chat_area.tag_configure('own_sender', foreground='#0078d7', font=('Segoe UI', 10, 'bold'))
        self.chat_area.tag_configure('own_message', foreground='#ffffff')
        self.chat_area.tag_configure('other_sender', foreground='#ff6b00', font=('Segoe UI', 10, 'bold'))
        self.chat_area.tag_configure('other_message', foreground='#e0e0e0')
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    def add_system_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"● {message}\n", 'system')
        self.chat_area.tag_configure('system', foreground='#888888', font=('Segoe UI', 9, 'italic'))
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            self.messenger.send_message(message)
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.add_message(self.workstation_id, message, timestamp, is_own=True)
            self.message_entry.delete(0, tk.END)
            
    def on_message_received(self, workstation, message, timestamp):
        self.add_message(workstation, message, timestamp, is_own=False)
        
    def start_listening(self):
        self.listener_thread = threading.Thread(
            target=self.messenger.listen_messages, 
            args=(self.on_message_received,),
            daemon=True
        )
        self.listener_thread.start()
        
    def on_closing(self):
        self.messenger.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MAXMessengerApp(root)
    
    # Обработка закрытия окна
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Устанавливаем фокус на поле ввода
    root.after(100, lambda: app.message_entry.focus_set())
    
    root.mainloop()