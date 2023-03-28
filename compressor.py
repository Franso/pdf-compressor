import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import Image
import io
import PyPDF2


def compress_pdf(file_path, quality):
    """Takes in a pdf and compresses it"""
    # Open the PDF file
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        pdf_writer = PyPDF2.PdfWriter()

        # iterate over all the pages in the PDF
        for page in pdf_reader.pages:
            page.compress_content_streams()
            pdf_writer.add_page(page)

        # Save the compressed PDF file
        new_file_path = os.path.splitext(file_path)[0] + '_compressed.pdf'
        with open(new_file_path, 'wb') as f:
            pdf_writer.write(f)

    return new_file_path


class PDFCompressorApp:
    def __init__(self, master):
        self.master = master
        self.master.title('PDF Compressor')
        self.master.geometry('300x150')

        # create a button to select a file
        self.file_path = ''
        self.select_button = tk.Button(
            master, text='Select PDF file', command=self.select_file)
        self.select_button.pack(pady=10)

        # create a slider to select the compression quality
        self.quality_label = tk.Label(
            master, text='Select compression quality:')
        self.quality_label.pack()
        self.quality_slider = tk.Scale(
            master, from_=10, to=100, orient='horizontal')
        self.quality_slider.pack()

        # create a button to compress the selected file
        self.compress_button = tk.Button(
            master, text='Compress', command=self.compress)
        self.compress_button.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()

    def compress(self):
        if not self.file_path:
            messagebox.showerror('Error', 'Please select a PDF file.')
            return

        quality = self.quality_slider.get()
        try:
            compressed_file_path = compress_pdf(self.file_path, quality)
            messagebox.showinfo(
                'Success', f'PDF file compressed successfully.\nCompressed file: {compressed_file_path}')
        except Exception as e:
            messagebox.showerror(
                'Error', f'Failed to compress PDF file.\nError message: {str(e)}')


root = tk.Tk()
app = PDFCompressorApp(root)
root.mainloop()
