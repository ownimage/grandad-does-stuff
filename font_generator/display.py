import tkinter as tk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import io

from vector2d import Vector2D

from ownimage.font_generator.blackletter import Blackletter


def display_svg(svg_data):
    # Convert SVG data to a file-like object
    svg_file = io.StringIO(svg_data)

    # Parse the SVG file into a drawing object
    drawing = svg2rlg(svg_file)

    # Create a new window
    root = tk.Tk()
    root.geometry("800x600")

    # Get the size of the SVG
    width, height = drawing.width, drawing.height
    print(f"width: {width}, height: {height}")

    # Render the SVG to an image
    renderPM.drawToFile(drawing, "temp.png", fmt="PNG")

    # Load the rendered image into a tkinter label
    img_label = tk.Label(root)
    img_label.place(x=0, y=0, width=width, height=height)

    # Use PhotoImage instead of tk.PhotoImage to load the PNG file
    img = tk.PhotoImage(file="temp.png")
    img_label.config(image=img)
    img_label.image = img  # keep a reference!

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    # svg = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    #   <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
    # </svg>"""

    blackletter = Blackletter(.5, 0, 3)
    svg = """<svg xmlns="http://www.w3.org/2000/svg"
     width="500"
     height="500"
     viewBox="0 0 500 500">
     <g transform="translate(0, 500) scale(1, -1)">
     
""" +  blackletter.svg(Vector2D(1,0), 10) + """
    </g>
</svg>"""
    print(svg)
    display_svg(svg)
