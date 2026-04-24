import sqlite3
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brain.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

mcp = FastMCP("ThuHoiNo_MCP", host="127.0.0.1", port=3001)

@mcp.tool()
def get_daily_summary(date: str = None) -> str:
    """
    Biến AI thành kế toán trưởng, tổng hợp báo cáo kinh doanh của ngày hôm nay.
    
    Args:
        date: Ngày cần báo cáo định dạng YYYY-MM-DD. Nếu không cung cấp, lấy ngày hôm nay.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
        
    db = get_db()
    
    try:
        new_customers_count = db.execute("SELECT COUNT(*) as c FROM customers WHERE DATE(registered_at) = ?", (date,)).fetchone()['c']
        
        orders = db.execute("SELECT status, COUNT(*) as c, SUM(amount) as s FROM orders WHERE DATE(ordered_at) = ? GROUP BY status", (date,)).fetchall()
        
        total_orders = sum(r['c'] for r in orders)
        revenue = sum((r['s'] or 0) for r in orders if r['status'] == 'paid')
        
        report = f"📊 Báo cáo kinh doanh ngày {date}:\n"
        report += f"- Khách hàng/leads mới: {new_customers_count}\n"
        report += f"- Đơn hàng mới: {total_orders} (Doanh thu đã thu: {revenue:,.0f} VNĐ)\n"
        
        if orders:
            report += "- Chi tiết trạng thái đơn:\n"
            for o in orders:
                report += f"  + {o['status'].upper()}: {o['c']} đơn ({(o['s'] or 0):,.0f} VNĐ)\n"
                
        return report
    except Exception as e:
        return f"Lỗi truy xuất báo cáo: {e}"
    finally:
        db.close()


@mcp.tool()
def search_customer_info(query: str) -> str:
    """
    Tra cứu thông tin và lịch sử đơn hàng của khách hàng bằng số điện thoại, email, hoặc tên.
    
    Args:
        query: Số điện thoại, email hoặc một phần tên khách hàng
    """
    db = get_db()
    
    try:
        search_term = f"%{query}%"
        customers = db.execute(
            "SELECT * FROM customers WHERE phone LIKE ? OR email LIKE ? OR name LIKE ?",
            (search_term, search_term, search_term)
        ).fetchall()
        
        if not customers:
             return f"Không tìm thấy khách hàng nào khớp với '{query}'."
             
        res = []
        for c in customers:
            c_info = f"👤 Tên: {c['name']} | SĐT: {c['phone']} | Email: {c['email'] or 'N/A'}\n"
            c_info += f"   Nguồn: {c['source']} | Đăng ký lúc: {c['registered_at']}\n"
            c_info += f"   Ghi chú Sale: {c['notes'] or 'Không có'}\n"
            
            orders = db.execute(
                 "SELECT product_name, amount, status, ordered_at FROM orders WHERE customer_id = ? ORDER BY id DESC",
                 (c['id'],)
            ).fetchall()
            
            if orders:
                c_info += "   [Lịch sử đơn hàng]\n"
                lifetime_value = 0
                for o in orders:
                     c_info += f"     - {o['ordered_at']}: {o['product_name']} ({o['amount']:,.0f} đ) - {o['status'].upper()}\n"
                     if o['status'] == 'paid':
                         lifetime_value += o['amount']
                c_info += f"   💰 Tổng LTV (Đã thanh toán): {lifetime_value:,.0f} VNĐ\n"
            else:
                c_info += "   🚫 Khách chưa có đơn hàng nào.\n"
                
            res.append(c_info)
            
        return "\n---\n".join(res)
    except Exception as e:
        return f"Lỗi truy xuất khách hàng: {e}"
    finally:
        db.close()


@mcp.tool()
def add_customer_note(phone: str, note_content: str) -> str:
    """
    Cập nhật ngay lập tức ghi chú / insights sau khi giao tiếp với khách hàng.
    
    Args:
        phone: Số điện thoại chính xác của khách hàng
        note_content: Nội dung thông tin bổ sung cần ghi chú lại
    """
    db = get_db()
    try:
        c = db.execute("SELECT id, name, notes FROM customers WHERE phone = ?", (phone,)).fetchone()
        
        if not c:
            return f"❌ Không tìm thấy khách hàng có số {phone}."
            
        old_notes = c['notes'] or ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_note = f"[{timestamp}]: {note_content}"
        
        updated_notes = old_notes + "\n" + new_note if old_notes.strip() else new_note
        
        db.execute("UPDATE customers SET notes = ? WHERE id = ?", (updated_notes, c['id']))
        db.commit()
        
        return f"✅ Đã cập nhật ghi chú thành công cho khách hàng: {c['name']} (SĐT: {phone})."
    except Exception as e:
        return f"Lỗi cập nhật ghi chú: {e}"
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run(transport="sse")
