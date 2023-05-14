# Collatz Conjecture Script v1.6
# By Oliver Box
# last updated 17/03/22
from turtle import *
from turtle import RawTurtle

from PIL import ImageGrab
import tkinter as tk

# initialise preset system variables









# song number is 77176736535666765675335353771765767335444765376567562322276772333276567562322276771275345545766564543422334554576665646577176736535666765676335353771765767335444765
['profile_name', 'even_angle', 'odd_angle', 'stroke_length',
  'x_start', 'y_start', 'pen_size', 'perspective', 'bgColor',
    'additive', 'start_i', 'finish_i']
# get preset selection and i range from use
def drawCollatz(cfg:dict):
    profile_name = cfg['profile_name']
    even_angle = cfg['even_angle']
    odd_angle = cfg['odd_angle']
    stroke_length = cfg['stroke_length']
    x_start = cfg['x_start']
    y_start = cfg['y_start']
    pen_size = cfg['pen_size']
    perspective = cfg['perspective']
    bgColor = cfg['bgColor']
    additive = cfg['additive']
    start_i = cfg['start_i']
    finish_i = cfg['finish_i']

    def takePic(FN):
        x0 = root.winfo_rootx()
        y0 = root.winfo_rooty()
        x1 = x0 + root.winfo_width()
        y1 = y0 + root.winfo_height()
        root.lift()
        ImageGrab.grab(bbox=(x0, y0, x1, y1)).save((FN+".png"))

    # calculate coefficient to use for the green value becuase green increases along with no. of steps
    print("generating from", start_i, "to", str(finish_i) +
        ", for a total of", str(finish_i-start_i), "iterations")

    # turtle setup
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1280, height=720, background='black')
    canvas.pack()
    t = RawTurtle(canvas)

    # turtle.screensize(canvwidth=None, canvheight=None, bg=None)
    "P0 is default, P1 increases, P2 decreases towards you, and P3 is large pensize"
    t.speed(0)
    if perspective == 'Default' or perspective == 'Increasing':
        t.pensize(1)
    elif perspective == 'Decreasing' or perspective == 'Large Pensize':
        t.pensize(pen_size)

    t.pu()
    t.goto(x_start, y_start)
    t.pd()
    t.seth(90)
    # t.colormode(255)
    
    
    canvas.configure(bg=bgColor.lower())
    t.ht()

    count = 0
    maxcount = 0
    i = start_i
    num = i

    maxsteps = calcMaxGreen(i, finish_i, num, count, maxcount)

    # visual loop::
    count = 0
    maxcount = 0
    i = start_i
    num = i + 1
    while (i < finish_i):  # triggers every different value tested
        while num != 1:  # triggers every segment
            res = applyRule(num)
            num = res[0]
            even = res[1]
            if even:  # change angles according to preset
                t.seth(t.heading()+even_angle)
            else:
                t.seth(t.heading()+odd_angle)
            # colouring system: red increases and blue decreases as different numbers are tested, green increases along with the number of steps
            # ie. long tips will be more green.
            if ((count % 2) == 0):  # every second segment
                t.color((1/finish_i)*i, count *
                        (1/maxsteps), 1-(1/finish_i)*i)
            t.fd(stroke_length)  # move forward
            count += 1
        t.pu()
        t.goto(x_start, y_start)
        t.seth(90)
        t.pd()
        if perspective == 1:
            # pensize increases to have some form of 3d view
            t.pensize(((i - start_i)/(finish_i - start_i)) * pen_size)
        elif perspective == 2:
            # pensize decreases to have a different effect (i hope)
            t.pensize(
                (1 - ((i - start_i)/(finish_i - start_i))) * pen_size)
        if count > maxcount:  # adapted basic highscore system
            maxcount = count
            maxNum = i
        if i % 10 == 0:  # print status reports every 10 values tested
            print("maxcount is", maxcount, "at", maxNum)
            print(round((((i - start_i)/(finish_i - start_i))
                * 100), 2), "percent complete at", i)
        count = 0
        num = i
        i += 1

    print("maximum steps for values", start_i,
        "to", finish_i, "is", maxcount)

    # get file name
    FN = "collatz_"+profile_name+"_" + str(start_i)+"to"+str(finish_i)+"i_"+str(
        odd_angle)+"o_"+str(even_angle)+"e_"+str(stroke_length)+"d_persp"+str(perspective)
    if bgColor != '':
        FN += ("_"+bgColor.lower())
    print("filename should be:", FN)

    takePic(FN)
    #t.exitonclick()
    root.mainloop()

# figure out max green value:
def calcMaxGreen(i, finish_i, num, count, maxcount):
    while (i < finish_i):
        while num != 1:
            num = applyRule(num)[0]
            # print(num, text)
            count += 1
        if count > maxcount:
            maxcount = count
        count = 0
        num = i
        i += 1
    # set variable for max green value in graphical section
    print("Preliminary calculations finished with max value of", maxcount)
    print(256/maxcount, "is multiplied by the steps to get the green value")
    return maxcount
def applyRule(num: int) -> int | bool:
    even = True
    if ((num % 2) == 0):  # even
        num = num / 2
    elif num == 0:
        pass
    else:  # odd
        num = 3 * num + 1
        even = False
    return num, even