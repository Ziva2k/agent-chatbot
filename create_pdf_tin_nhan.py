#!/usr/bin/env python3
"""
Tạo PDF: 15 Mẫu Tin Nhắn Đòi Nợ — Copy-Paste, Gửi Luôn, Không Sợ Mất Lòng
Brand voice: Gần gũi, thẳng thắn, câu ngắn, không corporate
"""

import os
from fpdf import FPDF

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '15_mau_tin_nhan_doi_no.pdf')

# Brand colors
ORANGE = (255, 107, 0)
DARK_BG = (15, 15, 15)
DARK_CARD = (25, 25, 25)
DARK_CARD2 = (30, 30, 30)
WHITE = (255, 255, 255)
LIGHT_GRAY = (192, 192, 192)
MUTED = (130, 130, 130)
GREEN = (74, 222, 128)
YELLOW = (251, 191, 36)
RED = (248, 113, 113)
LIGHT_ORANGE = (255, 154, 64)

FONT_REG = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


class PDFDoc(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('main', '', FONT_REG, uni=True)
        self.add_font('main', 'B', FONT_BOLD, uni=True)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_fill_color(*DARK_BG)
            self.rect(0, 0, 210, 12, 'F')
            self.set_font('main', '', 7)
            self.set_text_color(*MUTED)
            self.set_xy(10, 4)
            self.cell(0, 5, '15 Mẫu Tin Nhắn Đòi Nợ — Thu Hồi Nợ PRO', 0, 0, 'L')
            self.set_xy(0, 4)
            self.cell(200, 5, f'Trang {self.page_no()}', 0, 0, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('main', '', 7)
        self.set_text_color(*MUTED)
        self.cell(0, 5, 'Hotline: 089.843.7922  |  Zalo: Thu Hồi Nợ PRO  |  thuhoino.pro', 0, 0, 'C')

    def dark_page(self):
        self.set_fill_color(*DARK_BG)
        self.rect(0, 0, 210, 297, 'F')

    def section_title(self, icon, title, color=ORANGE):
        self.ln(6)
        self.set_fill_color(color[0], color[1], color[2])
        self.rect(10, self.get_y(), 3, 10, 'F')
        self.set_font('main', 'B', 16)
        self.set_text_color(*WHITE)
        self.set_x(18)
        self.cell(0, 10, f'{icon}  {title}', 0, 1, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def template_card(self, number, title, situation, message, tip=None):
        y_start = self.get_y()
        card_x = 14

        # Check if we need a new page
        if y_start > 225:
            self.add_page()
            self.dark_page()
            y_start = 20

        # Template number + title
        self.set_font('main', 'B', 11)
        self.set_text_color(*ORANGE)
        self.set_x(card_x)
        self.cell(0, 7, f'Mẫu #{number}', 0, 1)

        self.set_font('main', 'B', 13)
        self.set_text_color(*WHITE)
        self.set_x(card_x)
        self.multi_cell(175, 7, title)
        self.ln(1)

        # Situation
        self.set_font('main', '', 9)
        self.set_text_color(*MUTED)
        self.set_x(card_x)
        self.cell(0, 5, f'Tình huống:  {situation}', 0, 1)
        self.ln(3)

        # Message box
        box_x = 16
        msg_y = self.get_y()
        self.set_fill_color(28, 28, 28)

        # Draw left orange bar
        self.set_fill_color(*ORANGE)
        self.rect(box_x, msg_y, 2, 1, 'F')  # placeholder, will extend

        # Message content
        self.set_fill_color(22, 22, 22)
        self.set_font('main', '', 10.5)
        self.set_text_color(220, 220, 220)
        self.set_x(box_x + 6)
        prev_y = self.get_y()
        self.multi_cell(168, 6.5, message)
        msg_height = self.get_y() - prev_y

        # Draw orange bar at correct height
        self.set_fill_color(*ORANGE)
        self.rect(box_x, prev_y - 1, 2, msg_height + 2, 'F')

        self.ln(2)

        # Tip
        if tip:
            self.set_font('main', '', 8.5)
            self.set_text_color(*LIGHT_ORANGE)
            self.set_x(card_x)
            self.cell(0, 5, f'> Mẹo: {tip}', 0, 1)
            self.ln(1)

        # Separator line
        self.set_draw_color(40, 40, 40)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(6)


def build_pdf():
    pdf = PDFDoc()

    # ==================== COVER PAGE ====================
    pdf.add_page()
    pdf.dark_page()

    # Top accent line
    pdf.set_fill_color(*ORANGE)
    pdf.rect(0, 0, 210, 4, 'F')

    # Title area
    pdf.ln(45)
    pdf.set_font('main', 'B', 32)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 15, '15 Mẫu Tin Nhắn', 0, 1, 'C')

    pdf.set_font('main', 'B', 32)
    pdf.set_text_color(*ORANGE)
    pdf.cell(0, 15, 'Đòi Nợ', 0, 1, 'C')

    pdf.ln(4)
    pdf.set_font('main', '', 14)
    pdf.set_text_color(*LIGHT_GRAY)
    pdf.cell(0, 8, 'Copy — Paste — Gửi Luôn', 0, 1, 'C')
    pdf.cell(0, 8, 'Không Sợ Mất Lòng', 0, 1, 'C')

    # Decorative line
    pdf.ln(10)
    pdf.set_fill_color(*ORANGE)
    pdf.rect(80, pdf.get_y(), 50, 1.5, 'F')
    pdf.ln(12)

    # Subtitle
    pdf.set_font('main', '', 11)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 7, 'Từ nhắc nhẹ nhàng đến thông báo pháp lý —', 0, 1, 'C')
    pdf.cell(0, 7, 'đủ mọi tình huống, đúng luật, chuyên nghiệp.', 0, 1, 'C')

    pdf.ln(25)

    # Brand
    pdf.set_font('main', 'B', 14)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 8, 'THU HỒI NỢ PRO', 0, 1, 'C')
    pdf.set_font('main', '', 10)
    pdf.set_text_color(*ORANGE)
    pdf.cell(0, 7, 'Hotline: 089.843.7922', 0, 1, 'C')

    # Bottom accent
    pdf.set_fill_color(*ORANGE)
    pdf.rect(0, 293, 210, 4, 'F')

    # ==================== PAGE 2: GIỚI THIỆU ====================
    pdf.add_page()
    pdf.dark_page()
    pdf.ln(5)

    pdf.set_font('main', 'B', 20)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 12, 'Trước khi bắt đầu', 0, 1, 'C')
    pdf.ln(6)

    intro = """Chào bạn,

Bạn đang cầm file này, nghĩa là bạn đang bị ai đó nợ tiền. Và bạn không biết nhắn thế nào cho đúng — vừa đòi được tiền, vừa không mất lòng, vừa không vi phạm pháp luật.

Nói thẳng: đa số người bị nợ đều MẤT TIỀN không phải vì con nợ quịt — mà vì MÌNH KHÔNG BIẾT CÁCH ĐÒI.

Nhắn sai → con nợ block. Không nhắn → con nợ quên luôn. Nhắn quá hung → mình vi phạm luật.

File này giải quyết hết. 15 mẫu tin nhắn, chia theo 4 cấp độ, từ nhắc nhẹ đến thông báo pháp lý. Copy-paste là gửi được luôn. Thế thôi.

Lưu ý quan trọng:
• Luôn giữ bằng chứng (screenshot mọi tin nhắn)
• Không đe dọa, xúc phạm — đó là vi phạm pháp luật
• Gửi đúng thứ tự: nhẹ trước, nặng sau
• Mỗi lần nhắn cách nhau 3-5 ngày cho con nợ có thời gian phản hồi"""

    pdf.set_font('main', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.set_x(20)
    pdf.multi_cell(170, 7, intro)

    pdf.ln(8)
    pdf.set_font('main', 'B', 11)
    pdf.set_text_color(*ORANGE)
    pdf.cell(0, 7, '— Thu Hồi Nợ PRO', 0, 1, 'R')

    # ==================== NHÓM 1: NHẮC NHẸ NHÀNG ====================
    pdf.add_page()
    pdf.dark_page()
    pdf.ln(3)
    pdf.section_title('▶', 'NHÓM 1: NHẮC NHẸ NHÀNG (Lần 1-2)', GREEN)

    pdf.set_font('main', '', 9.5)
    pdf.set_text_color(*MUTED)
    pdf.set_x(14)
    pdf.multi_cell(180, 5.5, 'Dùng khi mới bắt đầu đòi. Giọng thân thiện, nhẹ nhàng. Mục tiêu: nhắc khéo, giữ mối quan hệ, cho con nợ cơ hội tự giác trả.')
    pdf.ln(4)

    # Mẫu 1
    pdf.template_card(
        1,
        'Nhắc lần đầu — Bạn bè / Người quen',
        'Cho bạn bè hoặc người quen vay, đã tới hạn trả.',
        'Ê [Tên] ơi, mình tiện nhắc khoản [số tiền] hôm [ngày cho vay] nha.\n\n'
        'Dạo này mình cũng cần xoay chút nên nhờ bạn sắp xếp khi nào tiện chuyển lại giúp mình nhé.\n\n'
        'Không gấp lắm, nhưng tuần này được thì tốt. Cảm ơn bạn!',
        'Nhắn nhẹ nhàng, không gây áp lực. Cho deadline mềm "tuần này" để con nợ có mốc thời gian.'
    )

    # Mẫu 2
    pdf.template_card(
        2,
        'Nhắc lần đầu — Đối tác / Kinh doanh',
        'Đối tác hoặc khách hàng chưa thanh toán theo hợp đồng.',
        'Chào anh/chị [Tên],\n\n'
        'Em gửi tin nhắn này để xác nhận lại khoản thanh toán [số tiền] theo [hợp đồng/đơn hàng số X], hạn thanh toán ngày [ngày].\n\n'
        'Anh/chị kiểm tra giúp em xem đã xử lý chưa ạ? Nếu có vướng mắc gì thì mình trao đổi thêm nha.\n\n'
        'Cảm ơn anh/chị! 😊',
        'Giọng lịch sự nhưng rõ ràng. Nêu đúng số tiền + mốc thời gian để con nợ không "quên".'
    )

    # Mẫu 3
    pdf.template_card(
        3,
        'Nhắc lần 2 — Kèm deadline cụ thể',
        'Đã nhắc 1 lần nhưng con nợ chưa phản hồi hoặc hứa nhưng chưa trả.',
        '[Tên] ơi, mình nhắc lại khoản [số tiền] nha.\n\n'
        'Lần trước mình có nhắn nhưng chắc bạn bận quên. Mình cũng hiểu.\n\n'
        'Nhưng mình cần bạn sắp xếp trước ngày [ngày cụ thể] giúp mình nhé. Khoản này mình cũng cần dùng.\n\n'
        'Bạn confirm giúp mình được không? 🙏',
        'Đưa deadline CỤ THỂ. Không nói "khi nào tiện" nữa — phải có ngày rõ ràng.'
    )

    # Mẫu 4
    pdf.template_card(
        4,
        'Nhắc khi gần hạn trả (hợp đồng/cam kết)',
        'Gần tới hạn cam kết trả nợ, nhắc trước 2-3 ngày.',
        'Chào anh/chị [Tên],\n\n'
        'Em nhắc nhẹ: khoản [số tiền] theo thỏa thuận sẽ đến hạn ngày [ngày].\n\n'
        'Anh/chị sắp xếp chuyển khoản đúng hạn giúp em nhé. Thông tin TK:\n'
        '• Ngân hàng: [Tên ngân hàng]\n'
        '• STK: [Số TK]\n'
        '• Nội dung CK: [Nội dung]\n\n'
        'Cảm ơn anh/chị ạ!',
        'Gửi sẵn thông tin chuyển khoản → giảm ma sát → con nợ dễ hành động hơn.'
    )

    # ==================== NHÓM 2: NHẮC NGHIÊM TÚC ====================
    pdf.add_page()
    pdf.dark_page()
    pdf.ln(3)
    pdf.section_title('🟡', 'NHÓM 2: NHẮC NGHIÊM TÚC (Lần 3-4)', YELLOW)

    pdf.set_font('main', '', 9.5)
    pdf.set_text_color(*MUTED)
    pdf.set_x(14)
    pdf.multi_cell(180, 5.5, 'Dùng khi đã nhắc 2 lần mà con nợ chưa trả hoặc liên tục "hứa lèo". Giọng rõ ràng, thẳng thắn, nêu hậu quả nhẹ. Vẫn lịch sự nhưng không nhân nhượng.')
    pdf.ln(4)

    # Mẫu 5
    pdf.template_card(
        5,
        'Nhắc nghiêm túc — Nêu hậu quả rõ ràng',
        'Đã nhắc 2 lần, con nợ im lặng hoặc hứa nhưng không trả.',
        '[Tên] ơi, mình đã nhắc 2 lần về khoản [số tiền] rồi.\n\n'
        'Mình tin bạn không cố tình, nhưng mình cũng cần bạn nghiêm túc về chuyện này.\n\n'
        'Nếu trong vòng [X ngày] bạn chưa sắp xếp được, mình sẽ phải tìm cách khác để xử lý. '
        'Mình không muốn, nhưng tiền của mình thì mình phải bảo vệ.\n\n'
        'Bạn reply giúp mình nhé.',
        'Không đe dọa cụ thể — chỉ nói "tìm cách khác". Để con nợ tự suy nghĩ.'
    )

    # Mẫu 6
    pdf.template_card(
        6,
        'Khi con nợ hứa rồi... nuốt lời',
        'Con nợ đã hứa trả vào ngày X nhưng qua ngày vẫn không thấy.',
        '[Tên] ơi, hôm [ngày con nợ hứa] bạn nói sẽ chuyển khoản [số tiền] cho mình.\n\n'
        'Hôm nay là [ngày hiện tại] rồi mà mình chưa nhận được.\n\n'
        'Nói thẳng nha: mình đã rất kiên nhẫn. Nhưng hứa mà không làm thì mình không biết tin bạn ở điểm nào.\n\n'
        'Bạn cho mình biết rõ ràng: bao giờ trả? Mình cần câu trả lời cụ thể, không phải "để xem".',
        'Nêu đúng ngày con nợ hứa → chứng minh mình có follow-up = con nợ khó chối.'
    )

    # Mẫu 7
    pdf.template_card(
        7,
        'Nhắc qua người trung gian',
        'Con nợ né tránh, không trả lời. Bạn nhờ người quen chung nhắn hộ.',
        'Chào [Tên người trung gian],\n\n'
        'Nhờ bạn/anh/chị một chuyện: mình có khoản [số tiền] cho [Tên con nợ] vay từ [ngày]. '
        'Mình đã nhắn mấy lần nhưng bạn ấy không phản hồi.\n\n'
        'Bạn/anh/chị tiện thì nhắc giúp mình nhé — mình chỉ cần bạn ấy liên lạc lại thôi, không cần phải trả ngay.\n\n'
        'Cảm ơn nhiều! 🙏',
        'Nhờ người trung gian tạo áp lực xã hội. Con nợ biết nhiều người biết → sẽ xử lý nhanh hơn.'
    )

    # Mẫu 8
    pdf.template_card(
        8,
        'Thông báo deadline CUỐI CÙNG trước khi leo thang',
        'Đây là tin nhắn cuối cùng ở cấp độ "nhắc nhẹ" trước khi chuyển sang pháp lý.',
        '[Tên],\n\n'
        'Mình nhắn lần cuối về khoản nợ [số tiền].\n\n'
        'Mình đã kiên nhẫn nhắc nhiều lần rồi. Đến thời điểm này, mình mong bạn hiểu: '
        'mình không thể chờ thêm được nữa.\n\n'
        'Deadline cuối: [ngày — cách 5-7 ngày].\n\n'
        'Sau ngày này nếu bạn không giải quyết, mình sẽ phải nhờ bên thứ ba hỗ trợ. '
        'Mình thành thật không muốn đến bước đó.\n\n'
        'Hy vọng bạn sẽ liên lạc lại.',
        'Đây là tin nhắn "cảnh cáo" cuối — nêu đúng deadline, nêu hậu quả "bên thứ ba".'
    )

    # ==================== NHÓM 3: THÔNG BÁO PHÁP LÝ ====================
    pdf.add_page()
    pdf.dark_page()
    pdf.ln(3)
    pdf.section_title('🔴', 'NHÓM 3: THÔNG BÁO PHÁP LÝ (Lần 5+)', RED)

    pdf.set_font('main', '', 9.5)
    pdf.set_text_color(*MUTED)
    pdf.set_x(14)
    pdf.multi_cell(180, 5.5, 'Dùng khi mọi cách nhắc nhở đều thất bại. Giọng trang trọng, nghiêm túc. Nêu rõ căn cứ pháp lý. QUAN TRỌNG: Tuyệt đối KHÔNG đe dọa — chỉ THÔNG BÁO quyền hợp pháp của mình.')
    pdf.ln(4)

    # Mẫu 9
    pdf.template_card(
        9,
        'Thông báo pháp lý chính thức (lần 1)',
        'Đã qua deadline cuối mà con nợ không liên lạc.',
        'Kính gửi anh/chị [Tên],\n\n'
        'Tôi gửi tin nhắn này để THÔNG BÁO CHÍNH THỨC về khoản nợ [số tiền] phát sinh từ ngày [ngày], '
        'đã quá hạn thanh toán.\n\n'
        'Tôi đã nhiều lần liên hệ nhưng không nhận được phản hồi. '
        'Theo quy định pháp luật, tôi có đầy đủ quyền hợp pháp để khởi kiện dân sự nhằm thu hồi khoản nợ này.\n\n'
        'Tôi đề nghị anh/chị liên hệ lại với tôi trước ngày [ngày] để thỏa thuận phương án thanh toán. '
        'Đây là thiện chí của tôi để hai bên giải quyết ổn thỏa.\n\n'
        'Trân trọng,\n'
        '[Họ tên đầy đủ]\n'
        '[SĐT]',
        'Chuyển sang dùng "tôi — anh/chị" trang trọng. Đây là bằng chứng pháp lý nên cần nghiêm túc.'
    )

    # Mẫu 10
    pdf.template_card(
        10,
        'Thông báo sẽ nhờ luật sư / đơn vị thu hồi nợ',
        'Con nợ vẫn không phản hồi sau thông báo pháp lý lần 1.',
        'Anh/chị [Tên],\n\n'
        'Tôi đã gửi thông báo về khoản nợ [số tiền] vào ngày [ngày gửi TB lần 1] nhưng chưa nhận được phản hồi.\n\n'
        'Do đó, tôi sẽ CHUYỂN HỒ SƠ sang đơn vị thu hồi nợ chuyên nghiệp / văn phòng luật sư để hỗ trợ giải quyết. '
        'Toàn bộ chi phí phát sinh sẽ do bên nợ chịu theo quy định.\n\n'
        'Đây là thông báo cuối cùng trước khi tôi chuyển hồ sơ.\n\n'
        'Nếu anh/chị muốn giải quyết trực tiếp, vui lòng liên hệ tôi trước ngày [ngày].\n\n'
        '[Họ tên]\n'
        '[SĐT]',
        'Nêu rõ: chi phí phát sinh sẽ do con nợ chịu → tạo thêm động lực trả sớm.'
    )

    # Mẫu 11
    pdf.template_card(
        11,
        'Thông báo quyết định khởi kiện dân sự',
        'Đã cảnh cáo nhiều lần, chuẩn bị nộp đơn khởi kiện.',
        'THÔNG BÁO\n\n'
        'Kính gửi: Anh/Chị [Họ tên đầy đủ con nợ]\n'
        'V/v: Khoản nợ [số tiền] phát sinh ngày [ngày]\n\n'
        'Do Anh/Chị không thực hiện nghĩa vụ thanh toán dù đã được thông báo nhiều lần, '
        'tôi thông báo sẽ nộp đơn khởi kiện tại Tòa án Nhân dân [Quận/Huyện] để yêu cầu:\n\n'
        '1. Thu hồi toàn bộ khoản nợ gốc: [số tiền]\n'
        '2. Lãi suất chậm trả theo quy định pháp luật\n'
        '3. Chi phí tố tụng và luật sư\n\n'
        'Anh/Chị có 07 (bảy) ngày kể từ ngày nhận thông báo này để liên hệ giải quyết.\n\n'
        '[Họ tên — Ngày tháng]',
        'Đây là mẫu chính thức. Screenshot lại làm bằng chứng. Nếu kiện thật thì nộp cùng hồ sơ.'
    )

    # Mẫu 12
    pdf.template_card(
        12,
        'Tin nhắn cuối cùng — "Last chance"',
        'Tin nhắn cuối cùng tuyệt đối trước khi giao hồ sơ cho luật sư.',
        '[Tên],\n\n'
        'Đây là tin nhắn cuối cùng tôi gửi cho anh/chị.\n\n'
        'Hồ sơ khoản nợ [số tiền] đã được chuẩn bị đầy đủ, bao gồm toàn bộ bằng chứng: '
        '[giấy vay / sao kê / tin nhắn xác nhận nợ].\n\n'
        'Nếu anh/chị không liên hệ trước [ngày, tháng, năm], hồ sơ sẽ được chuyển sang xử lý pháp lý. '
        'Sau đó mọi chi phí phát sinh sẽ không còn là vấn đề tôi thương lượng.\n\n'
        'Tôi hy vọng chúng ta giải quyết được ổn thỏa.\n\n'
        '[Họ tên — SĐT]',
        'Giọng bình tĩnh nhưng dứt khoát. Không hỏi ý kiến, chỉ THÔNG BÁO.'
    )

    # ==================== NHÓM 4: TÌNH HUỐNG ĐẶC BIỆT ====================
    pdf.add_page()
    pdf.dark_page()
    pdf.ln(3)
    pdf.section_title('🔧', 'NHÓM 4: TÌNH HUỐNG ĐẶC BIỆT', LIGHT_ORANGE)

    pdf.set_font('main', '', 9.5)
    pdf.set_text_color(*MUTED)
    pdf.set_x(14)
    pdf.multi_cell(180, 5.5, 'Những tình huống "khó nhằn" mà bạn chắc chắn sẽ gặp. Mỗi mẫu kèm cách xử lý cụ thể.')
    pdf.ln(4)

    # Mẫu 13
    pdf.template_card(
        13,
        'Con nợ chặn số / đổi SĐT / biến mất',
        'Không liên lạc được qua mọi kênh.',
        '*Gửi qua kênh khác (SMS, email, Facebook, hoặc nhờ người quen chuyển):*\n\n'
        'Anh/chị [Tên],\n\n'
        'Tôi đã cố liên hệ nhiều lần qua [Zalo/điện thoại] nhưng không được.\n\n'
        'Tôi thông báo: Việc tránh liên lạc KHÔNG làm mất nghĩa vụ trả nợ. '
        'Tôi vẫn có đầy đủ bằng chứng pháp lý và sẽ tiếp tục xử lý theo quy trình.\n\n'
        'Nếu anh/chị nhận được tin nhắn này, hãy liên hệ lại [SĐT] trước ngày [ngày].\n\n'
        'Đây là cơ hội để giải quyết nhẹ nhàng. Sau thời hạn này, tôi sẽ buộc phải giao cho bên thứ ba.\n\n'
        '[Họ tên]',
        'Gửi qua NHIỀU kênh cùng lúc: SMS, email, tài khoản khác. Screenshot tất cả.'
    )

    # Mẫu 14
    pdf.template_card(
        14,
        'Con nợ phủ nhận nợ / "Tao không vay"',
        'Con nợ chối bỏ khoản nợ mặc dù có bằng chứng.',
        '[Tên],\n\n'
        'Mình hiểu bạn nói không nhớ / không vay. Nhưng mình có đầy đủ bằng chứng:\n\n'
        '• [Sao kê chuyển khoản ngày X — Ngân hàng Y]\n'
        '• [Tin nhắn ngày X bạn xác nhận "tháng sau trả"]\n'
        '• [Giấy vay / người làm chứng — nếu có]\n\n'
        'Tất cả đều có giá trị pháp lý.\n\n'
        'Mình muốn giải quyết nhẹ nhàng giữa hai bên. Nhưng nếu bạn tiếp tục phủ nhận, '
        'mình sẽ phải để luật sư và tòa án quyết định.\n\n'
        'Bạn suy nghĩ và liên hệ lại mình nhé.',
        'LIỆT KÊ bằng chứng cụ thể → con nợ thấy không thể chối → dễ đồng ý trả.'
    )

    # Mẫu 15
    pdf.template_card(
        15,
        'Con nợ xin gia hạn / trả góp',
        'Con nợ muốn trả nhưng xin thêm thời gian hoặc trả từng phần.',
        '[Tên],\n\n'
        'Ok, mình đồng ý cho bạn trả góp. Nhưng lần này mình cần RÕ RÀNG:\n\n'
        '• Tổng nợ: [số tiền]\n'
        '• Đợt 1: [số tiền] — chuyển trước ngày [ngày]\n'
        '• Đợt 2: [số tiền] — chuyển trước ngày [ngày]\n'
        '• Đợt 3: [số tiền còn lại] — chuyển trước ngày [ngày]\n\n'
        'Bạn đồng ý thì REPLY "Đồng ý" vào tin nhắn này để mình có bằng chứng hai bên thỏa thuận.\n\n'
        'Nếu bạn trễ bất kỳ đợt nào mà không báo trước, mình sẽ xem như thỏa thuận bị phá vỡ và xử lý theo pháp luật.\n\n'
        'Hy vọng lần này mình giải quyết được dứt điểm nhé. 🤝',
        'BẮT BUỘC con nợ reply "Đồng ý" → tạo bằng chứng thỏa thuận mới có giá trị pháp lý.'
    )

    # ==================== TRANG CUỐI: LƯU Ý + CTA ====================
    pdf.add_page()
    pdf.dark_page()
    pdf.ln(10)

    pdf.set_font('main', 'B', 22)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 12, 'Gửi hết 15 mẫu mà', 0, 1, 'C')
    pdf.set_text_color(*ORANGE)
    pdf.cell(0, 12, 'vẫn không đòi được?', 0, 1, 'C')
    pdf.ln(8)

    pdf.set_font('main', '', 12)
    pdf.set_text_color(200, 200, 200)
    pdf.set_x(30)
    pdf.multi_cell(150, 7.5,
        'Nói thẳng nha: có những khoản nợ bạn KHÔNG THỂ tự xử lý được.\n\n'
        'Con nợ bỏ trốn, đổi số, tẩu tán tài sản, phủ nhận tất cả — '
        'lúc đó bạn cần người chuyên nghiệp.\n\n'
        'Bên mình — Thu Hồi Nợ PRO — đã xử lý 1000+ hồ sơ trong 10 năm, '
        'tổng thu hồi 500 tỷ+. Cam kết 100%: không thu hồi được thì không mất phí.',
        align='C'
    )

    pdf.ln(10)
    pdf.set_fill_color(*ORANGE)
    pdf.rect(50, pdf.get_y(), 110, 18, 'F')
    pdf.set_font('main', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 18, 'GỌI NGAY: 089.843.7922', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('main', '', 12)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 8, 'Hoặc nhắn Zalo để được tư vấn MIỄN PHÍ', 0, 1, 'C')
    pdf.cell(0, 8, 'zalo.me/0898437922', 0, 1, 'C')

    pdf.ln(15)
    # Final tagline
    pdf.set_font('main', '', 10)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 7, 'Tư vấn: Miễn phí', 0, 1, 'C')
    pdf.cell(0, 7, 'Đánh giá hồ sơ: Miễn phí', 0, 1, 'C')
    pdf.cell(0, 7, 'Không thu hồi được: Không mất phí', 0, 1, 'C')

    pdf.ln(6)
    pdf.set_font('main', 'B', 11)
    pdf.set_text_color(*ORANGE)
    pdf.cell(0, 7, 'Mất 15-30% hay mất 100%? Thế thôi.', 0, 1, 'C')

    # Bottom accent
    pdf.set_fill_color(*ORANGE)
    pdf.rect(0, 293, 210, 4, 'F')

    # ==================== SAVE ====================
    pdf.output(OUTPUT)
    print(f'✅ Đã tạo PDF thành công!')
    print(f'📄 File: {OUTPUT}')
    print(f'📑 Tổng số trang: {pdf.page_no()}')


if __name__ == '__main__':
    build_pdf()
