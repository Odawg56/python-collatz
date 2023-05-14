# python-collatz
Tool to render interpretations of the Collatz Conjecture using Python Turtle.

# Explaination of the Conjecture {#explaination}

To understand how the program works, you must first know *what* the Collatz Conjecture is. If you don't want to read, Veritasium has a great video here: https://youtu.be/094y1Z2wpJg

For starters, the conjecture is a rule that - when applied continuously to any positive integer - the number will come to equal 1, then loop. The rules are as follows:

- If the number is even, divide by two (making it odd).
- If the number is odd, multiply my three and add one (making it even again)

If the conjecture were to be applied to say, 6, the pattern would be as follows: 6,3,10,5,16,8,4,2,1,4,2,1,4,2,1...
You will note that it ends up in the loop, 4,2,1,4,2,1. In the collatz python file, `collatz.py`, this rule is applied in a function `applyRule`.

# Prerequisites {#prerequisites}

The applications uses both Kivy and PIL, which are not shipped with python. Instructions for installing kivy can be found at https://kivy.org/doc/stable/gettingstarted/installation.html, and PIL can be installed using pip: 
```pip install Pillow```

Other than that, Python will obviously need to be installed as well, which can be done through the Windows Store or terminal.

**Note: There is no formal support for any OS other than Windows at this time, but you are welcome to try**

# Functions of the app {#functions}

As discussed in [Explaination of the Conjecture](#explaination), any positive integer will come to equal one after the rule is applied. The main loop of the app tests values in a specified range (default 1-200), and plots them using Python Turtle. This is achieved by applying the rule to the current number, and turning a set amount left or right based on if the result is even or odd. The turtle will then move forward and repeat this process until reaching 1. Once the 'strand' has reached 1, the turtle goes back to the starting position and draws the next value in a strand.

##Colour Calculation

If you've seen the app work, you'll note that there is a spectrum of colours that render in the strands, composed of RGB values. Currently, Red increases and Blue decreases through values tested, and Green increases along the length of a strand, with the maximum value in the whole application having the maximum green value of 255. The maximum value is hence needed prior to rendering the strands, so it is calculated beforehand in a function `calcMaxGreen`.
