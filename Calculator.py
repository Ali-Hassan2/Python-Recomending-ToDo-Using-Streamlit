from multiprocessing.managers import Value
from tkinter import *

def click(event):
    global valueIn
    text = event.widget.cget("text")
    print(text)

    if text == "=":
        if valueIn.get().isdigit():
            value = int(valueIn.get())
        else:
            value = eval(valueIn.get())
        valueIn.set(value)
        screen.update()
    elif text == "C":
        # pass
        valueIn.set("")
        screen.update()
    else:
        valueIn.set(valueIn.get() + text)
        screen.update()



from tokenize import String

from numpy.ma.core import filled

root = Tk()
root.title("Calculator")
root.geometry("500x500")

# creating a feild for getting the input from the user

# valueIn = IntVar()
# valueIn.set(0)

valueIn = StringVar()
valueIn.set("")

screen = Entry(root, textvariable=valueIn, font="Arial 40 bold")
screen.pack(fill=X, ipadx=10, pady=14, padx=7)

#  SO i have created a input entry
# No i will create 3 frams and each frame will contain the 3 buttons in x-deirection


# frame 1
frame1 = Frame(root,bg="#242424")
btn1 = Button(frame1,text="1",font="Arial 20 bold", padx=30, pady=20)

frame1.pack()
btn1.pack(side=LEFT,padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="2",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="3",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="C",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

# Frame 2

frame1 = Frame(root,bg="#242424")
btn1 = Button(frame1,text="4",font="Arial 20 bold", padx=30, pady=20)

frame1.pack()
btn1.pack(side=LEFT,padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="5",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="6",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="+",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

# Frame 3
frame1 = Frame(root,bg="#242424")
btn1 = Button(frame1,text="7",font="Arial 20 bold", padx=30, pady=20)

frame1.pack()
btn1.pack(side=LEFT,padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="8",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="9",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="*",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

# Frame 4
frame1 = Frame(root,bg="#242424")
btn1 = Button(frame1,text="0",font="Arial 20 bold", padx=30, pady=20)

frame1.pack()
btn1.pack(side=LEFT,padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="00",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="=",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)

btn1 = Button(frame1,text="/",font="Arial 20 bold", padx=30, pady=20)
btn1.pack(side=LEFT, padx=20, pady=10)
btn1.bind("<Button-1>",click)


root.mainloop()

