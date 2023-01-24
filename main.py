import tkinter
from tkinter import ttk
import customtkinter
import os
from PIL import Image
import random
import time

IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./images/UI")


class GameCard:
    def __init__(self, master, text, image, command, width, height, card_id, value):
        self.id = card_id
        self.value = value
        self.button = customtkinter.CTkButton(
            master=master, text=text, image=image, command=command, width=width, height=height
        )


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("image_example.py")
        self.geometry("1200x800")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = IMAGE_PATH
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26)
        )
        self.large_test_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150)
        )
        self.image_icon_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20)
        )
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20),
        )
        self.chat_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
            size=(20, 20),
        )
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
            size=(20, 20),
        )

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="Memory Game",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.settings_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Settings",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image,
            anchor="w",
            command=self.settings_button_event,
        )
        self.settings_button.grid(row=2, column=0, sticky="ew")

        self.game_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Play",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.chat_image,
            anchor="w",
            command=self.game_button_event,
        )
        self.game_button.grid(row=1, column=0, sticky="ew")

        # create game frame
        self.game_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.misses = tkinter.IntVar(self.game_frame, 0)

        # create settings frame
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # populate game frame
        self.game_card_values = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
        self.game_cards = {}
        for i in range(10):
            val = random.choice(self.game_card_values)
            self.game_card_values.remove(val)
            gc = GameCard(
                master=self.game_frame,
                text="",
                image=self.image_icon_image,
                command=lambda i=i, val=val: self.click_game_card(i, val),
                width=130,
                height=200,
                card_id=i,
                value=val,
            )
            self.game_cards[i] = gc

        for j in self.game_cards.values():
            row = 2
            col = int(j.id / 2)
            if (j.id + 1) % 2 == 0:
                row = 4
                col = int(j.id / 2)
            j.button.grid(row=row, column=col, padx=20, pady=10)

        self.instructions = customtkinter.CTkLabel(master=self.game_frame, text="Match two cards!")
        self.instructions.place(relx=0.1, rely=0.6)

        self.misses_label = ttk.Label(self.game_frame, text="Misses: 0")
        self.misses_label.place(relx=0.1, rely=0.9)

        self.selection_label = ttk.Label(master=self.game_frame, text="Selected Value: ")
        self.selection_label.place(relx=0.4, rely=0.9)
        self.first_selection = None
        self.second_selection = None

        # select default frame
        self.select_frame_by_name("game")

    def click_game_card(self, button, value=0):
        print(f"=== click event on button {button}")
        self.instructions.configure(text=f"You selected {button}")
        print(f"first: {self.first_selection}")
        print(f"second: {self.second_selection}")
        print("setting local game_card_obj")
        game_card_obj = self.game_cards[button]
        game_card_obj.button.configure(image=self.add_user_image)
        if not self.first_selection and not self.second_selection:
            # empty selections
            print("setting first selection")
            self.first_selection = game_card_obj
            self.selection_label.configure(text=f"Selected First Value: {str(game_card_obj.value)}")
        elif self.first_selection and not self.second_selection:
            print("setting second selection")
            self.second_selection = game_card_obj

        print(f"first: {self.first_selection}")
        print(f"second: {self.second_selection}")
        if self.first_selection and self.second_selection:
            print(f"first value: {self.first_selection.value}")
            print(f"second value: {self.second_selection.value}")
            time.sleep(2)
            if self.first_selection.value == self.second_selection.value:
                self.selection_label.configure(text="MATCH!")
            else:
                self.selection_label.configure(text="Miss. Try Again.")
                self.misses_label.configure(text=f"Misses: {self.misses.get() + 1}")
                self.flip_cards_face_down()
            self.first_selection = None
            self.second_selection = None

    def flip_cards_face_down(self):
        self.first_selection.button.configure(image=self.image_icon_image)
        self.second_selection.button.configure(image=self.image_icon_image)

    def get_first_selection_value(self):
        if self.first_selection.get():
            return self.first_selection.get()
        return "-"

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.game_button.configure(fg_color=("gray75", "gray25") if name == "game" else "transparent")

        # show selected frame
        if name == "home":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
        if name == "game":
            self.game_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.game_frame.grid_forget()

    def settings_button_event(self):
        self.select_frame_by_name("home")

    def game_button_event(self):
        self.select_frame_by_name("game")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
