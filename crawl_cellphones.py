"""
Script cao san pham laptop tu CellphoneS - Lay TAT CA thong so ky thuat
Su dung Playwright de click nut "Xem tat ca"
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import re
import time
from playwright.sync_api import sync_playwright


def crawl_10_products():
    """Cao 10 san pham dau tien tu trang laptop CellphoneS"""

    print("[*] Khoi dong trinh duyet...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        # Vao trang danh sach laptop
        url = "https://cellphones.com.vn/laptop.html"
        print(f"[*] Dang truy cap: {url}")
        page.goto(url, wait_until='networkidle', timeout=60000)

        # Doi trang load xong
        page.wait_for_selector('.product-info-container', timeout=30000)

        # Lay danh sach san pham
        product_items = page.query_selector_all('.product-info-container')
        print(f"[+] Tim thay {len(product_items)} san pham")

        results = []

        # Lay 10 san pham dau tien
        for i in range(min(10, len(product_items))):
            item = product_items[i]

            # Lay thong tin co ban
            link_el = item.query_selector('a.product__link')
            if not link_el:
                continue

            product_url = link_el.get_attribute('href')
            name_el = item.query_selector('.product__name h3')
            name = name_el.inner_text() if name_el else ''

            img_el = item.query_selector('.product__img')
            image = img_el.get_attribute('src') if img_el else ''

            price_el = item.query_selector('.product__price--show')
            price_text = price_el.inner_text() if price_el else '0'
            price = parse_price(price_text)

            original_el = item.query_selector('.product__price--through')
            original_text = original_el.inner_text() if original_el else price_text
            original_price = parse_price(original_text)

            discount_el = item.query_selector('.product__price--percent-detail span')
            discount = f"-{discount_el.inner_text()}" if discount_el else ''

            print(f"\n[{i+1}] {name[:60]}...")
            print(f"    Gia: {price:,}d (Goc: {original_price:,}d) {discount}")

            # Vao trang chi tiet de lay FULL thong so
            print(f"    [*] Dang lay thong so ky thuat...")
            specs = get_full_specs(context, product_url)

            product = {
                'stt': i + 1,
                'sku': extract_sku_from_url(product_url),
                'name': name,
                'brand': extract_brand(name),
                'price': price,
                'original_price': original_price,
                'discount': discount,
                'image': image,
                'url': product_url,
                'in_stock': True,
                'specs': specs,
            }
            results.append(product)

            print(f"    URL: {product_url}")
            print(f"    [+] Da lay {len(specs)} thong so")

        browser.close()

    return results


def get_full_specs(context, product_url):
    """Lay TAT CA thong so ky thuat bang cach click nut 'Xem tat ca'"""
    specs = {}

    try:
        page = context.new_page()
        page.goto(product_url, wait_until='networkidle', timeout=60000)

        # Doi cho phan thong so load
        page.wait_for_selector('.technical-content', timeout=10000)

        # Tim va click nut "Xem tat ca thong so"
        show_all_btn = page.query_selector('.button__show-modal-technical')
        if show_all_btn:
            show_all_btn.click()
            # Doi modal hien ra
            time.sleep(1)

            # Tim modal chua thong so day du
            modal = page.query_selector('.modal.is-active, [class*="modal"][class*="active"], .modal-technical')
            if modal:
                # Lay tat ca row trong modal
                rows = modal.query_selector_all('tr')
                for row in rows:
                    cols = row.query_selector_all('td')
                    if len(cols) >= 2:
                        key = cols[0].inner_text().strip()
                        value = cols[1].inner_text().strip()
                        if key and value:
                            specs[key] = value
            else:
                # Neu khong tim thay modal, thu lay tu trang chinh
                specs = get_specs_from_page(page)
        else:
            # Khong co nut xem tat ca, lay tu trang chinh
            specs = get_specs_from_page(page)

        page.close()

    except Exception as e:
        print(f"    [!] Loi: {e}")

    return specs


def get_specs_from_page(page):
    """Lay thong so tu trang hien tai"""
    specs = {}

    rows = page.query_selector_all('.technical-content tr, .technical-content-item')
    for row in rows:
        cols = row.query_selector_all('td')
        if len(cols) >= 2:
            key = cols[0].inner_text().strip()
            value = cols[1].inner_text().strip()
            if key and value:
                specs[key] = value

    return specs


def parse_price(price_text):
    """Chuyen doi text gia thanh so"""
    numbers = re.sub(r'[^\d]', '', price_text)
    return int(numbers) if numbers else 0


def extract_sku_from_url(url):
    """Lay SKU tu URL"""
    if url:
        slug = url.split('/')[-1].replace('.html', '')
        return slug
    return ''


def extract_brand(name):
    """Lay brand tu ten san pham"""
    brands = ['Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Apple', 'MacBook',
              'Samsung', 'LG', 'Huawei', 'Microsoft', 'Gigabyte', 'Razer']
    name_lower = name.lower()
    for brand in brands:
        if brand.lower() in name_lower:
            return brand
    return ''


if __name__ == "__main__":
    print("=" * 60)
    print("CELLPHONES CRAWLER - LAY 10 SAN PHAM + FULL THONG SO")
    print("=" * 60)

    products = crawl_10_products()

    if products:
        print(f"\n{'=' * 60}")
        print(f"DA LAY DUOC {len(products)} SAN PHAM")
        print("=" * 60)

        with open('cellphones_10_products.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print("\n[+] Da luu vao file: cellphones_10_products.json")

        # Hien thi thong so san pham dau tien
        print("\n[SAMPLE] Thong so san pham dau tien:")
        if products[0].get('specs'):
            for k, v in list(products[0]['specs'].items()):
                print(f"  - {k}: {v[:60]}..." if len(v) > 60 else f"  - {k}: {v}")
    else:
        print("\n[!] Khong lay duoc san pham")
