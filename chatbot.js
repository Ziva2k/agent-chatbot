/* ============================================
   THU HỒI NỢ PRO — Chatbot Widget
   Kịch bản từ sales_script.md
   ============================================ */

(() => {
    // === CONFIG ===
    const ZALO_URL = 'https://chat.zalo.me/?phone=0898437922';
    const FORM_SECTION = '#register';
    const BOT_NAME = 'Thu Hồi Nợ PRO';
    const BOT_AVATAR = '⚡';
    const TYPING_DELAY = 800;
    const MESSAGE_DELAY = 400;

    // === KNOWLEDGE BASE — from sales_script.md ===
    const GREETING = `Chào anh/chị! 👋\n\nEm là tư vấn viên bên <strong>Thu Hồi Nợ PRO</strong>. Anh/chị đang gặp vấn đề về khoản nợ khó đòi đúng không ạ?\n\nAnh/chị cứ chọn câu hỏi bên dưới hoặc nhắn trực tiếp — em tư vấn <strong>miễn phí</strong>, không ràng buộc gì hết 😊`;

    const QUICK_REPLIES = [
        { label: '💰 Phí dịch vụ?', key: 'phi' },
        { label: '📋 Cần giấy tờ gì?', key: 'giayto' },
        { label: '⏱️ Mất bao lâu?', key: 'thoigian' },
        { label: '🔒 Có hợp pháp không?', key: 'hopphap' },
        { label: '🔍 Con nợ trốn rồi?', key: 'contron' },
        { label: '📄 Không có giấy tờ?', key: 'khonggiayto' },
        { label: '🤫 Sợ lộ thông tin?', key: 'baomat' },
        { label: '📏 Nợ nhỏ quá?', key: 'nonho' },
        { label: '📅 Nợ lâu năm?', key: 'launam' },
        { label: '🔄 Quy trình thế nào?', key: 'quytrinh' },
    ];

    const RESPONSES = {
        phi: {
            text: `Phí dao động <strong>15% – 30%</strong> trên số tiền bên em thu hồi được cho anh/chị.\n\nNhưng điểm quan trọng nhất: <strong>không thu được thì không lấy phí</strong>. Anh/chị không mất gì cả.\n\nNói thẳng ra: mất 15-30% hay mất 100%? Thế thôi 😊\n\nAnh/chị muốn em đánh giá trường hợp cụ thể không ạ?`,
            followUp: [
                { label: '✅ Muốn tư vấn cụ thể', key: '_interested' },
                { label: '📋 Cần giấy tờ gì?', key: 'giayto' },
                { label: '🔄 Quy trình thế nào?', key: 'quytrinh' },
            ]
        },
        hopphap: {
            text: `Em hiểu lo lắng này. Nhiều người cũng hỏi vậy vì ngoài kia có mấy bên làm ẩu.\n\nCòn bên em thì <strong>100% hợp pháp</strong>: đàm phán chuyên nghiệp, gửi thông báo pháp lý từ văn phòng luật sư, khởi kiện dân sự nếu cần.\n\nTrước khi bắt đầu, bên em ký <strong>NDA bảo mật</strong> luôn — thông tin anh/chị được bảo vệ tuyệt đối.\n\nBên em đã xử lý <strong>1000+ hồ sơ</strong> trong 10 năm rồi, anh/chị yên tâm ạ.`,
            followUp: [
                { label: '✅ Tôi muốn bắt đầu', key: '_interested' },
                { label: '💰 Phí bao nhiêu?', key: 'phi' },
                { label: '🤫 Bảo mật thế nào?', key: 'baomat' },
            ]
        },
        giayto: {
            text: `Đơn giản thôi! Anh/chị có cái nào thì gửi cái đó:\n\n✅ Giấy vay / cam kết nợ\n✅ Sao kê chuyển khoản\n✅ Tin nhắn Zalo/Messenger xác nhận nợ\n✅ Email trao đổi\n✅ Hợp đồng (nếu có)\n\n<strong>Chỉ cần 1 trong mấy cái trên</strong> là bên em đánh giá được rồi. Có khách chỉ có tin nhắn Zalo mà bên em vẫn thu hồi 350 triệu đó.\n\nAnh/chị chụp gửi em xem thử?`,
            followUp: [
                { label: '✅ Gửi hồ sơ ngay', key: '_interested' },
                { label: '📄 Không có giấy tờ?', key: 'khonggiayto' },
                { label: '⏱️ Mất bao lâu?', key: 'thoigian' },
            ]
        },
        thoigian: {
            text: `Nhanh hay chậm tùy mức độ phức tạp:\n\n🟢 Nợ đơn giản: <strong>1 – 3 tuần</strong>\n🟡 Con nợ né tránh: <strong>1 – 2 tháng</strong>\n🔴 Nợ lâu năm, con nợ biến mất: <strong>2 – 3 tháng</strong>\n\nBên em phản hồi <strong>trong 30 phút</strong> sau khi nhận thông tin và bắt đầu xử lý ngay trong ngày.\n\nTrường hợp gấp thì ưu tiên. Anh/chị cần gấp trong bao lâu ạ?`,
            followUp: [
                { label: '🔥 Rất gấp, bắt đầu ngay', key: '_interested' },
                { label: '💰 Phí bao nhiêu?', key: 'phi' },
                { label: '🔄 Quy trình thế nào?', key: 'quytrinh' },
            ]
        },
        khonggiayto: {
            text: `Vẫn có cách! Anh/chị kiểm tra lại xem có mấy thứ này không:\n\n• Tin nhắn Zalo/Messenger đề cập đến khoản vay?\n• Sao kê chuyển khoản ngân hàng?\n• Có ai làm chứng lúc cho vay không?\n\nMấy cái đó đều có <strong>giá trị pháp lý</strong> hết. Bên em sẽ đánh giá miễn phí trước — xem xong anh/chị mới quyết định.\n\nGửi em xem tình huống cụ thể nha?`,
            followUp: [
                { label: '✅ Gửi thông tin ngay', key: '_interested' },
                { label: '⏱️ Mất bao lâu?', key: 'thoigian' },
                { label: '💰 Phí bao nhiêu?', key: 'phi' },
            ]
        },
        contron: {
            text: `Đây là thứ bên em làm <strong>nhiều nhất</strong> luôn 💪\n\nBên em có đội ngũ chuyên truy tìm:\n• Xác minh nơi ở mới\n• Kiểm tra tài sản, tài khoản\n• Mạng lưới liên kết hỗ trợ\n\nMột khách bên em — anh H., chủ doanh nghiệp xây dựng — đối tác bỏ trốn với 2 tỷ. Bên em tìm ra và thu hồi được <strong>toàn bộ chỉ sau 2 tháng</strong>.\n\nAnh/chị gửi em thông tin con nợ, để em xem khả năng xử lý nha!`,
            followUp: [
                { label: '✅ Gửi thông tin ngay', key: '_interested' },
                { label: '🤫 Bảo mật thế nào?', key: 'baomat' },
                { label: '💰 Phí bao nhiêu?', key: 'phi' },
            ]
        },
        baomat: {
            text: `Hiểu anh/chị. Bảo mật là thứ bên em <strong>đặt lên đầu</strong>.\n\nQuy trình cụ thể:\n• Ký <strong>NDA</strong> trước khi tiếp nhận\n• Thông tin chỉ nội bộ đội xử lý biết\n• Con nợ nhận thông báo từ <strong>văn phòng luật sư</strong>, không liên quan trực tiếp đến anh/chị\n\nCó chị L. — chủ chuỗi quán cà phê — rất lo thương hiệu bị ảnh hưởng. Bên em xử lý kín đáo, thu hồi 1.2 tỷ mà không ai biết.\n\nAnh/chị yên tâm ạ!`,
            followUp: [
                { label: '✅ Tôi yên tâm rồi, bắt đầu', key: '_interested' },
                { label: '📋 Cần giấy tờ gì?', key: 'giayto' },
                { label: '🔄 Quy trình thế nào?', key: 'quytrinh' },
            ]
        },
        nonho: {
            text: `Anh/chị ơi, không có khoản nợ nào nhỏ cả. Tiền của mình mà 😄\n\nMà quan trọng là: <strong>không thu hồi thì không mất phí</strong> — anh/chị không rủi ro gì.\n\nCó anh K. — freelancer — bị nợ 85 triệu. Bên em xử lý <strong>10 ngày</strong> là xong. Nhanh gọn.\n\nAnh/chị cứ gửi thông tin, em đánh giá miễn phí trước nha!`,
            followUp: [
                { label: '✅ Gửi thông tin', key: '_interested' },
                { label: '💰 Phí bao nhiêu?', key: 'phi' },
                { label: '⏱️ Mất bao lâu?', key: 'thoigian' },
            ]
        },
        launam: {
            text: `Chưa chắc hết hạn đâu! Thời hiệu khởi kiện có thể <strong>tính lại</strong> nếu con nợ có thừa nhận nợ gần đây (tin nhắn, gặp mặt, qua người khác...).\n\nMà ngoài khởi kiện, bên em còn có phương pháp <strong>đàm phán</strong> — không cần ra tòa mà vẫn thu hồi được.\n\n10 năm làm nghề, bên em xử lý nhiều vụ nợ lâu năm rồi. Để em xem hồ sơ anh/chị trước nha!`,
            followUp: [
                { label: '✅ Gửi hồ sơ ngay', key: '_interested' },
                { label: '📋 Cần chuẩn bị gì?', key: 'giayto' },
                { label: '🔒 Có hợp pháp không?', key: 'hopphap' },
            ]
        },
        quytrinh: {
            text: `Đơn giản, 4 bước:\n\n<strong>Bước 1:</strong> Anh/chị gửi hồ sơ → Em kiểm tra tính pháp lý\n<strong>Bước 2:</strong> Bên em xác minh con nợ — tài chính, nơi ở thực tế\n<strong>Bước 3:</strong> Triển khai — đàm phán trực tiếp hoặc gửi thông báo pháp lý từ luật sư\n<strong>Bước 4:</strong> Thu tiền → bàn giao cho anh/chị. Nhanh gọn, minh bạch.\n\nToàn bộ quy trình bên em <strong>cập nhật liên tục</strong> cho anh/chị biết, không để mù thông tin.\n\nAnh/chị muốn bắt đầu bước 1 ngay không ạ?`,
            followUp: [
                { label: '✅ Bắt đầu ngay!', key: '_interested' },
                { label: '💰 Phí bao nhiêu?', key: 'phi' },
                { label: '📋 Cần chuẩn bị gì?', key: 'giayto' },
            ]
        },
        _interested: {
            text: `Tuyệt vời! 🔥\n\nĐể bắt đầu, anh/chị <strong>điền nhanh form bên dưới</strong> — chỉ mất 30 giây:\n\n✅ Tư vấn: miễn phí\n✅ Đánh giá hồ sơ: miễn phí\n✅ Không thu hồi được: không mất phí\n\nAnh/chị chỉ trả khi tiền thật sự về tay mình. Thế thôi 😊`,
            followUp: [],
            showCTA: true
        },
        _fallback: {
            text: `Cảm ơn anh/chị đã chia sẻ! Em ghi nhận rồi.\n\nĐể tư vấn chính xác nhất, anh/chị có thể:\n\n👉 Chọn câu hỏi bên dưới để em trả lời nhanh\n👉 Hoặc <strong>để lại thông tin</strong> qua form, bên em sẽ gọi lại tư vấn chi tiết ạ`,
            followUp: [
                { label: '💰 Phí dịch vụ?', key: 'phi' },
                { label: '🔄 Quy trình?', key: 'quytrinh' },
                { label: '✅ Để lại thông tin', key: '_interested' },
            ],
            showFormHint: true
        },
        _notready: {
            text: `Dạ, anh/chị cứ suy nghĩ ạ. Không vội!\n\nNhưng để tiện hơn, anh/chị <strong>điền nhanh form</strong> giúp em — em sẽ gửi <strong>tài liệu quy trình bảo mật + bảng phí chi tiết</strong> qua Zalo cho anh/chị xem thêm.\n\nThông tin hoàn toàn <strong>bảo mật</strong>, em chỉ dùng để gửi tài liệu thôi ạ 🔒`,
            followUp: [],
            showCTA: true
        }
    };

    // === KEYWORD MATCHING ===
    const KEYWORD_MAP = [
        { keywords: ['phí', 'phi', 'giá', 'gia', 'bao nhiêu', 'bao nhieu', 'chi phí', 'chi phi', 'tiền', 'tien', 'mắc', 'mac', 'đắt', 'dat', 'rẻ', 're', 'cost', 'price'], key: 'phi' },
        { keywords: ['hợp pháp', 'hop phap', 'bất hợp pháp', 'bat hop phap', 'trái luật', 'trai luat', 'pháp luật', 'phap luat', 'xã hội đen', 'xa hoi den', 'đe dọa', 'de doa', 'uy hiếp', 'uy hiep', 'legal'], key: 'hopphap' },
        { keywords: ['giấy tờ', 'giay to', 'chuẩn bị', 'chuan bi', 'hồ sơ', 'ho so', 'chứng từ', 'chung tu', 'cần gì', 'can gi', 'document'], key: 'giayto' },
        { keywords: ['bao lâu', 'bao lau', 'mất bao lâu', 'mat bao lau', 'thời gian', 'thoi gian', 'nhanh', 'chậm', 'cham', 'gấp', 'gap', 'lâu', 'lau', 'tuần', 'tuan', 'tháng', 'thang', 'how long'], key: 'thoigian' },
        { keywords: ['không có giấy', 'khong co giay', 'không giấy', 'khong giay', 'vay miệng', 'vay mieng', 'no miệng', 'no mieng', 'no docs', 'không chứng cứ', 'khong chung cu'], key: 'khonggiayto' },
        { keywords: ['trốn', 'tron', 'bỏ trốn', 'bo tron', 'biến mất', 'bien mat', 'mất tích', 'mat tich', 'bốc hơi', 'boc hoi', 'đổi số', 'doi so', 'chặn', 'chan', 'khóa máy', 'khoa may', 'missing'], key: 'contron' },
        { keywords: ['bảo mật', 'bao mat', 'lộ', 'lo thong tin', 'bí mật', 'bi mat', 'kín', 'kin', 'nda', 'uy tín', 'uy tin', 'danh dự', 'danh du', 'secret', 'privacy'], key: 'baomat' },
        { keywords: ['nhỏ', 'nho', 'ít', 'it', 'không đáng', 'khong dang', 'vài chục', 'vai chuc', 'dưới 100', 'duoi 100', 'small'], key: 'nonho' },
        { keywords: ['lâu năm', 'lau nam', 'lâu rồi', 'lau roi', 'mấy năm', 'may nam', 'hết hạn', 'het han', 'thời hiệu', 'thoi hieu', 'quá lâu', 'qua lau', 'old debt'], key: 'launam' },
        { keywords: ['quy trình', 'quy trinh', 'thế nào', 'the nao', 'như nào', 'nhu nao', 'cách', 'cach', 'bước', 'buoc', 'làm sao', 'lam sao', 'process', 'how'], key: 'quytrinh' },
        { keywords: ['muốn', 'muon', 'bắt đầu', 'bat dau', 'đăng ký', 'dang ky', 'tư vấn', 'tu van', 'liên hệ', 'lien he', 'gửi', 'gui', 'nhờ', 'nho', 'giúp', 'giup', 'cần', 'can', 'register', 'start'], key: '_interested' },
        { keywords: ['suy nghĩ', 'suy nghi', 'chưa', 'chua', 'để sau', 'de sau', 'chưa quyết', 'chua quyet', 'hỏi thăm', 'hoi tham', 'tham khảo', 'tham khao', 'later'], key: '_notready' },
    ];

    function matchResponse(input) {
        const text = input.toLowerCase().trim();
        for (const entry of KEYWORD_MAP) {
            for (const kw of entry.keywords) {
                if (text.includes(kw)) {
                    return entry.key;
                }
            }
        }
        return '_fallback';
    }

    // === BUILD WIDGET HTML ===
    function createWidget() {
        const widget = document.createElement('div');
        widget.id = 'chatbotWidget';
        widget.innerHTML = `
            <!-- Chat Toggle Button -->
            <button class="cb-toggle" id="cbToggle" aria-label="Mở chatbot tư vấn">
                <span class="cb-toggle-icon cb-toggle-icon--chat">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                    </svg>
                </span>
                <span class="cb-toggle-icon cb-toggle-icon--close">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </span>
                <span class="cb-badge" id="cbBadge">1</span>
            </button>

            <!-- Chat Window -->
            <div class="cb-window" id="cbWindow">
                <div class="cb-header">
                    <div class="cb-header-left">
                        <div class="cb-avatar">${BOT_AVATAR}</div>
                        <div class="cb-header-info">
                            <div class="cb-header-name">${BOT_NAME}</div>
                            <div class="cb-header-status">
                                <span class="cb-status-dot"></span>
                                Online — Phản hồi trong 30 phút
                            </div>
                        </div>
                    </div>
                    <button class="cb-close" id="cbClose" aria-label="Đóng chat">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                <div class="cb-messages" id="cbMessages"></div>
                <div class="cb-input-area">
                    <input type="text" class="cb-input" id="cbInput" placeholder="Nhập câu hỏi..." autocomplete="off">
                    <button class="cb-send" id="cbSend" aria-label="Gửi">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(widget);
    }

    // === DOM HELPERS ===
    function $(id) { return document.getElementById(id); }

    function scrollToBottom() {
        const msgs = $('cbMessages');
        requestAnimationFrame(() => {
            msgs.scrollTop = msgs.scrollHeight;
        });
    }

    // === MESSAGE RENDERING ===
    function addBotMessage(html, options = {}) {
        const msgs = $('cbMessages');

        // Show typing indicator
        const typing = document.createElement('div');
        typing.className = 'cb-msg cb-msg--bot cb-typing-msg';
        typing.innerHTML = `
            <div class="cb-msg-avatar">${BOT_AVATAR}</div>
            <div class="cb-msg-bubble">
                <div class="cb-typing">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        msgs.appendChild(typing);
        scrollToBottom();

        return new Promise(resolve => {
            setTimeout(() => {
                // Remove typing
                typing.remove();

                // Add actual message
                const msg = document.createElement('div');
                msg.className = 'cb-msg cb-msg--bot cb-msg--animate';
                msg.innerHTML = `
                    <div class="cb-msg-avatar">${BOT_AVATAR}</div>
                    <div class="cb-msg-bubble">${html.replace(/\n/g, '<br>')}</div>
                `;
                msgs.appendChild(msg);

                // Add CTA buttons if needed
                if (options.showCTA) {
                    setTimeout(() => {
                        addCTAButtons();
                        scrollToBottom();
                    }, MESSAGE_DELAY);
                }

                // Add follow-up quick replies
                if (options.followUp && options.followUp.length > 0) {
                    setTimeout(() => {
                        addQuickReplies(options.followUp);
                        scrollToBottom();
                    }, MESSAGE_DELAY);
                }

                scrollToBottom();
                resolve();
            }, TYPING_DELAY);
        });
    }

    function addUserMessage(text) {
        const msgs = $('cbMessages');
        const msg = document.createElement('div');
        msg.className = 'cb-msg cb-msg--user cb-msg--animate';
        msg.innerHTML = `<div class="cb-msg-bubble">${escapeHtml(text)}</div>`;
        msgs.appendChild(msg);
        scrollToBottom();
    }

    function addQuickReplies(replies) {
        const msgs = $('cbMessages');

        // Remove any existing quick replies
        msgs.querySelectorAll('.cb-quick-replies').forEach(el => el.remove());

        const wrap = document.createElement('div');
        wrap.className = 'cb-quick-replies cb-msg--animate';

        replies.forEach(r => {
            const btn = document.createElement('button');
            btn.className = 'cb-quick-btn';
            btn.textContent = r.label;
            btn.addEventListener('click', () => {
                // Remove this quick reply set
                wrap.remove();
                handleQuickReply(r);
            });
            wrap.appendChild(btn);
        });

        msgs.appendChild(wrap);
        scrollToBottom();
    }

    function addCTAButtons() {
        const msgs = $('cbMessages');
        const wrap = document.createElement('div');
        wrap.className = 'cb-cta-wrap cb-msg--animate';
        wrap.innerHTML = `
            <a href="${FORM_SECTION}" class="cb-cta-btn cb-cta-btn--primary" onclick="document.getElementById('cbToggle').click()">
                📋 Điền Form Tư Vấn Ngay
            </a>
            <a href="${ZALO_URL}" class="cb-cta-btn cb-cta-btn--zalo" target="_blank" rel="noopener noreferrer">
                💬 Nhắn Zalo Trực Tiếp
            </a>
        `;
        msgs.appendChild(wrap);
        scrollToBottom();
    }

    function showInitialQuickReplies() {
        addQuickReplies(QUICK_REPLIES);
    }

    // === HANDLERS ===
    function handleQuickReply(reply) {
        addUserMessage(reply.label);
        const resp = RESPONSES[reply.key];
        if (resp) {
            addBotMessage(resp.text, {
                followUp: resp.followUp,
                showCTA: resp.showCTA
            });
        }
    }

    function handleUserInput() {
        const input = $('cbInput');
        const text = input.value.trim();
        if (!text) return;

        input.value = '';
        addUserMessage(text);

        const key = matchResponse(text);
        const resp = RESPONSES[key];
        if (resp) {
            addBotMessage(resp.text, {
                followUp: resp.followUp,
                showCTA: resp.showCTA,
                showFormHint: resp.showFormHint
            });
        }
    }

    // === INIT ===
    function init() {
        createWidget();

        const toggle = $('cbToggle');
        const window_ = $('cbWindow');
        const close = $('cbClose');
        const input = $('cbInput');
        const send = $('cbSend');
        const badge = $('cbBadge');
        let isOpen = false;
        let hasGreeted = false;

        function openChat() {
            isOpen = true;
            toggle.classList.add('cb-toggle--open');
            window_.classList.add('cb-window--open');
            badge.style.display = 'none';

            if (!hasGreeted) {
                hasGreeted = true;
                addBotMessage(GREETING).then(() => {
                    showInitialQuickReplies();
                });
            }

            setTimeout(() => input.focus(), 400);
        }

        function closeChat() {
            isOpen = false;
            toggle.classList.remove('cb-toggle--open');
            window_.classList.remove('cb-window--open');
        }

        toggle.addEventListener('click', () => {
            if (isOpen) closeChat();
            else openChat();
        });

        close.addEventListener('click', closeChat);

        send.addEventListener('click', handleUserInput);
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') handleUserInput();
        });

        // Show badge after 3 seconds
        setTimeout(() => {
            if (!isOpen) badge.style.display = 'flex';
        }, 3000);
    }

    function escapeHtml(str) {
        const d = document.createElement('div');
        d.textContent = str;
        return d.innerHTML;
    }

    // Wait for DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
