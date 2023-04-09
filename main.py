import pickle
import tkinter as tk
from autocomplete import predict

def bifurcate(arr):
    split = int(len(arr) / 2)
    return arr[0:split], arr[split:]

root = tk.Tk()
root.maxsize(600,600)

left_initial = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l','m']
right_initial = ['n','o','p','q','r','s','t','u','v','w','x','y','z']

left_current = left_initial
right_current = right_initial
output_current: [str] = [] # gonna keep this as a character array to allow for pushing

# load autocomplete nonsense
nstubtree = None
with open('./autocomplete.pkl', 'rb') as f:
    nstubtree = pickle.load(f)
print(nstubtree)
def display_output():
    global output_current
    typing_area.config(text = ''.join(output_current))

    global nstubtree
    # global auto_complete_suggestion
    # attempt an autocomplete
    autocompleted = predict(typing_area.cget('text'),nstubtree,0.5)
    print(f"Autocompleted: {autocompleted}?")
    if len(autocompleted) > 1:
        typing_area.config(text=''.join(autocompleted))


def do_click(event):
    global left_current
    global right_current
    global output_current
    char_canvas.delete('all')
    char_canvas.create_line(150, 0, 150, 150)

    # first check if that's the only option left
    if event.x < 150 and len(left_current) <= 1:
        print(f"selected {left_current[0]}")
        output_current.append(left_current[0])
        display_output()
        left_current = left_initial
        right_current = right_initial
    elif event.x > 150 and len(right_current) <= 1:
        output_current.append(right_current[0])
        display_output()
        left_current = left_initial
        right_current = right_initial
        print(f"selected {right_current[0]}")
    else:
        left, right = bifurcate(left_current if event.x < 150 else right_current)
        print(left)
        print(right)

        # and set the global vars to match
        left_current = left
        right_current = right
    char_canvas.create_text(75, 75, text=f'{left_current[0]}-{left_current[-1]}')
    char_canvas.create_text(225, 75, text=f'{right_current[0]}-{right_current[-1]}')

main_frame = tk.Frame(root, width=300, height=300)

# so first thing to do is to have the typing area and then two canvas sections
# need a canvas because we'll need to control
text_frame = tk.Frame(main_frame, width=300,height=50).grid(row=0,column=0)
typing_area = tk.Label(text_frame, text="Word Select 3000")
typing_area.pack()
# typing_area.configure(state='disabled')

char_canvas = tk.Canvas(main_frame, bg="white", height=150, width=300)
# char_canvas.create_rectangle(0, 0, 50, 50)
char_canvas.create_line(150,0,150,150)
char_canvas.create_text(75,75,text=f'{left_current[0]}-{left_current[-1]}')
char_canvas.create_text(225,75,text=f'{right_current[0]}-{right_current[-1]}')
char_canvas.grid(row=1,column=0)
char_canvas.bind('<Button-1>', do_click)

# ws_canvas = tk.Canvas(main_frame, bg="white", height=150, width=300)
# ws_canvas.create_rectangle(0, 0, 50, 50)
# ws_canvas.create_line(150,0,150,150)
# ws_canvas.grid(row=2,column=0)

auto_complete_suggestion = tk.Label(main_frame, text="Autocomplete: ").grid(row=2, column=0)

# canvas.pack()
main_frame.pack()
main_frame.mainloop()