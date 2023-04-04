import tkinter as tk

def bifurcate(arr):
    split = int(len(arr) / 2)
    return arr[0:split], arr[split:]

root = tk.Tk()
root.maxsize(600,600)

left_current = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l','m']
right_current = ['n','o','p','q','r','s','t','u','v','w','x','y','z']

def do_click(event):
    global left_current
    global right_current
    char_canvas.delete('all')
    char_canvas.create_line(150, 0, 150, 150)
    left, right = bifurcate(left_current if event.x < 150 else right_current)
    print(left)
    print(right)

    # and set the global vars to match
    left_current = left
    right_current = right
    char_canvas.create_text(75,75,text=f'{left[0]}-{left[-1]}')
    char_canvas.create_text(225,75,text=f'{right[0]}-{right[-1]}')

main_frame = tk.Frame(root, width=300, height=300)

# so first thing to do is to have the typing area and then two canvas sections
# need a canvas because we'll need to control
text_frame = tk.Frame(main_frame, width=300,height=50).grid(row=0,column=0)
typing_area = tk.Label(text_frame, text="Yuh yuh")
typing_area.pack()
# typing_area.configure(state='disabled')

char_canvas = tk.Canvas(main_frame, bg="white", height=150, width=300)
char_canvas.create_rectangle(0, 0, 50, 50)
char_canvas.create_line(150,0,150,150)
char_canvas.create_text(75,75,text=f'{left_current[0]}-{left_current[-1]}')
char_canvas.create_text(225,75,text=f'{right_current[0]}-{right_current[-1]}')
char_canvas.grid(row=1,column=0)
char_canvas.bind('<Button-1>', do_click)

ws_canvas = tk.Canvas(main_frame, bg="white", height=150, width=300)
ws_canvas.create_rectangle(0, 0, 50, 50)
ws_canvas.create_line(150,0,150,150)
ws_canvas.grid(row=2,column=0)

# canvas.pack()
main_frame.pack()
main_frame.mainloop()