# Imports -------------------------
from tkinter import *
from tkinter import filedialog, messagebox
import PIL
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Set constants -------------------
TITLE_FONT = ('Century Gothic', 18, "bold")
BODY_FONT = ("Century Gothic", 12, "normal")
BUTTON_FONT = ("Century Gothic", 9, "normal")

PALE = "#FFF2F2"
LIGHT_BLUE = "#A9B5DF"
MED_BLUE = "#7886C7"
NAVY_BLUE = "#2D336B"

FILETYPES = [("Images", ".jpg .jpeg .btp .png .tiff .pgm .ppm .gif"),
             ("All files", "*.*")]


# Functions -----------------------
def open_file():
    """Select an image file and return as the chosen_image variable"""
    global chosen_image

    try:
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select an image",
                                              filetypes=FILETYPES)
    except AttributeError:
        return
    else:
        try:
            chosen_image = Image.open(filename).convert("RGBA")
            resize()
        except PIL.UnidentifiedImageError:
            messagebox.showerror(title="Error opening file", message="Please select a valid file")
            open_file()
        else:
            image_label = Label(text="Image loaded:\n"
                                     f"{filename}",
                                font=BUTTON_FONT,
                                bg=PALE,
                                justify=LEFT)
            image_label.grid(column=0, row=4, columnspan=3, sticky="w", pady=5)


def add_watermark(text, dark):
    """Adds a chosen text watermark to a preloaded image"""
    global chosen_image, canvas

    if dark:
        fill = (0, 0, 0, 255)
    else:
        fill = (255, 255, 255, 150)

    font_size = 36
    if len(text) > 18:
        font_size = 24
    if len(text) > 27:
        messagebox.showwarning(title="Long watermark", message="Watermark display may be limited")

    # Creates a transparent watermark layer
    watermark = Image.new("RGBA", chosen_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)

    # Calculates the size of the watermark text
    font = ImageFont.truetype("arial.ttf", font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Position watermark
    position = (chosen_image.width - text_width - 20, chosen_image.height - text_height - 20)
    draw.text(position, text, fill=fill, font=font)

    # Merge and convert
    watermarked_image = Image.alpha_composite(chosen_image, watermark)
    tk_image = ImageTk.PhotoImage(watermarked_image)

    # Display
    img_width, img_height = chosen_image.size
    canvas.delete("all")
    canvas.config(width=chosen_image.width, height=chosen_image.height)
    canvas.image = tk_image
    canvas.create_image(img_width // 2, img_height // 2, image=tk_image)
    canvas.grid(column=0, row=5, columnspan=3, pady=5)


def resize():
    global chosen_image
    if chosen_image.size[0] > chosen_image.size[1]:
        i = 0
        j = 1
    else:
        i = 1
        j = 0
    base = 400
    scale = (base / float(chosen_image.size[i]))
    hsize = int((float(chosen_image.size[j]) * float(scale)))
    chosen_image = chosen_image.resize((base, hsize), Image.Resampling.LANCZOS)


# Set variables -------------------
chosen_image = Image.open("base_img.jpg").convert("RGBA")  # Set initial image
resize()

# UI Setup ------------------------
window = Tk()
window.title("Water Marker")
window.config(padx=10, pady=20, bg=PALE)

# Labels
title = Label(text="Water Marker",
              font=TITLE_FONT,
              bg=PALE,
              fg=NAVY_BLUE, )
title.grid(column=0, row=0, columnspan=3, pady=15)

box_label = Label(text="Enter watermark text:",
                  font=BODY_FONT,
                  bg=PALE,
                  fg=NAVY_BLUE)
box_label.grid(column=0, row=1, columnspan=3, sticky="w")

# Boxes
entry_box = Entry(width=39)
entry_box.grid(column=0, row=2, columnspan=3, sticky="w", pady=10)
entry_box.insert(END, "Copyright")
entry_box.focus()

# Buttons
upload_button = Button(text="Upload Image",
                       command=open_file,
                       font=BUTTON_FONT,
                       bg=LIGHT_BLUE)
upload_button.grid(column=2, row=3, sticky="w")

add_light = Button(text="Light Mark",
                   command=lambda: add_watermark(entry_box.get(), False),
                   font=BUTTON_FONT,
                   bg=LIGHT_BLUE)
add_light.grid(column=0, row=3, sticky="w", padx=2)

add_dark = Button(text="Dark mark",
                  command=lambda: add_watermark(entry_box.get(), True),
                  font=BUTTON_FONT,
                  bg=LIGHT_BLUE)
add_dark.grid(column=1, row=3, sticky="w", padx=2)

# Canvas
canvas = Canvas(width=1, height=1, highlightthickness=0, bg=PALE)
canvas.grid(column=0, row=5, columnspan=4, pady=5)

window.mainloop()
