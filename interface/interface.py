from tkinter import *

def main():
    def start_paint(event):
        global last_x, last_y
        last_x, last_y = event.x-1, event.y-1

    def paint(event):
        # global last_x, last_y
        color = 'red'
        last_x, last_y = event.x-1, event.y-1
        canvas.create_oval(last_x, last_y, event.x, event.y, fill=color,width=2, tags="line")
        last_x, last_y = event.x, event.y
        print(f"Drawing at: x={event.x}, y={event.y}")

    def count_lines():
        # Count all line objects on the canvas
        line_count = len(canvas.find_withtag("line"))
        print(f"Total lines drawn: {line_count}")

    root = Tk()
    root.title("Drawing App")

    last_x, last_y = None, None  # Initialize the last known positions to None

    canvas = Canvas(root, width=800, height=600, bg='grey')

    canvas.pack(expand=YES, fill=BOTH)
    # canvas.bind("<Button-1>", start_paint)  # Set start points on mouse click
    canvas.bind("<B1-Motion>", paint)       # Draw lines as mouse moves with button pressed

    message = Label(root, text="Drag the mouse to draw")
    message.pack(side=BOTTOM)

    # Button to count lines on the canvas
    count_button = Button(root, text="Count Lines", command=count_lines)
    count_button.pack(side=BOTTOM)

    root.mainloop()

if __name__ == "__main__":
    main()
