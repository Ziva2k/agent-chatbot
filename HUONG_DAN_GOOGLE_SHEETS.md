# 📋 HƯỚNG DẪN KẾT NỐI GOOGLE SHEETS ĐỂ LƯU DATA KHÁCH HÀNG

## Vì sao cần Google Sheets?

Hiện tại form đang dùng **localStorage** — nó chỉ lưu data trong trình duyệt của người gửi.
Nghĩa là khi khách hàng A điền form trên điện thoại của họ, data chỉ nằm trong điện thoại *của họ*, bạn không xem được.

**Google Sheets** sẽ giải quyết vấn đề này — mọi data khách hàng sẽ tự động gửi vào 1 bảng tính Google của bạn, bạn mở xem được từ bất kỳ đâu.

---

## Hướng dẫn từng bước (5 phút)

### Bước 1: Tạo Google Sheet

1. Vào **[Google Sheets](https://sheets.google.com)** → bấm **"+ Trang tính trống"**
2. Đặt tên: `Data Khách Hàng - Thu Hồi Nợ`
3. Ở hàng đầu tiên (row 1), nhập tiêu đề các cột:
   - Ô A1: `Thời gian`
   - Ô B1: `Họ và tên`
   - Ô C1: `Số điện thoại`
   - Ô D1: `Số tiền`
   - Ô E1: `Ghi chú`
   - Ô F1: `Nguồn`

### Bước 2: Mở Script Editor

1. Trong Google Sheet vừa tạo, vào menu **Tiện ích mở rộng** (Extensions) → **Apps Script**
2. Xóa toàn bộ code mặc định trong editor
3. Copy và paste đoạn code dưới đây vào:

```javascript
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    var fullName = e.parameter.fullName || '';
    var phone = e.parameter.phone || '';
    var debtAmount = e.parameter.debtAmount || '';
    var debtNote = e.parameter.debtNote || '';
    var createdAt = e.parameter.createdAt || new Date().toLocaleString('vi-VN');
    var source = e.parameter.source || '';
    
    sheet.appendRow([createdAt, fullName, phone, debtAmount, debtNote, source]);
    
    return ContentService
      .createTextOutput(JSON.stringify({status: 'success'}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({status: 'error', message: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput('Form receiver is working!')
    .setMimeType(ContentService.MimeType.TEXT);
}
```

4. Bấm **💾 Lưu** (hoặc Ctrl+S)
5. Đặt tên project: `FormReceiver`

### Bước 3: Triển khai (Deploy)

1. Bấm nút **Triển khai** (Deploy) → **Triển khai mới** (New deployment)
2. Bấm ⚙️ biểu tượng bánh răng bên cạnh "Chọn loại" → chọn **Ứng dụng web** (Web app)
3. Cấu hình:
   - **Mô tả**: `Form Receiver`
   - **Thực thi với tư cách**: `Tôi` (Me)
   - **Ai có quyền truy cập**: `Bất kỳ ai` (Anyone)
4. Bấm **Triển khai** (Deploy)
5. Google sẽ yêu cầu quyền → bấm **Ủy quyền** (Authorize) → chọn tài khoản Google → bấm **Cho phép** (Allow)
   
   > ⚠️ Nếu thấy cảnh báo "Google hasn't verified this app", bấm **Advanced** → **Go to FormReceiver (unsafe)** → **Allow**

6. **Copy URL** xuất hiện sau khi deploy (dạng: `https://script.google.com/macros/s/ABC.../exec`)

### Bước 4: Dán URL vào website

1. Mở file **`script.js`** trong thư mục WED
2. Tìm dòng:
   ```javascript
   const GOOGLE_SHEETS_URL = '';
   ```
3. Dán URL vào giữa 2 dấu nháy đơn:
   ```javascript
   const GOOGLE_SHEETS_URL = 'https://script.google.com/macros/s/ABC.../exec';
   ```
4. Lưu file

### Bước 5: Test thử

1. Mở trang web của bạn
2. Điền form test và bấm gửi
3. Mở Google Sheet → data sẽ xuất hiện!

---

## ❓ Câu hỏi thường gặp

**Q: Data cũ trong admin.html có mất không?**
A: admin.html vẫn hoạt động bình thường cho data localStorage. Nhưng Google Sheets mới là nơi lưu chính.

**Q: Nếu gửi Google Sheets bị lỗi thì sao?**
A: Data vẫn được lưu vào localStorage như backup. Bạn vẫn có thể xem trong admin.html (cùng trình duyệt).

**Q: Google Sheets có giới hạn không?**
A: Miễn phí, tối đa 10 triệu ô dữ liệu — đủ cho hàng trăm nghìn khách hàng.

**Q: Tôi có thể xem data trên điện thoại không?**
A: Có! Dùng app Google Sheets trên điện thoại, data cập nhật realtime.
