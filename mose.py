import cv2
import numpy as np

# Initialize variables
drawing = False
mode = 1  # 1-Rectangle, 2-Circle, 3-Freehand, 4-Line
start_x, start_y = -1, -1
canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255  # White canvas
undo_stack = []
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 165, 0), (0, 0, 0)]
color_index = 0

# Helper for mode names
mode_names = {
    1: "Rectangle",
    2: "Circle",
    3: "Freehand",
    4: "Line"
}

# Draw instructions on canvas
def draw_instructions(canvas):
    instructions = f"Mode: {mode_names[mode]} | Color: {colors[color_index]} | [1-4: Modes] [m: Color] [u: Undo] [c: Clear] [s: Save] [Esc: Exit]"
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 30), (240, 240, 240), -1)
    cv2.putText(canvas, instructions, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1, cv2.LINE_AA)

# Mouse callback function
def draw_shape(event, x, y, flags, param):
    global start_x, start_y, drawing, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y
        undo_stack.append(canvas.copy())

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        temp = canvas.copy()
        if mode == 1:  # Rectangle
            cv2.rectangle(temp, (start_x, start_y), (x, y), colors[color_index], 2)
        elif mode == 2:  # Circle
            r = int(((x - start_x) ** 2 + (y - start_y) ** 2) ** 0.5)
            cv2.circle(temp, (start_x, start_y), r, colors[color_index], 2)
        elif mode == 3:  # Freehand
            cv2.line(canvas, (start_x, start_y), (x, y), colors[color_index], 2)
            start_x, start_y = x, y
        elif mode == 4:  # Line
            cv2.line(temp, (start_x, start_y), (x, y), colors[color_index], 2)
        draw_instructions(temp)
        cv2.imshow("Drawing", temp)

    elif event == cv2.EVENT_LBUTTONUP and drawing:
        drawing = False
        if mode == 1:
            cv2.rectangle(canvas, (start_x, start_y), (x, y), colors[color_index], 2)
        elif mode == 2:
            r = int(((x - start_x) ** 2 + (y - start_y) ** 2) ** 0.5)
            cv2.circle(canvas, (start_x, start_y), r, colors[color_index], 2)
        elif mode == 4:
            cv2.line(canvas, (start_x, start_y), (x, y), colors[color_index], 2)
        draw_instructions(canvas)
        cv2.imshow("Drawing", canvas)

    elif event == cv2.EVENT_RBUTTONDOWN:
        canvas[:] = 255
        draw_instructions(canvas)
        cv2.imshow("Drawing", canvas)

# Main function to handle key input
def interactive_draw():
    global mode, canvas, color_index

    draw_instructions(canvas)
    cv2.imshow("Drawing", canvas)
    cv2.setMouseCallback("Drawing", draw_shape)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('1'):
            mode = 1
        elif key == ord('2'):
            mode = 2
        elif key == ord('3'):
            mode = 3
        elif key == ord('4'):
            mode = 4
        elif key == ord('m'):
            color_index = (color_index + 1) % len(colors)
        elif key == ord('c'):
            canvas[:] = 255
            print("[Canvas cleared]")
        elif key == ord('s'):
            cv2.imwrite("drawing_output.png", canvas)
            print("[Image saved as 'drawing_output.png']")
        elif key == ord('u') and undo_stack:
            canvas = undo_stack.pop()
            print("[Undo successful]")
        draw_instructions(canvas)
        cv2.imshow("Drawing", canvas)

    cv2.destroyAllWindows()

# Run the interactive drawing app
interactive_draw()
