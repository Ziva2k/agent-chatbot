#!/usr/bin/env python3
"""
Thêm 3 bảng mới vào brain.db:
  1. products  — sản phẩm
  2. customers — khách hàng  
  3. orders    — đơn hàng

Nếu có file waitlist.json → import vào bảng customers (tránh trùng SĐT).
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brain.db')
WAITLIST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waitlist.json')

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # =====================
    # 1. BẢNG PRODUCTS
    # =====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL DEFAULT 0,
            description TEXT,
            stock INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Bảng 'products' đã tạo thành công.")

    # =====================
    # 2. BẢNG CUSTOMERS
    # =====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            zalo TEXT,
            email TEXT,
            registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
            source TEXT DEFAULT 'website',
            notes TEXT
        )
    ''')
    print("✅ Bảng 'customers' đã tạo thành công.")

    # =====================
    # 3. BẢNG ORDERS
    # =====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER,
            product_name TEXT,
            amount REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'pending',
            payment_method TEXT DEFAULT 'bank_transfer',
            sepay_transaction_id TEXT,
            notes TEXT,
            ordered_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    print("✅ Bảng 'orders' đã tạo thành công.")

    # =====================
    # THÊM DỮ LIỆU MẪU PRODUCTS
    # =====================
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Gói Thu Hồi Nợ Cá Nhân", 199000, "Dịch vụ thu hồi nợ cá nhân, tư vấn pháp lý miễn phí.", 999),
            ("Gói Thu Hồi Nợ Doanh Nghiệp", 499000, "Dịch vụ thu hồi nợ doanh nghiệp, đội ngũ luật sư chuyên nghiệp.", 999),
            ("Gói Tư Vấn Pháp Lý", 99000, "Tư vấn pháp lý trực tuyến 1 giờ.", 999),
            ("Gói Xử Lý Nợ Xấu Lâu Năm", 999000, "Xử lý nợ xấu trên 1 năm, hỗ trợ khởi kiện dân sự.", 999),
        ]
        cursor.executemany(
            "INSERT INTO products (name, price, description, stock) VALUES (?, ?, ?, ?)",
            sample_products
        )
        print(f"   📦 Đã thêm {len(sample_products)} sản phẩm mẫu.")

    # =====================
    # IMPORT WAITLIST.JSON → CUSTOMERS
    # =====================
    imported = 0
    skipped = 0

    if os.path.exists(WAITLIST_PATH):
        with open(WAITLIST_PATH, 'r', encoding='utf-8') as f:
            waitlist = json.load(f)

        # Hỗ trợ cả list và dict có key chứa list
        if isinstance(waitlist, dict):
            # Tìm key chứa list đầu tiên
            for key in waitlist:
                if isinstance(waitlist[key], list):
                    waitlist = waitlist[key]
                    break

        if isinstance(waitlist, list):
            for entry in waitlist:
                name = entry.get('name', entry.get('fullName', entry.get('ho_ten', '')))
                phone = entry.get('phone', entry.get('sdt', entry.get('phone_number', '')))
                zalo = entry.get('zalo', phone)  # Default zalo = phone
                email = entry.get('email', '')
                registered_at = entry.get('registered_at', entry.get('createdAt', entry.get('date', datetime.now().isoformat())))
                source = entry.get('source', 'waitlist')

                if not name or not phone:
                    skipped += 1
                    continue

                # Tránh trùng lặp theo số điện thoại
                cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
                if cursor.fetchone():
                    skipped += 1
                    continue

                cursor.execute(
                    "INSERT INTO customers (name, phone, zalo, email, registered_at, source) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, phone, zalo, email, registered_at, source)
                )
                imported += 1

            print(f"   📋 Import waitlist.json: {imported} khách hàng mới, {skipped} bỏ qua (trùng/thiếu data).")
        else:
            print("   ⚠️  waitlist.json không đúng format (cần array hoặc object chứa array).")
    else:
        print(f"   ℹ️  Không tìm thấy waitlist.json tại {WAITLIST_PATH}")
        print("       → Bạn có thể đặt file waitlist.json vào thư mục WED rồi chạy lại script này.")

    # =====================
    # IMPORT TỪ LOCALSTORAGE LEADS (nếu có JSON export)
    # =====================
    leads_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads.json')
    if os.path.exists(leads_path):
        with open(leads_path, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        if isinstance(leads, list):
            leads_imported = 0
            for lead in leads:
                name = lead.get('fullName', '')
                phone = lead.get('phone', '')
                if not name or not phone:
                    continue
                cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
                if cursor.fetchone():
                    continue
                cursor.execute(
                    "INSERT INTO customers (name, phone, zalo, registered_at, source) VALUES (?, ?, ?, ?, ?)",
                    (name, phone, phone, lead.get('createdAt', datetime.now().isoformat()), 'lead_form')
                )
                leads_imported += 1
            if leads_imported > 0:
                print(f"   📋 Import leads.json: {leads_imported} khách hàng mới.")

    conn.commit()

    # =====================
    # VERIFY
    # =====================
    print("\n" + "="*50)
    print("📊 TỔNG KẾT DATABASE:")
    print("="*50)
    
    tables = ['products', 'customers', 'orders', 'knowledge', 'business', 'brand_voice']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   📁 {table}: {count} records")

    print("\n📦 SẢN PHẨM:")
    cursor.execute("SELECT id, name, price, stock FROM products")
    for row in cursor.fetchall():
        print(f"   [{row[0]}] {row[1]} — {row[2]:,.0f}đ (còn {row[3]})")

    cursor.execute("SELECT COUNT(*) FROM customers")
    cust_count = cursor.fetchone()[0]
    if cust_count > 0:
        print(f"\n👥 KHÁCH HÀNG ({cust_count}):")
        cursor.execute("SELECT id, name, phone, source FROM customers LIMIT 10")
        for row in cursor.fetchall():
            print(f"   [{row[0]}] {row[1]} — {row[2]} ({row[3]})")

    conn.close()
    print("\n✅ Hoàn tất! Database đã được cập nhật.")

if __name__ == '__main__':
    main()
