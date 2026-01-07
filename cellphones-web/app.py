"""
CellphoneS Product Crawler - Flask Backend
Using requests + BeautifulSoup (lightweight, no browser needed)
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'products.db'

# Headers to mimic browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


def get_db():
    """Ket noi database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khoi tao database"""
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            brand TEXT,
            price INTEGER,
            original_price INTEGER,
            discount TEXT,
            image TEXT,
            url TEXT UNIQUE NOT NULL,
            in_stock INTEGER DEFAULT 1,
            specs TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS crawl_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()


def crawl_cellphones_product(url):
    """Crawl thong tin san pham tu CellphoneS using requests + BeautifulSoup"""

    if 'cellphones.com.vn' not in url:
        return {'error': 'URL khong phai tu CellphoneS'}

    product = {}

    try:
        # Fetch page content
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        # Lay ten san pham
        name_el = soup.select_one('h1')
        product['name'] = name_el.get_text(strip=True) if name_el else ''

        # Lay gia - thu nhieu selectors
        price = 0
        price_selectors = [
            '.tpt---sale-price .sale-price span',
            '.sale-price span',
            '.product__price--show',
            '.box-info__box-price .product__price--show',
            '.product-price .sale-price',
            '[class*="product__price"]',
            '.box-info__box-price',
        ]
        for sel in price_selectors:
            price_el = soup.select_one(sel)
            if price_el:
                price_text = price_el.get_text()
                price = parse_price(price_text)
                if price > 0:
                    break
        product['price'] = price

        # Lay gia goc
        original_price = price
        original_selectors = [
            '.tpt---sale-price .base-price',
            '.base-price',
            '.product__price--through',
            '.product-price del',
            'del[class*="price"]',
        ]
        for sel in original_selectors:
            original_el = soup.select_one(sel)
            if original_el:
                original_text = original_el.get_text()
                original_price = parse_price(original_text)
                if original_price > 0:
                    break
        product['original_price'] = original_price if original_price > 0 else price

        # Lay discount
        discount = ''
        if product['original_price'] > product['price'] and product['price'] > 0:
            discount_percent = round((product['original_price'] - product['price']) / product['original_price'] * 100)
            discount = f"-{discount_percent}%"
        product['discount'] = discount

        # Lay hinh anh - thu nhieu selectors
        image = ''
        img_selectors = [
            '.box-gallery__detail img',
            '.box-gallery__image img',
            '.gallery-product img',
            '.swiper-slide img[src*="cellphones"]',
            '.product-image img',
            'img[src*="media/catalog"]',
            '.box-gallery img',
            'img[src*="cdn"]',
        ]
        for sel in img_selectors:
            img_el = soup.select_one(sel)
            if img_el:
                src = img_el.get('src') or img_el.get('data-src')
                # Bo qua youtube thumbnail va placeholders
                if src and 'youtube' not in src and 'data:image' not in src and 'placeholder' not in src:
                    image = src
                    break
        product['image'] = image

        # Lay SKU tu URL
        product['sku'] = url.split('/')[-1].replace('.html', '')
        product['url'] = url
        product['brand'] = extract_brand(product['name'])
        product['in_stock'] = True

        # Lay thong so ky thuat
        specs = {}

        # Try to get specs from technical content section
        spec_rows = soup.select('.technical-content tr, .box-specifi tr, [class*="specification"] tr')
        for row in spec_rows:
            cols = row.select('td')
            if len(cols) >= 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                if key and value:
                    specs[key] = value

        # Alternative: try definition list format
        if not specs:
            dt_elements = soup.select('.technical-content dt, .box-specifi dt')
            dd_elements = soup.select('.technical-content dd, .box-specifi dd')
            for dt, dd in zip(dt_elements, dd_elements):
                key = dt.get_text(strip=True)
                value = dd.get_text(strip=True)
                if key and value:
                    specs[key] = value

        product['specs'] = specs

    except requests.exceptions.Timeout:
        return {'error': 'Timeout - trang web phan hoi qua cham'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Loi ket noi: {str(e)}'}
    except Exception as e:
        return {'error': str(e)}

    return product


def parse_price(price_text):
    """Chuyen doi text gia thanh so"""
    numbers = re.sub(r'[^\d]', '', price_text)
    return int(numbers) if numbers else 0


def extract_brand(name):
    """Lay brand tu ten san pham"""
    brands = ['Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Apple', 'MacBook',
              'Samsung', 'LG', 'Huawei', 'Microsoft', 'Gigabyte', 'Razer', 'iPhone',
              'iPad', 'Xiaomi', 'OPPO', 'Vivo', 'Realme', 'Sony', 'JBL', 'Marshall']
    name_lower = name.lower()
    for brand in brands:
        if brand.lower() in name_lower:
            return brand
    return ''


def save_product(product):
    """Luu san pham vao database"""
    conn = get_db()
    try:
        conn.execute('''
            INSERT OR REPLACE INTO products
            (sku, name, brand, price, original_price, discount, image, url, in_stock, specs, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['sku'],
            product['name'],
            product['brand'],
            product['price'],
            product['original_price'],
            product['discount'],
            product['image'],
            product['url'],
            product['in_stock'],
            json.dumps(product['specs'], ensure_ascii=False),
            datetime.now()
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving product: {e}")
        return False
    finally:
        conn.close()


def log_crawl(url, status, message=''):
    """Ghi log crawl"""
    conn = get_db()
    conn.execute('INSERT INTO crawl_history (url, status, message) VALUES (?, ?, ?)',
                 (url, status, message))
    conn.commit()
    conn.close()


# Routes
@app.route('/')
def index():
    """Trang chu"""
    return render_template('index.html')


@app.route('/api/crawl', methods=['POST'])
def api_crawl():
    """API crawl san pham"""
    data = request.json
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'success': False, 'error': 'Vui long nhap URL san pham'})

    # Crawl san pham
    result = crawl_cellphones_product(url)

    if 'error' in result:
        log_crawl(url, 'error', result['error'])
        return jsonify({'success': False, 'error': result['error']})

    # Luu vao database
    save_product(result)
    log_crawl(url, 'success')

    return jsonify({'success': True, 'product': result})


@app.route('/api/products')
def api_products():
    """API lay danh sach san pham da crawl"""
    conn = get_db()
    products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    conn.close()

    result = []
    for p in products:
        product = dict(p)
        product['specs'] = json.loads(product['specs']) if product['specs'] else {}
        result.append(product)

    return jsonify({'products': result})


@app.route('/api/products/<sku>')
def api_product_detail(sku):
    """API lay chi tiet san pham"""
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE sku = ?', (sku,)).fetchone()
    conn.close()

    if not product:
        return jsonify({'error': 'Khong tim thay san pham'}), 404

    result = dict(product)
    result['specs'] = json.loads(result['specs']) if result['specs'] else {}

    return jsonify({'product': result})


@app.route('/api/products/<sku>', methods=['DELETE'])
def api_delete_product(sku):
    """API xoa san pham"""
    conn = get_db()
    conn.execute('DELETE FROM products WHERE sku = ?', (sku,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})


@app.route('/api/history')
def api_history():
    """API lay lich su crawl"""
    conn = get_db()
    history = conn.execute('SELECT * FROM crawl_history ORDER BY created_at DESC LIMIT 50').fetchall()
    conn.close()

    return jsonify({'history': [dict(h) for h in history]})


# Init database on import (for Gunicorn)
init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
