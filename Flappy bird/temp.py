from tkinter import *
import random
import  time
is_game_over = False
end_game_bg = None
end_game_score = None
ms = 20
score = 0
level = 1
plus = 1
window = Tk()
window.title('Flappy bird')
cw, ch = 540, 960
canvas = Canvas(window, width = cw, height = ch, bg = '#43f0bf', highlightthickness = 0)
canvas.pack()
d = 200
pipeup= canvas.create_rectangle(cw - 100, 0, cw, 350, fill = '#3734eb', outline = '#3734eb')
pipedown = canvas.create_rectangle(cw - 100, 600, cw, ch, fill = '#3734eb', outline = '#3734eb')
text = canvas.create_text(15,60,fill="white",font="Impact 60",text=str(score), anchor=W)
lv_text = canvas.create_text(400,60,fill="white",font="Impact 60",text="Lv. " + str(level), anchor=W)
bird_img = PhotoImage(file ='C:/Users/ADMIN/Desktop/bird.png')
bird = canvas.create_image(100, ch // 2, image = bird_img)

gravity = 0
acer = 0.5
def bird_fall():
    global gravity, acer, is_game_over
    if is_game_over:
        return
    x1, y1 = canvas.coords(bird)
    y1 += gravity
    gravity += acer
    if y1 > ch:
        game_over()
    canvas.coords(bird, x1, y1)
    window.after(20, bird_fall)
up_count = 0
def bird_up(evt=None):
    global up_count, gravity, is_game_over
    if is_game_over:
        restart_game()
        return
    x1, y1 = canvas.coords(bird)
    gravity = 0
    y1 -= 25 - up_count * 5
    if up_count < 5:
        up_count += 1
        window.after(20, bird_up)
    else:
        up_count = 0
    canvas.coords(bird, x1, y1)
def move_pile():
    global  plus, is_game_over, score, ms, level
    if is_game_over:
        return
    x1, y1 , x2, y2 = canvas.coords(pipeup)
    x1 -= 5
    if x1 < -100:
        x1 = cw
        y2 = random.randint(100, ch - 350)
        plus = 0
    canvas.coords(pipeup, x1, 0, x1 + 100, y2)
    canvas.coords(pipedown, x1, y2 + 250, x1 + 100, ch)
    check_col()
    window.after(int(ms), move_pile)
def check_col():
    global score, plus, is_game_over, ms, level
    if is_game_over:
        return
    bird_w = 100
    bird_h = 70
    x, y = canvas.coords(bird)
    xp, yp, xp2, yp2 = canvas.coords(pipeup)
    if x < xp2 and x + bird_w > xp + 50 and (y + bird_h > yp2 + 250 or y < yp2):
        game_over()
    elif y > yp2:
        if plus == 0:
            score += 1
            if score != 0 and score % 10 == 0:
                level += 1
                ms *= 0.9
            plus = 1
            canvas.itemconfig(text, text=str(score))
            canvas.itemconfig(lv_text, text="Lv. " + str(level))
move_pile()
bird_fall()
def game_over():
    global is_game_over, end_game_bg, end_game_score
    is_game_over = True
    end_game_bg = canvas.create_rectangle(0, 0, cw, ch, fill = "#4EC0CA", outline = "white")
    end_game_score = canvas.create_text(15,200,fill="#ffffff",font="Impact 60",text="Your score is: " + str(score), anchor=W)
def restart_game():
    global is_game_over, end_game_bg, end_game_score, score, gravity, level, ms
    canvas.delete(end_game_bg)
    canvas.delete(end_game_score)
    score = 0
    canvas.itemconfig(text, text=str(score))
    level = 1
    canvas.itemconfig(lv_text, text="Lv. " + str(level))
    ms = 20
    canvas.coords(bird, 100, ch // 2)
    canvas.coords(pipeup, cw - 100, 0, cw, 350)
    canvas.coords(pipedown, cw - 100, 600, cw, ch)
    is_game_over = False
    gravity = 0
    move_pile()
    bird_fall()
window.bind('<space>', bird_up)
window.mainloop()