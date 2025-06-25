import os
import json
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from datetime import datetime

def combine(path): return os.path.join("icons", path)

class LightModeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.theme_icon = "sun.png"
        self.day_counter = self.sub_header = self.header = None
        self.page_label = self.day_entry = self.container = self.month_entry = self.data_of_the_day = self.clicks_pos = \
            self.processed_data = self.text_color_ = self.frame_color_ = self.container_color_ = self.border_color_ = \
            self.inp_color_ = None
        self.clicked = -1
        self.geometry("500x620")
        self.title("Calendar of Event - Personal Daily Knowledge Assistant")
        self.font_ap = "Aptos"
        self.JSON_PATH = "title_img_pos.json"
        self.change_mode = True
        self.today_date, self.today_month = str(int(datetime.now().strftime("%d"))), datetime.now().strftime("%B")
        self.bind("<Return>", self.event_handling)

    def event_handling(self, event):
        if event.keysym == "Return":
            self.find_data()
            print("CLicked")

    def change_theme(self):
        if self.change_mode:
            self.change_mode = False
            ctk.set_appearance_mode("light")
            self.configure(fg_color="#FFF")
            self.text_color_ = "#111"
            self.frame_color_ = "#E5E5E5"
            self.container_color_ = "#CCC"
            self.border_color_ = "#fff"
            self.inp_color_ = "#DCDCDC"
            self.theme_icon = "moon.png"
            print("LIGHT")
        else:
            self.change_mode = True
            ctk.set_appearance_mode("dark")
            self.configure(fg_color="#1e1e1e")
            self.text_color_ = "#DCDCDC"
            self.frame_color_ = "#444"
            self.container_color_ = "#222"
            self.border_color_ = "#fff"
            self.inp_color_ = "#222"
            self.theme_icon = "sun.png"
            print("DARK")
        self.header.configure(text_color=self.text_color_)
        self.sub_header.configure(text_color=self.text_color_)
        self.day_entry.configure(bg_color=self.inp_color_, text_color=self.text_color_)
        self.month_entry.configure(bg_color=self.inp_color_, text_color=self.text_color_)
        self.add_icon_button(self.theme_icon, 440, 15, 30, self.change_theme)

    def load_data(self):
        try:
            with open(self.JSON_PATH, "r") as f:
                reading = json.load(f)
                return reading[self.today_month.lower()][self.today_date]
        except Exception as e:
            messagebox.showerror("Error", f"There is no data found!\n{str(e)}")
            try:
                self.today_date, self.today_month = str(int(datetime.now().strftime("%d"))), datetime.now().strftime("%B")
                return reading[self.today_month.lower()][self.today_date]
            except Exception as e:
                messagebox.showerror("No data found", "Record data is not available, please contact to the administrator")
                print("Error loading JSON data:", e)
            return [[], []]

    def find_data(self):
        self.today_date = self.day_entry.get().strip() if self.day_entry.get() else self.today_date
        self.today_month = self.month_entry.get().strip() if self.month_entry.get() else self.today_month
        self.clicked = -1
        self.clean_screen()
        self.background_process()
        self.screen_()
        self.right_btn()

    def background_process(self):
        loading = self.load_data()
        if not loading[0] or not loading[1]:
            self.data_of_the_day = 0
            self.processed_data = []
            self.clicks_pos = 0
            return
        position = loading[0]
        images = loading[1]
        self.data_of_the_day = len(images)
        self.clicks_pos = -(-self.data_of_the_day // 5)

        grouped = []
        for i in range(0, len(position), 5):
            batch = list(zip(position[i:i + 5], images[i:i + 5]))
            grouped.append(batch)

        self.processed_data = grouped

    def screen_(self):
        # Title
        self.header = ctk.CTkLabel(self, text="WELCOME TO THE DAY".upper(), font=(self.font_ap, 24, "bold"))

        # Date Entry Section
        self.sub_header = ctk.CTkLabel(self, text="ENTER DATE", font=(self.font_ap, 16))
        self.day_entry = ctk.CTkEntry(self, width=50, height=30, placeholder_text=self.today_date,
                                      font=(self.font_ap, 16))
        self.month_entry = ctk.CTkEntry(self, width=120, height=30, placeholder_text=self.today_month,
                                        font=(self.font_ap, 16))
        find_btn = ctk.CTkButton(self, text="FIND", width=50, height=30, fg_color="#00A8FF", hover_color="#0099E6",
                                 text_color="#DCDCDC", command=self.find_data)
        # Positions
        self.header.place(x=120, y=20)
        self.sub_header.place(x=75, y=75)
        self.day_entry.place(x=180, y=75)
        self.month_entry.place(x=240, y=75)
        find_btn.place(x=375, y=75)

        # Entries Frame
        self.container = ctk.CTkFrame(self, width=450, height=410, fg_color=self.container_color_, corner_radius=10,
                                      border_width=1, border_color=self.border_color_)
        self.container.place(x=25, y=125)

        # Total Found
        self.day_counter = ctk.CTkLabel(self, text=f"Total Days Found: {self.data_of_the_day}", font=(self.font_ap, 14),
                                        text_color=self.text_color_)
        self.day_counter.place(x=185, y=550)

        # Icon + Buttons
        buttons = zip([self.theme_icon, "left_btn.png", "right_btn.png"], [440, 35, 425], [15, 565, 565], [30, 25, 25],
                      [self.change_theme, self.left_btn, self.right_btn])
        for button in buttons:
            self.add_icon_button(button[0], button[1], button[2], button[3], button[4])

        self.page_label = ctk.CTkLabel(self, text=f"Page {self.clicked + 1} of {self.clicks_pos}", text_color="#555",
                                       font=(self.font_ap, 12))
        self.page_label.place(x=220, y=580)

    def add_entry(self, parent, profile: str = None, text: str = "", y: int = 0):
        # Entry frame
        frame = ctk.CTkFrame(parent, width=420, height=70, corner_radius=15, fg_color=self.frame_color_)
        frame.place(x=15, y=y)

        # Profile on Image
        img_path = os.path.join("Images", "Days Image", self.today_month.lower(), self.today_date)
        try:
            pro = Image.open(os.path.join(img_path, profile)).resize((75, 75))
            pro_ctk = ctk.CTkImage(light_image=pro, size=(75, 75))
            ctk.CTkLabel(frame, image=pro_ctk, text="").place(x=0, y=0)
        except Exception as e:
            print("Image missing:", e)

        # Text
        ctk.CTkLabel(frame, text=text, font=("Aptos", 18), anchor="w", text_color=self.text_color_, width=250 * -1,
                     wraplength=300, justify="left").place(x=100, y=10)

        # Read More button
        read_more_img = ctk.CTkImage(Image.open(combine("read_more.png")), size=(50, 10))
        ctk.CTkButton(frame, image=read_more_img, text="", width=50, height=10, fg_color="transparent",
                      hover_color="#f0f0f0").place(x=350, y=50)

    def right_btn(self):
        if self.clicks_pos == 0: return
        self.clicked = (self.clicked + 1) % self.clicks_pos
        self.by_the_loop(self.processed_data[self.clicked])
        self.page_label.configure(text=f"Page {self.clicked + 1} of {self.clicks_pos}")

    def left_btn(self):
        if self.clicks_pos == 0: return
        self.clicked = (self.clicked - 1 + self.clicks_pos) % self.clicks_pos
        self.by_the_loop(self.processed_data[self.clicked])
        self.page_label.configure(text=f"Page {self.clicked + 1} of {self.clicks_pos}")

    def by_the_loop(self, data):
        for widget in self.container.winfo_children():
            widget.destroy()

        for pos, name in data:
            self.add_entry(self.container, name, os.path.splitext(name)[0].capitalize(), pos)

    def add_icon_button(self, img_name, x, y, size, command=None):
        img = ctk.CTkImage(Image.open(combine(img_name)), size=(size, size))
        (ctk.CTkButton(self, image=img, text="", command=command, width=size, height=size, fg_color="transparent").place
            (x=x, y=y))

    def clean_screen(self):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()


if __name__ == "__main__":
    app = LightModeApp()
    app.background_process()
    app.screen_()
    app.change_theme()
    app.right_btn()
    app.mainloop()
