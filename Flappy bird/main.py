from tkinter import *
import random

# Setup variables
c_width = 400
c_height = 760
c_bg = "#3ea9f0"
speed_default = 10
speed_bonus = 0.5
rate_time = 20
up_count = 0
position_x = 50
pipe_color = "#06d417"
pipe_hole_height = 300
pipe_hole_width = 100
is_running = False
score = 0
bg_score = alert_score = None
level = 1
rate_level = 3
lb_score = None
# Setup tk
tk = Tk()
tk.title("Flappy bird")
tk.geometry("%dx%d" % (c_width, c_height))

w = Canvas(tk, width=c_width, height=c_height, bg=c_bg)
w.pack()

# Background of game
backgroundImage = PhotoImage(file="background.png")
w.create_image(0, 0, image=backgroundImage,
               anchor="nw")

# pipe
pipe_up = w.create_rectangle(
    c_width - 100, 0, c_width, 300, fill=pipe_color, outline=pipe_color)

pipe_down = w.create_rectangle(
    c_width - 100, 300 + pipe_hole_height, c_width, c_height, fill=pipe_color, outline=pipe_color)

# bird
birdImage = PhotoImage(file="bird.png")
bird = w.create_image(position_x, c_height // 2, image=birdImage)


# Srore
lb_score = w.create_text(20, 40, text="SCORE: 0",
                         fill="white", anchor=W, font="Impact 20")

# Level
lb_level = w.create_text(c_width - 100, 40, text="LEVEL: 1",
                         fill="white", anchor=W, font="Impact 20")


def cta_over():
    global score, is_running, bg_score, alert_score
    is_running = False
    bg_score = w.create_rectangle(
        0, 0, c_width, c_height, fill=c_bg, outline=c_bg)
    alert_score = w.create_text(40, 100, text="YOUR SCORE: %s" % score,
                                fill="white", anchor=W, font="Impact 40")


def cta_move_pipe():
    global pipe_hole_width, c_width, score, is_running, level, rate_level, rate_time
    if is_running:
        xb, yb = w.coords(bird)
        x1, y1, x2, y2 = w.coords(pipe_up)
        x1 -= 5

        if x1 < -100:
            x1 = c_width
            y2 = random.randint(100, c_height - pipe_hole_height - 100)
            score += 1
            w.itemconfigure(lb_score, text="SCORE: " + str(score))
            if score % rate_level == 0:
                level += 1
                w.itemconfigure(lb_level, text="LEVEL: " + str(level))
                rate_time += 5
                print("rate_time: " + str(rate_time))

        w.coords(pipe_up, x1, y1, x1 + pipe_hole_width, y2)
        w.coords(pipe_down, x1, y2 + pipe_hole_height,
                 x1 + pipe_hole_width, c_height)

        # Width image is 50, height is 37
        if (xb + 50 > x1 and xb < x2 and (yb < y2 or yb + 37 > y2 + pipe_hole_height)):
            cta_over()

    tk.after(rate_time, cta_move_pipe)


def cta_restart():
    global speed_default, is_running, score, c_width, c_height, pipe_hole_height, pipe_color
    w.coords(bird, position_x, 0)
    speed_default = 10
    score = 0
    is_running = True
    if bg_score:
        w.delete(bg_score)
    if alert_score:
        w.delete(alert_score)

    w.coords(pipe_up, c_width - 100, 0, c_width, 300)
    w.coords(pipe_down, c_width - 100, 300 + pipe_hole_height,
             c_width, c_height)


def cta_down():
    global rate_time
    global speed_bonus, speed_default, is_running
    if is_running:
        x, y = w.coords(bird)

        y += speed_default
        speed_default += speed_bonus
        w.coords(bird, x, y)

        if(y > c_height):
            cta_over()

    tk.after(rate_time, cta_down)


def cta_up(e=None):
    global speed_default, up_count, is_running
    if is_running:
        x, y = w.coords(bird)
        speed_default = 10
        y -= 20

        if(up_count < 5):
            up_count += 1
            tk.after(rate_time, cta_up)
        else:
            up_count = 0

        if x < 0:
            cta_over()

        w.coords(bird, x, y)
    else:
        cta_restart()


tk.after(rate_time, cta_down)
tk.after(rate_time, cta_move_pipe)
tk.bind("<space>", cta_up)
tk.bind("<Button-1>", cta_up)
tk.mainloop()
