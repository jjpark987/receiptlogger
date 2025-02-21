import os
import tkinter as tk
from paddleocr import PaddleOCR
from PIL import Image, ImageTk
from tkinter import Label, Frame, Canvas, Scrollbar
from app.extract import extract_data

class ReceiptLogger:
    def __init__(self, root):
        self.initialize_variables(root)
        self.center_window(1000, 800)
        self.create_ui()

    def initialize_variables(self, root):
        # self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.root = root
        self.root.title('ReceiptLogger')
        self.receipts_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'PUT YO RECEIPTS HERE')
        self.image_refs = []

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_ui(self):
        # Create Folder Button
        self.create_folder_btn = tk.Button(self.root, text='Create Folder', command=self.create_folder)
        self.create_folder_btn.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text='', fg='green')
        self.status_label.pack(pady=10)

        # Extract Receipts Button
        self.run_paddleocr_btn = tk.Button(self.root, text='Extract Receipts', command=self.extract_receipts)
        self.run_paddleocr_btn.pack(pady=10)

        # Create a display frame for receipts
        display_frame = Frame(self.root, bg='white', width=1000, height=550)
        display_frame.pack_propagate(False)
        display_frame.pack(pady=10)





        # Scrollable Canvas inside display_frame
        self.scroll_canvas = Canvas(display_frame, bg='white', width=1000, height=550)
        
        # Scrollbar (define first)
        scrollbar = Scrollbar(display_frame, orient='vertical', command=self.scroll_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable Frame (must be defined before `create_window`)
        self.scroll_frame = Frame(self.scroll_canvas, bg='white')

        # Add scroll_frame inside scroll_canvas
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        self.scroll_canvas.pack(side='left', fill='both', expand=True)

        # Adjust scrolling region when content expands
        self.scroll_frame.bind('<Configure>', lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all')))





        # Create Sheets Button
        self.create_sheets_btn = tk.Button(self.root, text='Create Sheets', command=self.create_sheets)
        self.create_sheets_btn.pack(pady=10)

    def create_folder(self):
        if os.path.exists(self.receipts_folder):
            self.status_label.config(text='✅ The folder already exists', fg='green')
        else:
            try:
                os.makedirs(self.receipts_folder)
                self.status_label.config(text=f'✅ Folder created: {self.receipts_folder}', fg='green')
            except Exception as e:
                self.status_label.config(text=f'❌ Error creating folder: {str(e)}', fg='red')

    def extract_receipts(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.image_refs.clear()

        if not os.path.exists(self.receipts_folder):
            self.status_label.config(text='❌ Receipts folder not found', fg='red')
            return

        image_files = [os.path.join(self.receipts_folder, f) for f in os.listdir(self.receipts_folder) if f.lower().endswith('.png')]
        self.status_label.config(text=f'✅ Found {len(image_files)} receipts.', fg='green')

        for img_path in image_files:
            # try:
            #     raw_data = self.ocr.ocr(img_path, cls=True)
            #     receipt_data = extract_data(raw_data) if raw_data else {}
            # except Exception as e:
            #     self.status_label.config(text=f'❌ Error processing receipt: {str(e)}', fg='red')
            #     receipt_data = {}
            receipt_data = {
                'store': 'SuperMart',
                'location': 'Seatac Village',
                'date': '2024-02-20',
                'items': [
                    {'name': 'Apples', 'price': 3.50},
                    {'name': 'Milk', 'price': 2.99},
                    {'name': 'Bread', 'price': 2.50}
                ],
                'subtotal': 8.99,
                'tax': 0.72,
                'total': 9.71
            }
            self.display(img_path, receipt_data)

    def display(self, img_path, receipt_data):
        # Create a container
        container = Frame(self.scroll_frame, bg='white')
        container.pack(pady=10, padx=10, anchor='center', fill='both', expand=True)

        # Left Side: Image Display
        img_frame = Frame(container, bg='white', width=500, height=500)
        img_frame.pack_propagate(False)
        img_frame.pack(side='left', padx=10, pady=10, fill='y')

        img = Image.open(img_path)
        img = img.resize((500, 500))
        img_tk = ImageTk.PhotoImage(img)
        img_label = Label(img_frame, image=img_tk, bg='white')
        img_label.image = img_tk 
        img_label.pack()

        # Right Side: Receipt Data Display
        data_frame = Frame(container, bg='white', width=500, height=500)
        data_frame.pack_propagate(False)
        data_frame.pack(side='right', padx=10, pady=10, fill='y')

        date_label = Label(data_frame, text=f'📅 Date: {receipt_data.get('date', 'Unknown')}', fg='black', bg='white', font=('Arial', 12), anchor='w', width=50)
        date_label.pack(pady=5, padx=10, anchor='w')

        store_label = Label(data_frame, text=f'🛒 Store: {receipt_data.get('store', 'Unknown')}', fg='black', bg='white', font=('Arial', 12), anchor='w', width=50)
        store_label.pack(pady=5, padx=10, anchor='w')

        location_label = Label(data_frame, text=f'📍 Location: {receipt_data.get('location', 'Unknown')}', fg='black', bg='white', font=('Arial', 12), anchor='w', width=50)
        location_label.pack(pady=5, padx=10, anchor='w')

        items_label = Label(data_frame, text='🛍️ Items Purchased:', fg='black', bg='white', font=('Arial', 12), anchor='w', width=50)
        items_label.pack(pady=5, padx=10, anchor='w')
        for item in receipt_data.get('items', []):
            item_label = Label(data_frame, text=f'- {item['name']}: ${item['price']:.2f}', fg='black', bg='white', font=('Arial', 10), anchor='w', width=50)
            item_label.pack(pady=2, padx=10, anchor='w')

        subtotal_label = Label(data_frame, text=f'💰 Subtotal: ${receipt_data.get('subtotal', 0.00):.2f}', fg='black', bg='white', font=('Arial', 12), anchor='w', width=50)
        subtotal_label.pack(pady=2, padx=10, anchor='w')

        tax_label = Label(data_frame, text=f'💵 Tax: ${receipt_data.get('tax', 0.00):.2f}', fg='black', bg='white', font=('Arial', 12), anchor='w', width=50)
        tax_label.pack(pady=2, padx=10, anchor='w')

        total_label = Label(data_frame, text=f'✅ Total: ${receipt_data.get('total', 0.00):.2f}', fg='black', bg='white', font=('Arial', 12, 'bold'), anchor='w', width=50)
        total_label.pack(pady=5, padx=10, anchor='w')

    def create_sheets(self):
        ''' Placeholder function for exporting data to Google Sheets '''
        self.status_label.config(text='📤 Creating Google Sheets (Feature Not Implemented)', fg='green')

if __name__ == '__main__':
    root = tk.Tk()
    app = ReceiptLogger(root)
    root.mainloop()
