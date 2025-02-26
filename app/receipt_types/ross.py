import re

ITEM_PATTERN = r'^(\d+)\s+([a-z0-9 .-]+)$'          
PRICE_PATTERN = r'^(-?)\$(\d+\.\d{2})[a-z]?$' 
SALES_TAX_PATTERN = r'(\d+\.\d+)%'
DATE_PATTERN = r'^date:\s*(\d{2}/\d{2}/\d{2})'

def find_price_next_line(receipt: list, i: int) -> float:
    if i + 1 < len(receipt):  
        next_line = receipt[i + 1][1][0].lower()
        price_match = re.match(PRICE_PATTERN, next_line)
        if price_match:
            sign = price_match.group(1)
            price_value = price_match.group(2) 
            return float(sign + price_value)
    return 0.0

def parse_ross_receipt(receipt: list) -> dict:
    date = ''
    location = ''
    items = []
    subtotal = 0.0
    tax_rate = 0.0
    tax = 0.0
    total = 0.0

    skip = False
    i = 0

    while i < len(receipt):
        text = receipt[i][1][0].lower()
        # print(f'Processing line {i}: {text}')

        if i == 2:
            location = text

        if 'begin return' in text:
            skip = True
            i += 1
            continue
        if 'end return' in text:
            skip = False
            i += 1
            continue
        if skip:
            i += 1
            continue

        item_match = re.match(ITEM_PATTERN, text)
        if item_match:
            items.append({
                'sku': item_match.group(1),
                'name': item_match.group(2),
                'price': find_price_next_line(receipt, i)
            })

        if 'subtotal' in text:
            subtotal = find_price_next_line(receipt, i)

        if 'tax' in text:
            if not tax_rate:
                tax_rate = round(float(re.search(SALES_TAX_PATTERN, text).group(1).strip()) / 100, 4)
            tax += round(find_price_next_line(receipt, i), 2)

        if 'total' in text:
            total = find_price_next_line(receipt, i)
        
        date_match = re.match(DATE_PATTERN, text)
        if date_match:
            date = date_match.group(1)

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
