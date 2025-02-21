from app.receipt_types.ross import parse_ross_receipt
from app.receipt_types.tjx import parse_tjx_receipt

def extract_data(response):
    store = ''
    stores = [
        'homegoods', 
        'marshalls', 
        'marshalls homegoods', 
        'ross',
        'tj-max'
    ]

    if response[0][0][1][0].lower() in stores:
        store = response[0][0][1][0].lower()

    if store in ['homegoods', 'marshalls', 'marshalls homegoods', 'tj-max']:
        receipt_data = parse_tjx_receipt(response[0])
        receipt_data['store'] = store
    elif store == 'ross':
        receipt_data = parse_ross_receipt(response[0])
        receipt_data['store'] = store    
    else:
        print('🚨 Could not extract')
        return {}

    return receipt_data
