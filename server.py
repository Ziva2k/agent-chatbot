#!/usr/bin/env python3
"""
Thu Hồi Nợ PRO — Admin API Server
Chạy: python3 server.py
Truy cập: http://localhost:5000/admin
"""

import sqlite3
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import resend
import threading
import time
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brain.db')

# Init Resend
resend.api_key = os.environ.get('RESEND_API_KEY')
if resend.api_key:
    print("✅ Đã kết nối Resend API từ .env.")
else:
    print("⚠️  Không tìm thấy RESEND_API_KEY trong .env.")



def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def send_email_resend(to_email, subject, content):
    if not resend.api_key:
        print("⚠️ Không thể gửi email, chưa có Resend API Key.")
        return
        
    # MẸO: Vì bản miễn phí Resend cấm gửi sai email đăng ký (dù là có '+test'),
    # ta cắt luôn chữ '+test' ra khỏi đầu kia, để Resend nhận diện đúng chủ!
    clean_email = to_email.replace('+test', '').replace('+TEST', '')
    
    # Chuyển đổi markdown dởm thành HTML (xuống dòng = <br>)
    html_content = content.replace('\n', '<br>')
    
    params = {
        "from": "Thu Hồi Nợ PRO <onboarding@resend.dev>",
        "to": [clean_email],
        "subject": subject,
        "html": html_content
    }
    try:
        resend.Emails.send(params)
        print(f"📧 Đã gửi email: {subject} -> {clean_email} (Gốc: {to_email})")
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}")

def run_email_sequenceThread(email, test_mode):
    # Đọc file email_sequence.md
    seq_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'email_sequence.md')
    if not os.path.exists(seq_path):
        print("⚠️ Không tìm thấy email_sequence.md")
        return
        
    with open(seq_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by "---"
    parts = content.split('---')
    emails = []
    for p in parts:
        p = p.strip()
        if not p: continue
        # Extract title
        m = re.search(r'\*\*Tiêu đề:\*\*\s*(.+)', p)
        subject = m.group(1).strip() if m else "Thông báo từ Thu Hồi Nợ PRO"
        
        # Extract body (skip until after Tiêu đề)
        parts_title_split = re.split(r'\*\*Tiêu đề:\*\*\s*.+', p)
        body = parts_title_split[-1].strip() if len(parts_title_split) > 1 else p
        emails.append((subject, body))
        
    if len(emails) < 3:
        print("⚠️ Cảnh báo: File email_sequence.md chưa đủ 3 email.")

    e1 = emails[0] if len(emails) > 0 else ("Email 1", "Nội dung 1")
    e2 = emails[1] if len(emails) > 1 else ("Email 2", "Nội dung 2")
    e3 = emails[2] if len(emails) > 2 else ("Email 3", "Nội dung 3")
    
    if test_mode:
        print(f"🚀 [TEST MODE] Gửi toàn bộ 3 email cho {email}")
        send_email_resend(email, e1[0], e1[1])
        time.sleep(2)
        send_email_resend(email, e2[0], e2[1])
        time.sleep(2)
        send_email_resend(email, e3[0], e3[1])
    else:
        print(f"🕒 [NORMAL MODE] Bắt đầu sequence cho {email}")
        # Gửi Email 1 ngay lập tức
        send_email_resend(email, e1[0], e1[1])
        
        # Chờ 2 ngày
        time.sleep(172800)
        send_email_resend(email, e2[0], e2[1])
        
        # Chờ 1 ngày
        time.sleep(86400)
        send_email_resend(email, e3[0], e3[1])

def trigger_email_sequence(email):
    if not email: return
    test_mode = '+test' in email.lower()
    t = threading.Thread(target=run_email_sequenceThread, args=(email, test_mode))
    t.daemon = True
    t.start()


def trigger_order_email(customer_email, product_name, amount):
    if not customer_email: return
    
    subject = f"Xác nhận đơn hàng: {product_name} - Bắt tay vào việc thôi"
    content = f"""Chào bạn,
    
Tôi xác nhận hệ thống đã ghi nhận đơn hàng của bạn:
- **Sản phẩm/Dịch vụ:** {product_name}
- **Giá trị:** {amount:,.0f} VNĐ

Tiền trao thì cháo múc. Làm việc với Thu Hồi Nợ PRO là vậy: Sòng phẳng, súc tích và dứt điểm. Bạn đã bước một chân vào hành trình đòi lại tiền của mình rồi đấy.

**Phải làm gì tiếp theo?**
Đội ngũ sẽ liên hệ trực tiếp với bạn qua Zalo hoặc số điện thoại bạn đã cung cấp để bắt đầu quy trình làm hồ sơ. Bạn hãy chuẩn bị sẵn mọi giấy tờ, bằng chứng (tin nhắn, hợp đồng, ủy nhiệm chi...) liên quan đến con nợ nhé.

Nếu có bất cứ thắc mắc gì thêm, cứ nhắn thẳng vào Zalo.

Thân,
**Thu Hồi Nợ PRO**"""
    
    t = threading.Thread(target=send_email_resend, args=(customer_email, subject, content))
    t.daemon = True
    t.start()

# ========== SERVE PAGES ==========
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/admin')
def admin_page():
    return send_from_directory('.', 'admin.html')


# ========== PRODUCTS API ==========
@app.route('/api/products', methods=['GET'])
def get_products():
    db = get_db()
    rows = db.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/products', methods=['POST'])
def create_product():
    d = request.json
    db = get_db()
    db.execute(
        "INSERT INTO products (name, price, description, stock) VALUES (?, ?, ?, ?)",
        (d['name'], d.get('price', 0), d.get('description', ''), d.get('stock', 0))
    )
    db.commit()
    db.close()
    return jsonify({"success": True}), 201


@app.route('/api/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    d = request.json
    db = get_db()
    db.execute(
        "UPDATE products SET name=?, price=?, description=?, stock=?, updated_at=? WHERE id=?",
        (d['name'], d.get('price', 0), d.get('description', ''), d.get('stock', 0),
         datetime.now().isoformat(), pid)
    )
    db.commit()
    db.close()
    return jsonify({"success": True})


@app.route('/api/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    db = get_db()
    db.execute("DELETE FROM products WHERE id=?", (pid,))
    db.commit()
    db.close()
    return jsonify({"success": True})


# ========== CUSTOMERS API ==========
@app.route('/api/customers', methods=['GET'])
def get_customers():
    db = get_db()
    rows = db.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/customers', methods=['POST'])
def create_customer():
    d = request.json
    db = get_db()
    try:
        db.execute(
            "INSERT INTO customers (name, phone, zalo, email, source, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (d['name'], d.get('phone', ''), d.get('zalo', ''), d.get('email', ''),
             d.get('source', 'admin'), d.get('notes', ''))
        )
        db.commit()
        trigger_email_sequence(d.get('email', ''))
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({"success": False, "error": "Số điện thoại đã tồn tại"}), 400
    db.close()
    return jsonify({"success": True}), 201


@app.route('/api/customers/<int:cid>', methods=['PUT'])
def update_customer(cid):
    d = request.json
    db = get_db()
    try:
        db.execute(
            "UPDATE customers SET name=?, phone=?, zalo=?, email=?, source=?, notes=? WHERE id=?",
            (d['name'], d.get('phone', ''), d.get('zalo', ''), d.get('email', ''),
             d.get('source', ''), d.get('notes', ''), cid)
        )
        db.commit()
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({"success": False, "error": "Số điện thoại đã tồn tại"}), 400
    db.close()
    return jsonify({"success": True})


@app.route('/api/customers/<int:cid>', methods=['DELETE'])
def delete_customer(cid):
    db = get_db()
    db.execute("DELETE FROM customers WHERE id=?", (cid,))
    db.commit()
    db.close()
    return jsonify({"success": True})


# ========== ORDERS API ==========
@app.route('/api/orders', methods=['GET'])
def get_orders():
    db = get_db()
    rows = db.execute("""
        SELECT o.*, c.name as customer_name, c.phone as customer_phone, p.name as prod_name
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        LEFT JOIN products p ON o.product_id = p.id
        ORDER BY o.id DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/orders', methods=['POST'])
def create_order():
    d = request.json
    db = get_db()

    product_id = d.get('product_id')
    product_name = d.get('product_name', '')

    # Nếu chọn sản phẩm → lấy tên + trừ stock
    if product_id:
        prod = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
        if prod:
            product_name = prod['name']
            if prod['stock'] <= 0:
                db.close()
                return jsonify({"success": False, "error": "Sản phẩm đã hết hàng"}), 400
            db.execute("UPDATE products SET stock = stock - 1, updated_at=? WHERE id=?",
                       (datetime.now().isoformat(), product_id))

    db.execute(
        """INSERT INTO orders (customer_id, product_id, product_name, amount, status, payment_method, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (d['customer_id'], product_id, product_name, d.get('amount', 0),
         d.get('status', 'pending'), d.get('payment_method', 'bank_transfer'), d.get('notes', ''))
    )
    db.commit()
    
    # Lấy email khách hàng để gửi
    cust = db.execute("SELECT email FROM customers WHERE id=?", (d['customer_id'],)).fetchone()
    if cust and cust['email']:
        trigger_order_email(cust['email'], product_name, d.get('amount', 0))
        
    db.close()
    return jsonify({"success": True}), 201


@app.route('/api/orders/<int:oid>', methods=['PUT'])
def update_order(oid):
    d = request.json
    db = get_db()

    # Nếu đổi sản phẩm → hoàn stock cũ, trừ stock mới
    old = db.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone()
    if old:
        new_pid = d.get('product_id')
        old_pid = old['product_id']
        if new_pid != old_pid:
            if old_pid:
                db.execute("UPDATE products SET stock = stock + 1 WHERE id=?", (old_pid,))
            if new_pid:
                db.execute("UPDATE products SET stock = stock - 1 WHERE id=?", (new_pid,))

    product_name = d.get('product_name', '')
    if d.get('product_id'):
        prod = db.execute("SELECT name FROM products WHERE id=?", (d['product_id'],)).fetchone()
        if prod:
            product_name = prod['name']

    db.execute(
        """UPDATE orders SET customer_id=?, product_id=?, product_name=?, amount=?,
           status=?, payment_method=?, notes=?, updated_at=? WHERE id=?""",
        (d['customer_id'], d.get('product_id'), product_name, d.get('amount', 0),
         d.get('status', 'pending'), d.get('payment_method', 'bank_transfer'),
         d.get('notes', ''), datetime.now().isoformat(), oid)
    )
    db.commit()
    db.close()
    return jsonify({"success": True})


@app.route('/api/orders/<int:oid>', methods=['DELETE'])
def delete_order(oid):
    db = get_db()
    # Hoàn lại stock khi xóa đơn
    order = db.execute("SELECT product_id FROM orders WHERE id=?", (oid,)).fetchone()
    if order and order['product_id']:
        db.execute("UPDATE products SET stock = stock + 1 WHERE id=?", (order['product_id'],))
    db.execute("DELETE FROM orders WHERE id=?", (oid,))
    db.commit()
    db.close()
    return jsonify({"success": True})


# ========== STATS ==========
@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    products = db.execute("SELECT COUNT(*) as c FROM products").fetchone()['c']
    customers = db.execute("SELECT COUNT(*) as c FROM customers").fetchone()['c']
    orders = db.execute("SELECT COUNT(*) as c FROM orders").fetchone()['c']
    revenue = db.execute("SELECT COALESCE(SUM(amount),0) as s FROM orders WHERE status='paid'").fetchone()['s']
    pending = db.execute("SELECT COUNT(*) as c FROM orders WHERE status='pending'").fetchone()['c']
    db.close()
    return jsonify({
        "products": products,
        "customers": customers,
        "orders": orders,
        "revenue": revenue,
        "pending": pending
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    print("="*50)
    print("🚀 Thu Hồi Nợ PRO — Admin Server")
    print("="*50)
    print(f"📁 Database: {DB_PATH}")
    print(f"🌐 Website:  http://localhost:{port}")
    print(f"👤 Admin:    http://localhost:{port}/admin")
    print("="*50)
    app.run(debug=True, port=port)
