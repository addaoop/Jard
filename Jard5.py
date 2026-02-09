# -*- coding: utf-8 -*-

import os
import datetime
import webbrowser
import urllib.parse

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle

# تشغيل Full Screen
Window.fullscreen = True

PROJECT_FOLDER = "/storage/emulated/0/ZumJard"


# ==========================
# صف الصنف
# ==========================
class ItemRow(GridLayout):
    def __init__(self, img, name, **kwargs):
        super().__init__(cols=5, size_hint_y=None, height=90, spacing=6)

        self.item_name = name

        # AVAILABLE (وسط)
        self.available = TextInput(
            multiline=False,
            input_filter="float",
            input_type="number",
            halign="center"
        )
        self.available.bind(text=self.calc)
        self.add_widget(self.available)

        # SELL (وسط)
        self.sell = Label(
            text="0",
            bold=True,
            color=(0,0,0,1),
            halign="center",
            valign="middle"
        )
        self.sell.bind(size=self.sell.setter('text_size'))
        self.add_widget(self.sell)

        # BUY (وسط)
        self.buy = TextInput(
            multiline=False,
            input_filter="float",
            input_type="number",
            halign="center"
        )
        self.buy.bind(text=self.calc)
        self.add_widget(self.buy)

        # START (وسط)
        self.start = TextInput(
            multiline=False,
            input_filter="float",
            input_type="number",
            halign="center"
        )
        self.start.bind(text=self.calc)
        self.add_widget(self.start)

        # IMAGE
        self.add_widget(
            Image(source=img, allow_stretch=True, keep_ratio=True)
        )

    def calc(self, *args):
        try:
            s = float(self.start.text) if self.start.text else 0
            b = float(self.buy.text) if self.buy.text else 0
            a = float(self.available.text) if self.available.text else 0

            result = s + b - a

            self.sell.text = str(int(result))

            if result < 0:
                self.sell.color = (1,0,0,1)
            else:
                self.sell.color = (0,0,0,1)

        except:
            pass

    def get_values(self):
        return (
            self.start.text or "0",
            self.buy.text or "0",
            self.sell.text or "0",
            self.available.text or "0",
        )


# ==========================
# التطبيق
# ==========================
class InventoryApp(App):

    def build(self):

        self.rows = []

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        with root.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(size=root.size, pos=root.pos)
        root.bind(size=self._update_rect, pos=self._update_rect)

        today = datetime.date.today().strftime("%Y-%m-%d")

        title = Label(
            text=f"Zummaria Inventory - {today}",
            size_hint_y=None,
            height=40,
            color=(0,0,0,1)
        )
        root.add_widget(title)

        # HEADER بالصور العربية
        header = GridLayout(cols=5, size_hint_y=None, height=60)

        header_images = [
            "available.jpg",
            "sell.jpg",
            "buy.jpg",
            "start.jpg",
            "item.jpg"
        ]

        for img in header_images:
            header.add_widget(
                Image(source=os.path.join(PROJECT_FOLDER, img),
                      allow_stretch=True,
                      keep_ratio=True)
            )

        root.add_widget(header)

        self.container = GridLayout(cols=1, size_hint_y=None, spacing=6)
        self.container.bind(minimum_height=self.container.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.container)
        root.add_widget(scroll)

        images = []

        if os.path.exists(PROJECT_FOLDER):
            for file in os.listdir(PROJECT_FOLDER):
                if file.lower().endswith(".jpg"):
                    if file in ["available.jpg","sell.jpg","buy.jpg","start.jpg","item.jpg"]:
                        continue
                    images.append(file)

        images.sort()

        for img in images:
            full_path = os.path.join(PROJECT_FOLDER, img)
            name = img.replace(".jpg", "")
            self.add_row(full_path, name)

        wa_btn = Button(
            text="SEND WHATSAPP",
            size_hint_y=None,
            height=90,
            background_color=(1,0.6,0.2,1)
        )
        wa_btn.bind(on_press=self.send_whatsapp)

        root.add_widget(wa_btn)

        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def add_row(self, img, name):
        row = ItemRow(img, name)
        self.container.add_widget(row)
        self.rows.append(row)

    def send_whatsapp(self, instance):

        today = datetime.date.today().strftime("%Y-%m-%d")

        msg = f"📊 جرد زُمّاريا - {today}\n"
        msg += "====================\n\n"

        for row in self.rows:

            start, buy, sell, av = row.get_values()

            msg += f"📦 {row.item_name}\n"
            msg += f"بداية : {start}\n"
            msg += f"مشتريات : {buy}\n"
            msg += f"مباع : {sell}\n"
            msg += f"متوفر : {av}\n"
            msg += "------------------\n"

        url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        webbrowser.open(url)


if __name__ == "__main__":
    InventoryApp().run()