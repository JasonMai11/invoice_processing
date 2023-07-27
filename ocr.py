from PyPDF2 import PdfReader
import os 
import database as db
from re import sub
from decimal import Decimal

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    page_count = len(reader.pages)
    text = ''
    for page_number in range(page_count):
        page = reader.pages[page_number]
        text += page.extract_text()
    return text

def extract_invoice_number(text):
    for line in text.split('\n'):
        if 'FBS-' in line:
            start = line.index('FBS-')
            return line[start:]

def extract_PO_number(text):
    for line in text.split('\n'):
        if '# SBAS' in line:
            start = line.index('# SBAS')
            return line[start:]
        
def flexible_invoice(text):
    search_words = ['Date:', 'FBS-', 'PO #']
    dictionary_searchwords_to_text = {'Date:': 'Invoice Date', 'FBS-': 'Invoice Number', 'PO #': 'PO Number'}
    price_bool = True 
    visited = set()
    return_dict = {}
    database_dict = db.view_all_items()
    item_id = db.item_ids()
    temp_insert = ""
    total = 0
    for line in text.split('\n'):
        if price_bool:
            for word in search_words:
                if word in line and word not in visited:
                    start = line.index(word)
                    if word == 'Date:':
                        return_dict[dictionary_searchwords_to_text[word]] = line[start + 6:]
                    elif word == 'PO #':
                        return_dict[dictionary_searchwords_to_text[word]] = line[start + 5:]
                    else:
                        return_dict[dictionary_searchwords_to_text[word]] = line[start:]
                    visited.add(word)
            for id_ in item_id:
                if id_[0] in line:
                    if not return_dict.get("Item"):
                        return_dict['Item'] = [database_dict[id_[0]][0]]
                    else:
                        return_dict['Item'].append(database_dict[id_[0]][0])
                    price_bool = False
        elif "$" in line:
            start_index = line.find("$", line.find("$") + 1)
            end_index = line.find(" ", start_index)
            amount = line[start_index:end_index]
            if not return_dict.get("Price"):
                return_dict['Price'] = [amount]
            else:
                return_dict['Price'].append(amount)
            total += Decimal(sub(r'[^\d.]', '', amount))
            price_bool = True
    return_dict['Total'] = total
    return return_dict

def main():
    invoice_name = os.listdir('./invoice')[0]
    pdf_path = './invoice/' + invoice_name
    text = extract_text_from_pdf(pdf_path)
    keyword_dict = flexible_invoice(text)
    print(keyword_dict)
    return keyword_dict


if __name__ == '__main__':
    main()
