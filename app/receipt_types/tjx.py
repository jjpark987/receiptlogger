import re

PRICE_PATTERN = r'^\$(\d+\.\d{2})$'
STANDALONE_SKU_PATTERN = r'^\d{6}$'
ATTACHED_SKU_PATTERN = r'^(.+?)(\d{6})$'
SALES_TAX_PATTERN = r'(\d+\.\d+)%'
DATE_PATTERN = r'(\d{2}/\d{2}/\d{4})'

def parse_tjx_receipt(receipt: list) -> dict:
    date = ''
    location = ''
    items = []
    subtotal = 0.0
    tax_rate = 0.0
    tax = 0.0
    total = 0.0

    i = 0
    while i < len(receipt):
        text = receipt[i][1][0].lower()
        # print(f'Processing line {i}: {text}')

        if i == 1:
            location = text

        price_match = re.match(PRICE_PATTERN, text)
        if price_match:
            price = float(price_match.group(1))

            if i - 1 >= 0:
                prev_line = receipt[i - 1][1][0].lower()
                sku = ''
                name = ''

                if re.match(STANDALONE_SKU_PATTERN, prev_line):
                    sku = prev_line
                    if i - 2 >= 0:
                        name = receipt[i - 2][1][0].lower()
                        items.append({
                            'sku': sku, 
                            'name': name, 
                            'price': price
                        })
                elif re.match(ATTACHED_SKU_PATTERN, prev_line):  
                    match = re.match(ATTACHED_SKU_PATTERN, prev_line)
                    items.append({
                            'sku': match.group(2).strip() , 
                            'name': match.group(1).strip(), 
                            'price': round(price, 2)
                        })
                elif 'subtotal' in prev_line:
                    subtotal = round(price, 2)
                elif 'tax' in prev_line:
                    if not tax_rate:
                        tax_rate = round(float(re.search(SALES_TAX_PATTERN, prev_line).group(1).strip()) / 100, 4)
                    tax = round(price, 2)
                elif 'total' in prev_line:
                    total = round(price, 2)

        date_match = re.search(DATE_PATTERN, text)
        if date_match:
            date = date_match.group(1).strip()

        i += 1 

    return {
        'location': location,
        'items': items,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax': tax,
        'total': total,
        'date': date
    }
