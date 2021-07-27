# Flash card program

import tkinter as tk
import pandas as pd
from random import choice

WORDS_TO_LEARN = "data/words_to_learn.csv"

##### check if there is a words to learn file
try:
    data = pd.read_csv(WORDS_TO_LEARN)
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    data.to_csv(WORDS_TO_LEARN, index=False)
finally:
    word_list = data.to_dict(orient="records")
    current_card = {}

def random_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(word_list)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, func=card_flip)


def known_word():
    word_list.remove(current_card)
    data = pd.DataFrame.from_dict(word_list)
    data.to_csv(WORDS_TO_LEARN, index=False)
    random_word()


def unknown_word():
    random_word()


#### flip card
def card_flip():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_image, image=card_back_img)

##### program layout
BACKGROUND_COLOR = "#B1DDC6"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 526

window = tk.Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=card_flip)

canvas = tk.Canvas(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_back_img = tk.PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, image=card_front_img)
card_title = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/4, text="Title", font=("Ariel", 30, "italic"))
card_word = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, text="word", font=("Ariel", 50, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_img = tk.PhotoImage(file="images/wrong.png")
unknown_button = tk.Button(image=cross_img, highlightthickness=0, command=unknown_word)
unknown_button.grid(row=1, column=0)

check_img = tk.PhotoImage(file="images/right.png")
known_button = tk.Button(image=check_img, highlightthickness=0, command=known_word)
known_button.grid(row=1, column=1)

random_word()

window.mainloop()
