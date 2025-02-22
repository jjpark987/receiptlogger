import customtkinter as ctk
import gspread
import os
import subprocess
import traceback
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
# from paddleocr import PaddleOCR
from PIL import Image, ImageTk
from app.process_data import process

load_dotenv()

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
        self.receipt_data_refs = []

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_ui(self):
        # create folder button
        self.create_folder_btn = ctk.CTkButton(self.root, text='Create Folder', command=self.create_folder)
        self.create_folder_btn.pack(pady=20)

        # status label
        self.status_label = ctk.CTkLabel(self.root, text='')
        self.status_label.pack(pady=10)

        # extract receipt button
        self.extract_receipts_btn = ctk.CTkButton(self.root, text='Extract Receipts', command=self.extract_receipts)
        self.extract_receipts_btn.pack(pady=10)

        # scrollable frame for displaying receipts
        self.scroll_frame = ctk.CTkScrollableFrame(self.root, width=1000, height=500)
        self.scroll_frame.pack(pady=10, fill='both', expand=True)

        # upload to google sheets button
        self.upload_data_btn = ctk.CTkButton(self.root, text='Upload Data', command=self.upload_data)
        self.upload_data_btn.pack(pady=20)

    def create_folder(self):
        if os.path.exists(self.receipts_folder):
            self.status_label.configure(text='✅ The folder already exists')
        else:
            try:
                os.makedirs(self.receipts_folder)
                self.status_label.configure(text=f'✅ Folder created: {self.receipts_folder}')
            except Exception as e:
                self.status_label.configure(text=f'❌ Error creating folder: {str(e)}')

    def extract_receipts(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.image_refs.clear()

        if not os.path.exists(self.receipts_folder):
            self.status_label.configure(text='❌ Receipts folder not found')
            return

        image_files = [os.path.join(self.receipts_folder, f) for f in os.listdir(self.receipts_folder) if f.lower().endswith('.png')]
        self.status_label.configure(text=f'✅ Found {len(image_files)} receipts')

        def run_ocr(img_path):
            command = f'docker exec receiptlogger python3 -m paddleocr --image_dir {img_path} --use_angle_cls true'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout

        for img_path in image_files:
            try:
                ocr_output = run_ocr(img_path) 
                receipt_data = process(ocr_output) 
            except Exception as e:
                self.status_label.configure(text=f'❌ Error processing receipts: {str(e)}')
                return
            self.display(img_path, receipt_data)

    def display(self, img_path, receipt_data):
        container = ctk.CTkFrame(self.scroll_frame)
        container.pack(pady=10, padx=10, anchor='center', fill='both', expand=True)

        # image
        img_frame = ctk.CTkFrame(container, width=500, height=500, corner_radius=10)
        img_frame.pack_propagate(False)
        img_frame.pack(side='left', padx=10, pady=10, fill='y')

        img = Image.open(img_path)
        img.thumbnail((500, 500))
        img_tk = ImageTk.PhotoImage(img)
        self.image_refs.append(img_tk)

        img_label = ctk.CTkLabel(img_frame, image=img_tk, text='')
        img_label.pack()
        img_label.image = img_tk
        img_label.bind('<Button-1>', lambda event, path=img_path: self.open_zoomed_image(path))

        # receipt data
        self.receipt_data_refs.append(receipt_data)
        data_frame = ctk.CTkFrame(container, width=500, height=500, corner_radius=0)
        data_frame.pack_propagate(False)
        data_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

        if not receipt_data:
            image = Image.open('static/no_data.jpeg') 
            image = image.resize((400, 400)) 
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 400))

            label = ctk.CTkLabel(data_frame, image=ctk_image, text='')
            label.pack(expand=True)
            return

        data_frame.grid_columnconfigure(0, weight=2)
        data_frame.grid_columnconfigure(1, weight=1)
        data_frame.grid_columnconfigure(2, weight=1)

        date_label = ctk.CTkLabel(data_frame, text=f'📅 {receipt_data.get('date', 'N/A')}', font=('Arial', 12), anchor='w')
        date_label.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=3)

        store_label = ctk.CTkLabel(data_frame, text=f'🛒 {receipt_data.get('store', 'N/A')}', font=('Arial', 12), anchor='w')
        store_label.grid(row=1, column=0, columnspan=3, sticky='w', padx=10, pady=3)

        for i, item in enumerate(receipt_data.get('items', []), start=4):
            ctk.CTkLabel(data_frame, text=f'       {item['sku']}   {item['name']}', font=('Arial', 10), anchor='w').grid(
                row=i, column=0, sticky='w', padx=10, pady=2)  
            ctk.CTkLabel(data_frame, text=f'${item['price']:.2f}', font=('Arial', 10), anchor='e').grid(
                row=i, column=1, sticky='e', padx=10, pady=2)
            ctk.CTkLabel(data_frame, text=f'${item['taxed']:.2f}', font=('Arial', 10), anchor='e').grid(
                row=i, column=2, sticky='e', padx=10, pady=2)

        tax_rate_label = ctk.CTkLabel(data_frame, text=f'📈 Tax Rate:', font=('Arial', 12), anchor='w')
        tax_rate_label.grid(row=i+1, column=0, sticky='ew', padx=10, pady=3)
        tax_rate_value = ctk.CTkLabel(data_frame, text=f'{round(receipt_data.get('tax_rate', 0.00) * 100, 2)}%', font=('Arial', 12), anchor='e')
        tax_rate_value.grid(row=i+1, column=2, sticky='ew', padx=10, pady=3)

        tax_label = ctk.CTkLabel(data_frame, text=f'⚖️ Tax:', font=('Arial', 12), anchor='w')
        tax_label.grid(row=i+2, column=0, sticky='ew', padx=10, pady=3)
        tax_value = ctk.CTkLabel(data_frame, text=f'${receipt_data.get('tax', 0.00):.2f}', font=('Arial', 12), anchor='e')
        tax_value.grid(row=i+2, column=2, sticky='ew', padx=10, pady=3)

        total_label = ctk.CTkLabel(data_frame, text=f'✅ Total:', font=('Arial', 12, 'bold'), anchor='w')
        total_label.grid(row=i+3, column=0, sticky='ew', padx=10, pady=5)
        total_value = ctk.CTkLabel(data_frame, text=f'${receipt_data.get('total', 0.00):.2f}', font=('Arial', 12, 'bold'), anchor='e')
        total_value.grid(row=i+3, column=2, sticky='ew', padx=10, pady=5)
    
    def open_zoomed_image(self, img_path):
        zoom_popup = ctk.CTkToplevel(self.root)
        zoom_popup.title('Zoomed Receipt')
        zoom_popup.geometry('800x800')

        img = Image.open(img_path) 
        img.thumbnail((800, 800))
        img_tk = ImageTk.PhotoImage(img)

        label = ctk.CTkLabel(zoom_popup, image=img_tk, text='') 
        label.pack(expand=True) 
        label.image = img_tk

    def upload_data(self):
        if not self.receipt_data_refs:
            self.status_label.configure(text='⚠️ Extract receipts before uploading')
            return

        self.status_label.configure(text='📤 Uploading to Google Sheets...')

        # authenticate and prepare data to append
        credentials = os.getenv('GOOGLE_KEY')
        sheet_id = os.getenv('SPREADSHEET_ID')
        worksheet_name = os.getenv('WORKSHEET_NAME')
        if not credentials:
            self.status_label.configure(text='❌ Google Service Key not found in .env')
            return
        try:
            creds = Credentials.from_service_account_file(credentials, scopes=['https://www.googleapis.com/auth/spreadsheets'])
            sheet = gspread.authorize(creds).open_by_key(sheet_id)
            worksheet = sheet.worksheet(worksheet_name)

            print(f'✅ Successfully connected to Google Sheet: {sheet.title}')
            self.status_label.configure(text=f'✅ Connected to Google Sheets "{sheet.title}"')

            rows_to_append = []
            for receipt in self.receipt_data_refs:
                store = receipt['store']
                date = datetime.strptime(receipt['date'], '%m/%d/%Y' if len(receipt['date']) == 10 else '%m/%d/%y').strftime('%m/%d/%y')
                tax_rate = receipt['tax_rate']
                item_map = {}

                for item in receipt['items']:
                    sku = item['sku']
                    if sku not in item_map:
                        item_map[sku] = {
                            'name': item['name'],
                            'quantity': 1,
                            'price': item['price'], 
                            'taxed': item['taxed']
                        }
                    else:
                        item_map[sku]['quantity'] += 1

                rows_to_append.extend([
                    [
                        store,
                        date,
                        sku,
                        data['quantity'],
                        data['name'],
                        data['price'],
                        tax_rate,
                        data['taxed']
                    ]
                    for sku, data in item_map.items()
                ])

            # append to google sheets
            if rows_to_append:
                next_empty_row = len(worksheet.get_all_values()) + 1
                worksheet.insert_rows(rows_to_append, row=next_empty_row, value_input_option='USER_ENTERED')

                print(f'✅ Successfully added {len(rows_to_append)} rows to Google Sheets')
                self.status_label.configure(text=f'✅ Uploaded {len(rows_to_append)} rows to Google Sheets')
            else:
                print('⚠️ No data to upload')
                self.status_label.configure(text='⚠️ No data to upload')

        except Exception as e:
            # traceback.print_exc()
            print(f'❌ Google Sheets connection error: {e}')
            self.status_label.configure(text='❌ Google Sheets authentication failed')

if __name__ == '__main__':
    root = ctk.CTk()
    app = ReceiptLogger(root)
    root.mainloop()
