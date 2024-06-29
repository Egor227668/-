import random
from collections import defaultdict
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import scrolledtext

class Room:
    def __init__(self, capacity, price, count):
        self.capacity = capacity
        self.price = price
        self.count = count

    def __str__(self):
        return f"Вместимость: {self.capacity}, Цена: {self.price}, Доступно: {self.count}"

class Hotel:
    def __init__(self, rooms):
        self.rooms = rooms
        self.bookings = defaultdict(list)
        self.current_occupancy = defaultdict(int)

    def process_booking_request(self, current_time, text_box):
        room_type = random.choice(list(self.rooms.keys()))
        room = self.rooms[room_type]

        if room.count > 0:
            room.count -= 1
            confirmation_code = self.generate_confirmation_code()
            self.bookings[confirmation_code] = {
                'room_type': room_type,
                'check_in_date': current_time,
                'duration': random.randint(1, 7)
            }
            booking_info = self.bookings[confirmation_code]
            message = f"Бронь подтверждена на номер {room_type} с {current_time.date()} на {booking_info['duration']} дней. Код подтверждения: {confirmation_code}"
            self.display_message(text_box, message, color="green")
        else:
            message = f"Нет доступных номеров {room_type} на {current_time.date()}."
            self.display_message(text_box, message, color="red")

    def process_checkin_request(self, current_time, text_box):
        if len(self.bookings) > 0:
            confirmation_code = random.choice(list(self.bookings.keys()))
            booking_info = self.bookings.pop(confirmation_code)

            check_in_date = booking_info['check_in_date']
            room_type = booking_info['room_type']
            duration = booking_info['duration']

            occupied_dates = [check_in_date + timedelta(days=i) for i in range(duration)]
            for date in occupied_dates:
                self.current_occupancy[date] += 1

            message = f"Гость заселен в номер {room_type} на {check_in_date.date()} на {duration} дней."
            self.display_message(text_box, message, color="blue")

    def print_statistics(self, num_days, text_box):
        total_rooms = sum(room.count for room in self.rooms.values())
        total_occupied = sum(self.current_occupancy.values())
        occupancy_percent = (total_occupied / (total_rooms * num_days)) * 100

        self.display_message(text_box, "\nСтатистика загрузки отеля:\n", color="black")
        self.display_message(text_box, f"Всего номеров: {total_rooms}\n", color="black")
        self.display_message(text_box, f"Занятых дней: {total_occupied}\n", color="black")
        self.display_message(text_box, f"Загрузка: {occupancy_percent:.2f}%\n\n", color="black")

        self.display_message(text_box, "Загрузка по категориям:\n", color="black")
        for room_type, room in self.rooms.items():
            occupied_days = sum(self.current_occupancy[date] for date in self.current_occupancy if room.capacity >= 1)
            occupancy_percent = (occupied_days / (room.count * num_days)) * 100
            self.display_message(text_box, f"{room_type}: {occupancy_percent:.2f}%\n", color="black")

    def generate_confirmation_code(self):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

    def display_message(self, text_box, message, color="black"):
        text_box.configure(state=tk.NORMAL)
        text_box.insert(tk.END, message + "\n", color)
        text_box.configure(state=tk.DISABLED)

class SmallHotel(Hotel):
    def __init__(self, num_rooms):
        rooms = {
            'одноместный': Room(capacity=1, price=70, count=num_rooms),
            'полулюкс': Room(capacity=2, price=90, count=num_rooms),
            'двухместный': Room(capacity=2, price=100, count=num_rooms),
            'люкс': Room(capacity=3, price=120, count=num_rooms)
        }
        super().__init__(rooms)

    def simulate(self, num_days, text_box):
        current_time = datetime.now()
        end_time = current_time + timedelta(days=num_days)

        while current_time < end_time:
            next_event_time = current_time + timedelta(hours=random.randint(1, 5))
            current_time = next_event_time

            event_type = random.choice(['booking', 'check-in'])

            if event_type == 'booking':
                self.process_booking_request(current_time, text_box)
            elif event_type == 'check-in':
                self.process_checkin_request(current_time, text_box)

        self.print_statistics(num_days, text_box)

# GUI part
def create_gui():
    root = tk.Tk()
    root.title("Система управления отелем")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
    text_area.pack(padx=10, pady=10)

    small_hotel = SmallHotel(num_rooms=20)
    simulate_button = tk.Button(root, text="Моделировать", command=lambda: small_hotel.simulate(num_days=14, text_box=text_area))
    simulate_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
