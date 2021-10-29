from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageGrab
import sys
import time
import ocr_bruteforced as ob


class App(tk.Tk):
    imgPath = ""
    card_w = 340
    card_h = 320
    card_gap_w = 10
    card_gap_h = 20
    global input_image
    global image_canvas_label

    def __init__(self):
        super().__init__()
        # self.grid_rowconfigure(2, weight=1)
        # self.grid_columnconfigure(2, weight=1)
        self.geometry("1280x640+0+0")
        self.resizable(False, False)
        self.title("too much nyalin")

        self.input_image = ImageTk.PhotoImage(
            (Image.open(self.imgPath + "temp.png")).resize((self.card_w, self.card_h), Image.ANTIALIAS))
        self.image_canvas_label = tk.Label(self, image=self.input_image)
        self.image_canvas_label.grid(row=0, column=0, padx=self.card_gap_w, pady=self.card_gap_h / 4)

        button1 = tk.Button(self, text="Open File", command=self.open)
        button1.grid(row=1, column=0, padx=self.card_gap_w, pady=self.card_gap_h / 4, sticky=tk.W)

        button2 = tk.Button(self, text="Hasil Pencocokan", command=self.output_module_posi)
        button2.grid(row=2, column=0, padx=self.card_gap_w, pady=self.card_gap_h / 4, sticky=tk.W)

        button3 = tk.Button(self, text="Reset Textbox", command=self.reset_text)
        button3.grid(row=3, column=0, padx=self.card_gap_w, pady=self.card_gap_h / 4, sticky=tk.W)

        self.text = tk.Text(self, wrap="word", height=30, width=120)
        self.text.grid(row=0, column=1, pady=self.card_gap_h / 4)
        self.text.tag_configure("stderr", foreground="#b22222")

        buttonCopy = tk.Button(self, text="Copy to Clipboard", command=self.copy)
        buttonCopy.grid(row=1, column=1, sticky=tk.E)

    def open(self):
        global im
        im = ImageGrab.grabclipboard()
        if im is not None:
            im.save('temp.png', 'PNG')
            self.input_image = ImageTk.PhotoImage(
                (Image.open("temp.png")).resize((self.card_w, self.card_h), Image.ANTIALIAS))
            self.image_canvas_label.configure(image=self.input_image)
        else:
            print("Is None! Failed to update clipboard.")


    def output_module_posi(self):
        result = ob.ocrBrute()
        print(result)
        self.text.insert(tk.END, result)

    def reset_text(self):
        self.text.delete('1.0', tk.END)

    def copy(self):
        current_text = self.text.get('1.0', tk.END)
        clipboardCopier = tk.Tk()
        clipboardCopier.withdraw()
        clipboardCopier.clipboard_clear()
        clipboardCopier.clipboard_append(current_text)
        clipboardCopier.update()  # now it stays on the clipboard after the window is closed
        clipboardCopier.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()