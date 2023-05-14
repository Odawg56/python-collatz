#Collatz Conjecture Script v1.6
#By Oliver Box
#last updated 17/03/22
from turtle import *
from turtle import RawTurtle

from PIL import ImageGrab
import tkinter as tk

#initialise preset system variables
class preset:
  def __init__(self, n, e, o, d, xs, ys, pns):
    self.idName = n
    self.eA = e
    self.oA = o
    self.dist = d
    self.xStart = xs
    self.yStart = ys
    self.pSZ= pns

def applyRule(num):
    even = True
    if ((num % 2) == 0): #even
        num = num / 2
    elif num == 0:
        pass
    else: #odd
        num = 3 * num +1
        even = False
    return num, even

#figure out max green value:
def calcMaxGreen(i,maxIterations,num):
    while (i < maxIterations):
        while num != 1:
            num = applyRule(num)[0]
            #print(num, text)
            count += 1
        if count > maxcount:
            maxcount = count
        count = 0
        num = i
        i += 1
    #set variable for max green value in graphical section
    print("Preliminary calculations finished with max value of", maxcount)
    print(256/maxcount, "is multiplied by the steps to get the green value")
    return maxcount

def takePic(FN):
    x0 = root.winfo_rootx()
    y0 = root.winfo_rooty()
    x1 = x0 + root.winfo_width()
    y1 = y0 + root.winfo_height()
    ImageGrab.grab(bbox=(x0, y0, x1, y1)).save((FN+".png"))

#preset matrix / bank >> assign different presets numerical values
#               NAME   EVEN    ODD    DISTANCE    XSTART  YSTART    MAX_PENSIZE
preset1 = preset("Coral1", 8, -20, 8, 0, 20, 20)
preset2 = preset("Curly_Feather", -6, 4, 8, 0, 20, 20)
preset3 = preset("Eaglefish", -10, 20, 7, 100, 50, 20)
preset4 = preset("evenSteven", -5, 5, 6, -50, -150, 20)
preset5 = preset("hexagons", -60, 30, 20, 0, 0, 20)
preset6 = preset("squares", -90, 45, 20, 0, 0, 20)
preset7 = preset("penta", -72, 36, 18, 0, 0, 20)

presets = [preset1, preset2, preset3, preset4, preset5, preset6, preset7]
#song number is 77176736535666765675335353771765767335444765376567562322276772333276567562322276771275345545766564543422334554576665646577176736535666765676335353771765767335444765

#display presets in a nice manner
print("Current available presets:")
print("Order of information is index, name, odd angle, even angle, distance per step and starting pensize")
i2 = 0
i22 = 0
#print(i2)
for i2 in presets:
    spaces = " "*int((20-len(str(i2.idName))))
    info = str((str(i22)+" | "+ str(i2.idName)+" ::"+spaces+str(i2.oA)+" "+str(i2.eA)+" "+ str(i2.dist)+" "+ str(i2.pSZ)))
    print(info)
    i22 += 1

#get preset selection and i range from use
ps_select = int(input("Preset Selection (# to chose is in the left column): "))
startingNum = -1
while (int(startingNum) < 1):
    startingNum = int(input("Number to start with (default is 1): "))
maxIterations = int(input("What iteration to stop at (will start at " + str(startingNum) + ")? "))
print("P0 is default, P1 increases, P2 decreases towards you, and P3 is large pensize")
persp1 = int(input("Realistic perspective (0/1/2/3)? "))
bgCol = input("BG Colour? ")
penSize1 = presets[ps_select].pSZ


#calculate coefficient to use for the green value becuase green increases along with no. of steps
print("generating from", startingNum, "to", str(maxIterations)+ ", for a total of", str(maxIterations-startingNum), "iterations" )

#turtle setup
root = tk.Tk()
canvas = tk.Canvas(root, width=1280, height=720, background='black')
canvas.pack()
t = RawTurtle(canvas)

#turtle.screensize(canvwidth=None, canvheight=None, bg=None)

t.speed(0)
if persp1 == 0 or persp1 == 1:
    t.pensize(1)
elif persp1 == 2 or persp1 == 3:
    t.pensize(penSize1)
t.pu()
t.goto(presets[ps_select].xStart,presets[ps_select].yStart)
t.pd()
t.seth(90)
#t.colormode(255)
if bgCol.lower() == 'black':
    canvas.configure(bg='black')
ht()

count = 0
maxcount = 0
i = startingNum
num = i

maxsteps = calcMaxGreen(i,maxIterations,num)

#visual loop::
culminative1 = "t"
count = 0
maxcount = 0
i = startingNum
num = i +1
while (i < maxIterations): #triggers every different value tested
    while num != 1: #triggers every segment
        res = applyRule(num)[0]
        num = res[0]
        even = res[1]
        if even: #change angles according to preset
            t.seth(t.heading()+presets[ps_select].eA)
        else:
            t.seth(t.heading()+presets[ps_select].oA)
        #colouring system: red increases and blue decreases as different numbers are tested, green increases along with the number of steps
        #ie. long tips will be more green.
        if ((count % 2) == 0): #every second segment
            t.color((1/maxIterations)*i,count*(1/maxsteps),1-(1/maxIterations)*i)
        t.fd(presets[ps_select].dist) #move forward
        count += 1
    t.pu()
    t.goto(presets[ps_select].xStart,presets[ps_select].yStart)
    t.seth(90)
    t.pd()
    if persp1 == 1:
        #pensize increases to have some form of 3d view
        t.pensize(((i - startingNum)/(maxIterations - startingNum)) * penSize1)
    elif persp1 == 2:
        #pensize decreases to have a different effect (i hope)
        t.pensize((1 - ((i - startingNum)/(maxIterations - startingNum))) * penSize1)
    if count > maxcount: #adapted basic highscore system
        maxcount = count
        maxNum = i
    if i % 10 == 0: #print status reports every 10 values tested
        print("maxcount is", maxcount, "at", maxNum)
        print(round((((i - startingNum)/(maxIterations - startingNum))*100), 2), "percent complete at", i)
    count = 0
    num = i
    i += 1

print("maximum steps for values", startingNum, "to", maxIterations, "is", maxcount)

#get file name
FN = "collatz_"+presets[ps_select].idName+"_"+ str(startingNum)+"to"+str(maxIterations)+"i_"+str(presets[ps_select].oA)+"o_"+str(presets[ps_select].eA)+"e_"+str(presets[ps_select].dist)+"d_persp"+str(persp1)
if bgCol != '':
    FN += ("_"+bgCol.lower())
print("filename should be:", FN)

root.mainloop()
takePic(FN)
t.exitonclick()