from tkinter import *
from chat import get_response, bot_name, speak
import Constants.colors as colors
from gtts import gTTS
import playsound
import os


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def speak(sentence):
        tts = gTTS(text=sentence, lang='bn')
        tts.save('bangla_bot_speak.mp3')
        playsound.playsound('bangla_bot_speak.mp3', True)
        os.remove('bangla_bot_speak.mp3')

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=colors.BG_COLOR)

        # head label
        head_label = Label(self.window, bg=colors.BG_COLOR, fg=colors.TEXT_COLOR, text="Welcome", font=colors.FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=colors.BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # test widget
        self.text_widget = Text(self.window, width=50, height=2, bg=colors.BG_COLOR, fg="#00FF00", font=colors.FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=colors.BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=colors.TEXT_COLOR, font=colors.FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=colors.FONT_BOLD, width=20, bg=colors.BG_GRAY, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "আমি")
        self._speak_the_sentence(msg)

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    def _speak_the_sentence(self, msg):
        only_response = f"{get_response(msg)}"
        speak(only_response)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()