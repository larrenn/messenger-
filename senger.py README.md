[1mdiff --git a/messenger.py b/messenger.py[m
[1mindex 536ce86..dcc2d02 100644[m
[1m--- a/messenger.py[m
[1m+++ b/messenger.py[m
[36m@@ -97,8 +97,130 @@[m [mclass MAXMessengerApp:[m
         [m
         self.setup_ui()[m
         self.start_listening()[m
[32m+[m
[32m+[m[41m    [m
[32m+[m[32m    def setup_enhanced_features(self):[m
[32m+[m[32m        """Настройка расширенных функций"""[m
[32m+[m[32m        # Создаем меню с быстрыми сообщениями[m
[32m+[m[32m        self.predefined_messages = create_predefined_messages()[m
[32m+[m[41m        [m
[32m+[m[32m        # Создаем пользователя для текущей сессии[m
[32m+[m[32m        self.current_user = user_manager.create_user(self.workstation_id)[m
[32m+[m[32m        user_manager.user_login(self.current_user)[m
[32m+[m[41m        [m
[32m+[m[32m        # Добавляем системное сообщение о новых функциях[m
[32m+[m[32m        self.add_system_message("Расширенные функции активированы!")[m
[32m+[m[32m        self.add_system_message("Доступны: форматирование, история сообщений, управление пользователями")[m
[32m+[m
[32m+[m[32m    def send_formatted_message(self, message, style="normal"):[m
[32m+[m[32m        """Отправка форматированного сообщения"""[m
[32m+[m[32m        formatted_message = format_message(message, style)[m
[32m+[m[32m        self.messenger.send_message(formatted_message)[m
[32m+[m[32m        timestamp = datetime.now().strftime('%H:%M:%S')[m
[32m+[m[41m        [m
[32m+[m[32m        # Добавляем в историю[m
[32m+[m[32m        message_history.add_message(self.workstation_id, message, timestamp)[m
[32m+[m[32m        user_manager.increment_message_count(self.current_user['user_id'])[m
[32m+[m[41m        [m
[32m+[m[32m        self.add_message(self.workstation_id, formatted_message, timestamp, is_own=True)[m
[32m+[m
[32m+[m[32m    def search_message_history(self, keyword):[m
[32m+[m[32m        """Поиск в истории сообщений"""[m
[32m+[m[32m        results = message_history.search_messages(keyword)[m
[32m+[m[32m        if results:[m
[32m+[m[32m            self.add_system_message(f"Найдено сообщений по запросу '{keyword}': {len(results)}")[m
[32m+[m[32m            for msg in results[-5:]:  # Показываем последние 5 результатов[m
[32m+[m[32m                self.add_system_message(f"[{msg['timestamp']}] {msg['sender']}: {msg['message']}")[m
[32m+[m[32m        else:[m
[32m+[m[32m            self.add_system_message(f"Сообщения по запросу '{keyword}' не найдены")[m
[32m+[m
[32m+[m[32m    def show_user_statistics(self):[m
[32m+[m[32m        """Показывает статистику пользователя"""[m
[32m+[m[32m        stats = user_manager.get_user_stats(self.current_user['user_id'])[m
[32m+[m[32m        online_users = user_manager.get_online_users()[m
[32m+[m[32m        self.add_system_message(stats)[m
[32m+[m[32m        self.add_system_message(f"👥 Пользователей онлайн: {len(online_users)}")[m
[32m+[m
[32m+[m[32m    def send_quick_message(self, message_type):[m
[32m+[m[32m        """Отправка предопределенного сообщения"""[m
[32m+[m[32m        if message_type in self.predefined_messages:[m
[32m+[m[32m            message = self.predefined_messages[message_type][m
[32m+[m[32m            self.send_formatted_message(message)[m[41m    [m
         [m
     def setup_ui(self):[m
[32m+[m[41m        [m
[32m+[m[32m        quick_messages_frame = ttk.Frame(main_frame)[m
[32m+[m[32m        quick_messages_frame.pack(fill=tk.X, pady=(5, 10))[m
[32m+[m
[32m+[m[32m        quick_label = tk.Label(quick_messages_frame, text="Быстрые сообщения:",[m[41m [m
[32m+[m[32m                              font=('Segoe UI', 9), fg='#cccccc', bg=bg_color)[m
[32m+[m[32m        quick_label.pack(anchor=tk.W)[m
[32m+[m
[32m+[m[32m        quick_buttons_frame = ttk.Frame(quick_messages_frame)[m
[32m+[m[32m        quick_buttons_frame.pack(fill=tk.X, pady=(5, 0))[m
[32m+[m
[32m+[m[32m        # Кнопки быстрых сообщений[m
[32m+[m[32m        quick_messages = {[m
[32m+[m[32m            "👋": "greeting",[m
[32m+[m[32m            "❔": "question",[m[41m [m
[32m+[m[32m            "✅": "agree",[m
[32m+[m[32m            "🙏": "thanks",[m
[32m+[m[32m            "🎉": "celebrate"[m
[32m+[m[32m        }[m
[32m+[m
[32m+[m[32m        for emoji, msg_type in quick_messages.items():[m
[32m+[m[32m            btn = tk.Button([m
[32m+[m[32m                quick_buttons_frame,[m
[32m+[m[32m                text=emoji,[m
[32m+[m[32m                font=('Segoe UI', 10),[m
[32m+[m[32m                bg='#3c3c3c',[m
[32m+[m[32m                fg='#ffffff',[m
[32m+[m[32m                relief=tk.FLAT,[m
[32m+[m[32m                width=3,[m
[32m+[m[32m                command=lambda mt=msg_type: self.send_quick_message(mt)[m
[32m+[m[32m            )[m
[32m+[m[32m            btn.pack(side=tk.LEFT, padx=(0, 5))[m
[32m+[m
[32m+[m[32m        # КНОПКИ ДОПОЛНИТЕЛЬНЫХ ФУНКЦИЙ[m
[32m+[m[32m        tools_frame = ttk.Frame(main_frame)[m
[32m+[m[32m        tools_frame.pack(fill=tk.X, pady=(5, 0))[m
[32m+[m
[32m+[m[32m        # Кнопка поиска[m
[32m+[m[32m        search_btn = tk.Button([m
[32m+[m[32m            tools_frame,[m
[32m+[m[32m            text="🔍 Поиск",[m
[32m+[m[32m            font=('Segoe UI', 9),[m
[32m+[m[32m            bg='#3c3c3c',[m
[32m+[m[32m            fg='#ffffff',[m
[32m+[m[32m            relief=tk.FLAT,[m
[32m+[m[32m            command=self.open_search_dialog[m
[32m+[m[32m        )[m
[32m+[m[32m        search_btn.pack(side=tk.LEFT, padx=(0, 5))[m
[32m+[m
[32m+[m[32m        # Кнопка статистики[m
[32m+[m[32m        stats_btn = tk.Button([m
[32m+[m[32m            tools_frame,[m
[32m+[m[32m            text="📊 Статистика",[m
[32m+[m[32m            font=('Segoe UI', 9),[m
[32m+[m[32m            bg='#3c3c3c',[m
[32m+[m[32m            fg='#ffffff',[m
[32m+[m[32m            relief=tk.FLAT,[m
[32m+[m[32m            command=self.show_user_statistics[m
[32m+[m[32m        )[m
[32m+[m[32m        stats_btn.pack(side=tk.LEFT, padx=(0, 5))[m
[32m+[m
[32m+[m[32m        # Кнопка стилей сообщений[m
[32m+[m[32m        styles_btn = tk.Button([m
[32m+[m[32m            tools_frame,[m
[32m+[m[32m            text="🎨 Стили",[m
[32m+[m[32m            font=('Segoe UI', 9),[m
[32m+[m[32m            bg='#3c3c3c',[m
[32m+[m[32m            fg='#ffffff',[m
[32m+[m[32m            relief=tk.FLAT,[m
[32m+[m[32m            command=self.show_styles_demo[m
[32m+[m[32m        )[m
[32m+[m[32m        styles_btn.pack(side=tk.LEFT)[m[41m    [m
[32m+[m
         # Стиль для темной темы MAX[m
         style = ttk.Style()[m
         style.theme_use('clam')[m
[36m@@ -247,6 +369,170 @@[m [mclass MAXMessengerApp:[m
     def on_closing(self):[m
         self.messenger.running = False[m
         self.root.destroy()[m
[32m+[m[32m    # =============================================================================[m
[32m+[m[32m# НОВЫЕ ФУНКЦИИ ФОРМАТИРОВАНИЯ СООБЩЕНИЙ[m
[32m+[m[32m# =============================================================================[m
[32m+[m
[32m+[m[32mdef format_message(text, style="normal"):[m
[32m+[m[32m    """[m
[32m+[m[32m    Форматирует текст сообщения согласно выбранному стилю[m
[32m+[m[32m    """[m
[32m+[m[32m    styles = {[m
[32m+[m[32m        "normal": text,[m
[32m+[m[32m        "upper": text.upper(),[m
[32m+[m[32m        "lower": text.lower(),[m
[32m+[m[32m        "title": text.title(),[m
[32m+[m[32m        "bold": f"**{text}**",[m
[32m+[m[32m        "italic": f"_{text}_",[m
[32m+[m[32m        "code": f"`{text}`",[m
[32m+[m[32m        "quote": f"> {text}",[m
[32m+[m[32m        "spoiler": f"||{text}||"[m
[32m+[m[32m    }[m
[32m+[m[41m    [m
[32m+[m[32m    return styles.get(style, text)[m
[32m+[m
[32m+[m[32mdef show_message_styles():[m
[32m+[m[32m    """[m
[32m+[m[32m    Демонстрирует все доступные стили сообщений[m
[32m+[m[32m    """[m
[32m+[m[32m    test_text = "Привет, это тестовое сообщение"[m
[32m+[m[32m    print("Доступные стили сообщений:")[m
[32m+[m[32m    for style in ["normal", "upper", "lower", "title", "bold", "italic", "code", "quote", "spoiler"]:[m
[32m+[m[32m        formatted = format_message(test_text, style)[m
[32m+[m[32m        print(f"- {style}: {formatted}")[m
[32m+[m
[32m+[m[32mdef create_predefined_messages():[m
[32m+[m[32m    """[m
[32m+[m[32m    Создает набор предопределенных сообщений для быстрой отправки[m
[32m+[m[32m    """[m
[32m+[m[32m    messages = {[m
[32m+[m[32m        "greeting": "👋 Привет всем!",[m
[32m+[m[32m        "question": "❔ Есть вопрос...",[m
[32m+[m[32m        "agree": "✅ Согласен",[m
[32m+[m[32m        "disagree": "❌ Не согласен",[m
[32m+[m[32m        "thanks": "🙏 Спасибо!",[m
[32m+[m[32m        "warning": "⚠️ Внимание!",[m
[32m+[m[32m        "celebrate": "🎉 Ура!",[m
[32m+[m[32m        "thinking": "🤔 Дайте подумать..."[m
[32m+[m[32m    }[m
[32m+[m[32m    return messages[m
[32m+[m
[32m+[m[32m# =============================================================================[m
[32m+[m[32m# КЛАСС ДЛЯ УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ[m
[32m+[m[32m# =============================================================================[m
[32m+[m
[32m+[m[32mclass UserManager:[m
[32m+[m[32m    def __init__(self):[m
[32m+[m[32m        self.users = {}[m
[32m+[m[32m        self.current_user = None[m
[32m+[m[41m    [m
[32m+[m[32m    def create_user(self, username):[m
[32m+[m[32m        """Создает нового пользователя"""[m
[32m+[m[32m        import random[m
[32m+[m[32m        user_id = random.randint(1000, 9999)[m
[32m+[m[32m        user = {[m
[32m+[m[32m            'username': username,[m
[32m+[m[32m            'user_id': user_id,[m
[32m+[m[32m            'is_online': True,[m
[32m+[m[32m            'join_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),[m
[32m+[m[32m            'message_count': 0[m
[32m+[m[32m        }[m
[32m+[m[32m        self.users[user_id] = user[m
[32m+[m[32m        return user[m
[32m+[m[41m    [m
[32m+[m[32m    def user_login(self, user):[m
[32m+[m[32m        """Вход пользователя в систему"""[m
[32m+[m[32m        user['is_online'] = True[m
[32m+[m[32m        return f"👋 {user['username']} вошел в систему"[m
[32m+[m[41m    [m
[32m+[m[32m    def user_logout(self, user):[m
[32m+[m[32m        """Выход пользователя из системы"""[m
[32m+[m[32m        user['is_online'] = False[m
[32m+[m[32m        return f"🚪 {user['username']} вышел из системы"[m
[32m+[m[41m    [m
[32m+[m[32m    def get_online_users(self):[m
[32m+[m[32m        """Возвращает список онлайн пользователей"""[m
[32m+[m[32m        return [user for user in self.users.values() if user['is_online']][m
[32m+[m[41m    [m
[32m+[m[32m    def increment_message_count(self, user_id):[m
[32m+[m[32m        """Увеличивает счетчик сообщений пользователя"""[m
[32m+[m[32m        if user_id in self.users:[m
[32m+[m[32m            self.users[user_id]['message_count'] += 1[m
[32m+[m[41m    [m
[32m+[m[32m    def get_user_stats(self, user_id):[m
[32m+[m[32m        """Возвращает статистику пользователя"""[m
[32m+[m[32m        if user_id in self.users:[m
[32m+[m[32m            user = self.users[user_id][m
[32m+[m[32m            return f"📊 {user['username']}: {user['message_count']} сообщений"[m
[32m+[m[32m        return "Пользователь не найден"[m
[32m+[m
[32m+[m[32m# =============================================================================[m
[32m+[m[32m# ФУНКЦИИ ДЛЯ РАБОТЫ С ИСТОРИЕЙ СООБЩЕНИЙ[m
[32m+[m[32m# =============================================================================[m
[32m+[m
[32m+[m[32mclass MessageHistory:[m
[32m+[m[32m    def __init__(self, max_messages=1000):[m
[32m+[m[32m        self.messages = [][m
[32m+[m[32m        self.max_messages = max_messages[m
[32m+[m[41m    [m
[32m+[m[32m    def add_message(self, sender, message, timestamp):[m
[32m+[m[32m        """Добавляет сообщение в историю"""[m
[32m+[m[32m        message_data = {[m
[32m+[m[32m            'sender': sender,[m
[32m+[m[32m            'message': message,[m
[32m+[m[32m            'timestamp': timestamp,[m
[32m+[m[32m            'id': len(self.messages) + 1[m
[32m+[m[32m        }[m
[32m+[m[32m        self.messages.append(message_data)[m
[32m+[m[41m        [m
[32m+[m[32m        # Ограничиваем размер истории[m
[32m+[m[32m        if len(self.messages) > self.max_messages:[m
[32m+[m[32m            self.messages.pop(0)[m
[32m+[m[41m    [m
[32m+[m[32m    def search_messages(self, keyword):[m
[32m+[m[32m        """Поиск сообщений по ключевому слову"""[m
[32m+[m[32m        results = [][m
[32m+[m[32m        for msg in self.messages:[m
[32m+[m[32m            if keyword.lower() in msg['message'].lower():[m
[32m+[m[32m                results.append(msg)[m
[32m+[m[32m        return results[m
[32m+[m[41m    [m
[32m+[m[32m    def get_user_messages(self, username):[m
[32m+[m[32m        """Получает все сообщения определенного пользователя"""[m
[32m+[m[32m        return [msg for msg in self.messages if msg['sender'] == username][m
[32m+[m[41m    [m
[32m+[m[32m    def clear_history(self):[m
[32m+[m[32m        """Очищает историю сообщений"""[m
[32m+[m[32m        self.messages.clear()[m
[32m+[m
[32m+[m[32m# =============================================================================[m
[32m+[m[32m# УТИЛИТЫ ДЛЯ РАБОТЫ С ВРЕМЕНЕМ[m
[32m+[m[32m# =============================================================================[m
[32m+[m
[32m+[m[32mdef get_current_time():[m
[32m+[m[32m    """Возвращает текущее время в красивом формате"""[m
[32m+[m[32m    now = datetime.now()[m
[32m+[m[32m    return {[m
[32m+[m[32m        'time': now.strftime('%H:%M:%S'),[m
[32m+[m[32m        'date': now.strftime('%Y-%m-%d'),[m
[32m+[m[32m        'full': now.strftime('%Y-%m-%d %H:%M:%S'),[m
[32m+[m[32m        'pretty': now.strftime('%d %B %Y, %H:%M')[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32mdef format_duration(seconds):[m
[32m+[m[32m    """Форматирует длительность в читаемый вид"""[m
[32m+[m[32m    if seconds < 60:[m
[32m+[m[32m        return f"{seconds} сек"[m
[32m+[m[32m