import tkinter

#### CONSTANTS
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT = ("Courier", 25, "bold")
FONT_SMALL = ("Courier", 15, "bold")
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 224
IMAGE_PATH = "tomato.png"
reps = 0
timer = None

#### TIMER RESET
def timer_reset():
    start_button.config(state="normal")
    reset_button.config(state="disabled")

    window.after_cancel(timer)
    headline.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    tracker.config(text="")
    global reps
    reps = 0


#### TIMER MECHANISM
def front():
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)

def start_timer():
    start_button.config(state="disabled")
    reset_button.config(state="normal")

    global reps
    reps += 1
    if reps % 8 == 0:
        front()
        count_down(LONG_BREAK_MIN * 60)
        headline.config(text="Break", fg=RED)
    elif reps % 2 == 1:
        front()
        count_down(WORK_MIN * 60)
        headline.config(text="Work", fg=GREEN)
    else:
        front()
        count_down(SHORT_BREAK_MIN * 60)
        headline.config(text="Break", fg=PINK)

#### COUNTDOWN MECHANISM
def count_down(count):
    minutes = int(count / 60)
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02}:{seconds:02}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        # add a check mark
        checkmark_counter = int(reps/2) * u"\u2713"
        tracker.config(text=checkmark_counter)


# UI SETUP
window = tkinter.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# headline
headline = tkinter.Label(text="Timer", fg=GREEN, bg=YELLOW, font=FONT)
headline.grid(column=1, row=0)

# tomato background image
canvas = tkinter.Canvas(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=YELLOW, highlightthickness=0)
background_img = tkinter.PhotoImage(file=IMAGE_PATH)
canvas.create_image(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, image=background_img)
timer_text = canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.75, text="00:00", fill="white", font=FONT)
canvas.grid(column=1, row=1)

# buttons
start_button = tkinter.Button(text="Start", command=start_timer, highlightthickness=0, state="normal")
start_button.grid(column=0, row=3)

reset_button = tkinter.Button(text="Reset", command=timer_reset, highlightthickness=0, state="disabled")
reset_button.grid(column=2, row=3)

# keep track
tracker = tkinter.Label(fg=GREEN, bg=YELLOW, font=FONT_SMALL)
tracker.grid(column=1, row=4)


window.mainloop()

