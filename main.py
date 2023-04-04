import tkinter as tk

root = tk.Tk()
root.maxsize(600,600)

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
char_canvas.grid(row=1,column=0)

ws_canvas = tk.Canvas(main_frame, bg="white", height=150, width=300)
ws_canvas.create_rectangle(0, 0, 50, 50)
ws_canvas.create_line(150,0,150,150)
ws_canvas.grid(row=2,column=0)

# canvas.pack()
main_frame.pack()
main_frame.mainloop()