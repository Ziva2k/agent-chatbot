# Hướng Dẫn Deploy Lên VPS Ubuntu

## 1. Cài đặt môi trường trên VPS
Trước khi chạy server, hãy đảm bảo VPS của bạn đã cài đặt Python 3, pip và các thư viện cần thiết:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

Trong thư mục dự án trên VPS, thiết lập môi trường ảo và cài đặt thư viện:
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors resend python-dotenv gunicorn
```

## 2. Variables (Biến môi trường)
Mã nguồn giờ đã được cấu hình đọc các biến bảo mật từ file `.env`. Trên VPS, tạo file `.env` chung một thư mục với `server.py` chứa nội dung sau:
```env
RESEND_API_KEY=re_hqRqg7n5_48jSjptkF6vGggTZzmHRp8fJ
PORT=3000
```
> **Lưu ý:** Tuyệt đối không chia sẻ file `.env` và nó đã được cấu hình loại trừ khỏi git (trong `.gitignore`).

## 3. Khởi Dạy Server (Chạy ở Production)
Thay vì sử dụng `app.run` của Flask (vốn phù hợp cho Development), tại Production ta sẽ sử dụng Gunicorn để hoạt động ổn định:
```bash
# Thử nghiệm chạy bằng Gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 server:app
```
*(Nếu muốn chạy nền liên tục (background) hoặc thiết lập tự động chạy lại khi server khởi động lại trơn, nên cấu hình systemd).*

Server sẽ lắng nghe trên cổng **3000**. Mọi request từ Nginx có thể được proxy về cổng này.
