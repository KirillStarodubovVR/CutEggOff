import customtkinter
import os
from PIL import Image
from ruaccent import RUAccent


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ОтрубИ")
        self.geometry("700x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="Главное меню",
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Обработка строк",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Обработка документа",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_2_button_event,
        )
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_label = customtkinter.CTkLabel(
            self.home_frame, text="Преобразование текста"
        )
        self.home_frame_label.grid(row=0, column=0, padx=20, pady=0)

        # text box form income text
        self.home_text_in = customtkinter.CTkTextbox(
            self.home_frame,
            width=420,
            height=100,
            corner_radius=0,
            wrap="word",
        )
        self.home_text_in.grid(row=1, column=0, padx=10, pady=0)
        self.home_text_in.insert("0.0", "Текст для преобразования")

        # process button
        self.home_frame_button_process = customtkinter.CTkButton(
            self.home_frame,
            text="Process",
            compound="right",
            command=self.button_process_event,
        )
        self.home_frame_button_process.grid(row=2, column=0, padx=10, pady=0)

        # label and textbox for result out
        self.home_out_label = customtkinter.CTkLabel(self.home_frame, text="Ударения")
        self.home_out_label.grid(row=3, column=0, padx=0, pady=0)

        self.home_text_out = customtkinter.CTkTextbox(
            self.home_frame,
            width=420,
            height=100,
            corner_radius=0,
            wrap="word",
        )
        self.home_text_out.grid(row=4, column=0, padx=0, pady=0)
        self.home_text_out.insert("0.0", "Ударения")

        # label and textbox for omographs
        self.home_omo_label = customtkinter.CTkLabel(self.home_frame, text="Омографы")
        self.home_omo_label.grid(row=5, column=0, padx=0, pady=0)

        self.home_text_omo = customtkinter.CTkTextbox(
            self.home_frame,
            width=420,
            height=100,
            corner_radius=0,
            wrap="word",
        )
        self.home_text_omo.grid(row=6, column=0, padx=0, pady=0)
        self.home_text_omo.insert("0.0", "Омографы")

        # label and textbox for unknown words
        self.home_none_label = customtkinter.CTkLabel(
            self.home_frame, text="Неизвестные слова"
        )
        self.home_none_label.grid(row=7, column=0, padx=0, pady=0)

        self.home_text_none = customtkinter.CTkTextbox(
            self.home_frame,
            width=420,
            height=100,
            corner_radius=0,
            wrap="word",
        )
        self.home_text_none.grid(row=8, column=0, padx=0, pady=0)
        self.home_text_none.insert("0.0", "Неизвестные слова")

        # create second frame
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def get_accents(self, text):
        ru_accent = RUAccent()
        ru_accent.load()
        return ru_accent.process_all(text=text)

    def button_process_event(self):
        out_text = self.get_accents(self.home_text_in.get("0.0", "end-1c"))[0]
        omo_text = self.get_accents(self.home_text_in.get("0.0", "end-1c"))[1]
        none_text = self.get_accents(self.home_text_in.get("0.0", "end-1c"))[2]

        self.home_text_out.delete("0.0", "end-1c")
        self.home_text_omo.delete("0.0", "end-1c")
        self.home_text_none.delete("0.0", "end-1c")

        self.home_text_out.insert("0.0", f"{out_text}")
        self.home_text_omo.insert("0.0", f"{omo_text}")
        self.home_text_none.insert("0.0", f"{none_text}")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
