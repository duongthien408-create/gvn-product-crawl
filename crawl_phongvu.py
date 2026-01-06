"""
Script cao san pham laptop tu Phong Vu - Version don gian
"""

import requests
import json
from bs4 import BeautifulSoup


def crawl_10_products():
    """Cao 10 san pham dau tien tu trang laptop Phong Vu"""

    url = "https://phongvu.vn/c/laptop"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    print(f"[*] Dang fetch: {url}")

    response = requests.get(url, headers=headers, timeout=30)
    print(f"[*] Status: {response.status_code}")

    if response.status_code != 200:
        print(f"[!] Loi: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Tim __NEXT_DATA__ (Next.js stores data here)
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    if script_tag:
        print("[+] Tim thay __NEXT_DATA__")
        data = json.loads(script_tag.string)

        # Luu ra file de debug
        with open('debug_next_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("[+] Da luu __NEXT_DATA__ vao debug_next_data.json")

        # In cac keys de tim duong dan
        page_props = data.get('props', {}).get('pageProps', {})
        print(f"[DEBUG] pageProps keys: {list(page_props.keys())}")

        # Thu cac duong dan khac nhau
        products = []

        # Thu 1: serverProducts (Phong Vu dung cai nay)
        products = page_props.get('serverProducts', [])
        if products:
            print(f"[+] Found in serverProducts: {len(products)}")

        # Thu 2: productListing.products
        if not products:
            products = page_props.get('productListing', {}).get('products', [])
            if products:
                print(f"[+] Found in productListing.products: {len(products)}")

        # Thu 3: products truc tiep
        if not products:
            products = page_props.get('products', [])
            if products:
                print(f"[+] Found in products: {len(products)}")

        if products:
            results = []
            for i, p in enumerate(products[:10]):
                price_data = p.get('price', {})
                price = price_data.get('latestPrice', 0)
                original = price_data.get('supplierRetailPrice', price)
                discount = price_data.get('discountPercent', '')

                # Lay URL tu link.as.pathname
                link_data = p.get('link', {}).get('as', {})
                url_path = link_data.get('pathname', '')

                product = {
                    'stt': i + 1,
                    'sku': p.get('sku', ''),
                    'name': p.get('name', ''),
                    'brand': p.get('brand', {}).get('name', ''),
                    'price': price,
                    'original_price': original,
                    'discount': discount,
                    'image': p.get('imageUrl', ''),
                    'url': f"https://phongvu.vn{url_path}",
                    'in_stock': p.get('stockQuantity', 0) > 0,
                }
                results.append(product)
                print(f"\n[{i+1}] {product['name'][:60]}...")
                print(f"    SKU: {product['sku']} | Brand: {product['brand']}")
                print(f"    Gia: {price:,}d (Goc: {original:,}d) {discount}")
                print(f"    URL: {product['url']}")

            return results
        else:
            print("[!] Khong tim thay products trong NEXT_DATA")
            return []
    else:
        print("[!] Khong tim thay __NEXT_DATA__")
        return []


if __name__ == "__main__":
    print("=" * 60)
    print("PHONG VU CRAWLER - LAY 10 SAN PHAM")
    print("=" * 60)

    products = crawl_10_products()

    if products:
        print(f"\n{'=' * 60}")
        print(f"DA LAY DUOC {len(products)} SAN PHAM")
        print("=" * 60)

        with open('phongvu_10_products.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print("\n[+] Da luu vao file: phongvu_10_products.json")
    else:
        print("\n[!] Khong lay duoc san pham")
        print("[*] Kiem tra file debug_next_data.json de xem cau truc data")
