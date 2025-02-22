import re
from app.receipt_types.ross import parse_ross_receipt
from app.receipt_types.tjx import parse_tjx_receipt

def extract_data(response=[]):
    if not response:
        print('🚨 No data to extract')
        return

    stores = {
        'homegoods': 'HomeGoods',
        'marshalls': 'Marshalls',
        'marshalls homegoods': 'Marshalls-HomeGoods',
        'ross': 'Ross',
        't.j.maxx': 'T.J.Maxx',
        'tjmaxx': 'T.J.Maxx'
    }
    store = ''

    if response[0][0][1][0].lower() in stores:
        store = stores[response[0][0][1][0].lower()]
    else:
        for item in response[0]:
            possible_text = item[1][0].lower()
            for key in stores.keys():
                if re.search(rf'\b{re.escape(key)}\b', possible_text):
                    store = stores[key]  
                    break

    if store in ['HomeGoods', 'Marshalls', 'Marshalls-HomeGoods', 'T.J.Maxx']:
        receipt_data = parse_tjx_receipt(response[0])
        receipt_data['store'] = store
    elif store == 'Ross':
        receipt_data = parse_ross_receipt(response[0])
        receipt_data['store'] = store 
    else:
        print('🚨 Not included in the list of stores')
        return {}

    return receipt_data

def calculate_item_tax(receipt_data={}):
    if not receipt_data:
        print('🚨 No receipt data to calculate')
        return {}
    
    for item in receipt_data['items']:
        item['taxed'] = round(item['price'] * (1 + receipt_data['tax_rate']), 2)

    return receipt_data

def process(response=[]):
    # from paddleocr import PaddleOCR
    # ocr = PaddleOCR(use_angle_cls=True, lang='en')
    # response = ocr.ocr('dev/sample_receipts/tjmaxx.png', cls=True)
    receipt_data = extract_data(response)
    return calculate_item_tax(receipt_data)

if __name__ == '__main__':
    process()
