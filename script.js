/* ============================================
   THU HỒI NỢ PRO — Landing Page Scripts
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // =====================
    // NAVBAR SCROLL
    // =====================
    const navbar = document.getElementById('navbar');
    const floatingBtns = document.getElementById('floatingBtns');

    function onScroll() {
        const y = window.scrollY;
        navbar.classList.toggle('scrolled', y > 60);
        floatingBtns.classList.toggle('visible', y > 500);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // =====================
    // MOBILE MENU
    // =====================
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    mobileToggle.addEventListener('click', () => {
        mobileToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
        document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
    });
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileToggle.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // =====================
    // SCROLL ANIMATIONS
    // =====================
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: '0px 0px -60px 0px', threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

    // =====================
    // COUNTER ANIMATION
    // =====================
    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'));
        const duration = 2200;
        const start = performance.now();

        function tick(now) {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(eased * target).toLocaleString('vi-VN');
            if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.querySelectorAll('.counter').forEach(c => animateCounter(c));
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.4 });

    const proofStats = document.querySelector('.proof-stats');
    if (proofStats) counterObserver.observe(proofStats);

    // =====================
    // FAQ ACCORDION
    // =====================
    document.querySelectorAll('.faq-question').forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.parentElement;
            const isOpen = item.classList.contains('open');

            // Close all
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

            // Toggle current
            if (!isOpen) item.classList.add('open');
        });
    });

    // =====================
    // SMOOTH SCROLL (only for internal anchors)
    // =====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // =====================
    // MOBILE CTA BAR VISIBILITY
    // =====================
    const mobileCta = document.getElementById('mobileCta');
    if (mobileCta) {
        function toggleMobileCta() {
            if (window.scrollY > 300) {
                mobileCta.classList.add('visible');
            } else {
                mobileCta.classList.remove('visible');
            }
        }
        window.addEventListener('scroll', toggleMobileCta, { passive: true });
        toggleMobileCta();
    }

    // =====================
    // FORM HANDLING — Lưu data lên Google Sheets + Gửi Zalo
    // =====================
    const ZALO_URL = 'https://chat.zalo.me/?phone=0898437922';

    // ★★★ QUAN TRỌNG: Paste URL Google Apps Script vào đây ★★★
    // Xem hướng dẫn trong file HUONG_DAN_GOOGLE_SHEETS.md
    const GOOGLE_SHEETS_URL = 'https://script.google.com/macros/s/AKfycbwS4EyLfNCcmbClNGFzBtgiSV-GQ17S4Ju3p-acIDll-hbYOjF3mRTNlHX3HvFgEdra/exec';

    const form = document.getElementById('registerForm');
    const formSuccess = document.getElementById('formSuccess');

    // Toggle "Other" text input for docs
    const docOtherCheckbox = document.getElementById('docOtherCheckbox');
    const docOtherText = document.getElementById('docOtherText');
    if (docOtherCheckbox && docOtherText) {
        docOtherCheckbox.addEventListener('change', (e) => {
            docOtherText.style.display = e.target.checked ? 'block' : 'none';
            if (e.target.checked) docOtherText.focus();
        });
    }

    const preSubmitBtn = document.getElementById('preSubmitBtn');
    const checkoutModal = document.getElementById('checkoutModal');
    const btnEditForm = document.getElementById('btnEditForm');
    const btnConfirmForm = document.getElementById('btnConfirmForm');
    const checkoutSummary = document.getElementById('checkoutSummary');

    let pendingFormData = null;

    if (preSubmitBtn && form) {
        preSubmitBtn.addEventListener('click', () => {
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            // Collect form data
            const fullName = document.getElementById('fullName').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const email = document.getElementById('email') ? document.getElementById('email').value.trim() : '';

            const debtAmountEl = document.querySelector('input[name="debtAmount"]:checked');
            const debtAmount = debtAmountEl ? debtAmountEl.value : '';

            const debtTimeEl = document.querySelector('input[name="debtTime"]:checked');
            const debtTime = debtTimeEl ? debtTimeEl.value : '';

            const docEls = document.querySelectorAll('input[name="docs"]:checked');
            const docsList = [];
            docEls.forEach(el => {
                if (el.value === 'Khác') {
                    const otherText = document.getElementById('docOtherText').value.trim();
                    docsList.push(`Khác (${otherText})`);
                } else {
                    docsList.push(el.value);
                }
            });
            const docs = docsList.join(', ');

            const urgencyEl = document.querySelector('input[name="urgency"]:checked');
            const urgency = urgencyEl ? urgencyEl.value : '';
            
            const contactMethodEl = document.querySelector('input[name="contactMethod"]:checked');
            const contactMethod = contactMethodEl ? contactMethodEl.value : 'Qua Zalo';

            // Combine into debtNote
            const debtNote = `Thời gian nợ: ${debtTime} | Chứng từ: ${docs || 'Không có'} | Cấp thiết: ${urgency} | Hình thức liên hệ: ${contactMethod}`;

            pendingFormData = { fullName, phone, email, debtAmount, debtNote, contactMethod };

            // Hiển thị tóm tắt lên Modal
            if (checkoutSummary) {
                checkoutSummary.innerHTML = `
                    <div class="checkout-summary-item"><span class="checkout-summary-label">Họ tên:</span> <strong>${fullName}</strong></div>
                    <div class="checkout-summary-item"><span class="checkout-summary-label">SĐT / Zalo:</span> <strong>${phone}</strong></div>
                    <div class="checkout-summary-item"><span class="checkout-summary-label">Email:</span> <strong>${email || 'Chưa cung cấp'}</strong></div>
                    <div class="checkout-summary-item"><span class="checkout-summary-label">Số tiền:</span> <strong>${debtAmount}</strong></div>
                    <div class="checkout-summary-item"><span class="checkout-summary-label">Pháp lý có sẵn:</span> <strong>${docs || 'Không có'}</strong></div>
                    <div class="checkout-summary-item"><span class="checkout-summary-label">Yêu cầu liên hệ:</span> <strong style="color:var(--gold-500)">${contactMethod}</strong></div>
                `;
            }

            if (checkoutModal) checkoutModal.classList.add('show');
        });
    }

    if (btnEditForm && checkoutModal) {
        btnEditForm.addEventListener('click', () => {
            checkoutModal.classList.remove('show');
        });
    }

    if (btnConfirmForm && form) {
        btnConfirmForm.addEventListener('click', async () => {
            if (!pendingFormData) return;
            
            if (checkoutModal) checkoutModal.classList.remove('show');
            const { fullName, phone, email, debtAmount, debtNote, contactMethod } = pendingFormData;

            // ---- UI: Show loading ----
            const originalBtnHTML = preSubmitBtn.innerHTML;
            preSubmitBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" style="animation: spin 1s linear infinite;">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="60" stroke-linecap="round"/>
                </svg>
                <span>Đang xử lý...</span>
            `;
            preSubmitBtn.disabled = true;
            preSubmitBtn.style.opacity = '0.7';

            if (!document.getElementById('spinKeyframe')) {
                const s = document.createElement('style');
                s.id = 'spinKeyframe';
                s.textContent = '@keyframes spin { to { transform: rotate(360deg); } }';
                document.head.appendChild(s);
            }

            const now = new Date().toLocaleString('vi-VN', {
                timeZone: 'Asia/Ho_Chi_Minh',
                year: 'numeric', month: '2-digit', day: '2-digit',
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            });

            // Gửi Google Sheets
            if (GOOGLE_SHEETS_URL) {
                try {
                    const formData = new FormData();
                    formData.append('fullName', fullName);
                    formData.append('phone', phone);
                    formData.append('debtAmount', debtAmount);
                    formData.append('debtNote', debtNote);
                    formData.append('createdAt', now);
                    formData.append('source', window.location.href);

                    await fetch(GOOGLE_SHEETS_URL, { method: 'POST', body: formData });
                } catch (err) { console.warn('Google Sheets error:', err); }
            }

            // Save localStorage
            const lead = {
                id: Date.now(), fullName, phone, email, debtAmount, debtNote,
                createdAt: now, source: window.location.href, status: 'Mới'
            };
            const leads = JSON.parse(localStorage.getItem('thuhoino_leads') || '[]');
            leads.push(lead);
            localStorage.setItem('thuhoino_leads', JSON.stringify(leads));

            // Gửi Backend châm ngòi Email
            try {
                await fetch('/api/customers', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: fullName, phone: phone, email: email, notes: debtNote, source: 'Landing Page'
                    })
                });
            } catch (err) { console.warn('Backend API error:', err); }

            // Hiệu ứng Thành Công
            form.style.display = 'none';
            formSuccess.classList.add('show');

            // Chuyển hướng Zalo TÙY VÀO LỰA CHỌN
            if (contactMethod === 'Qua Zalo') {
                setTimeout(() => {
                    window.open(ZALO_URL, '_blank');
                }, 2000);
            } else {
                // Sửa nhẹ chữ thành công cho hợp ngữ cảnh
                formSuccess.innerHTML = `
                    <div class="success-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5" /></svg>
                    </div>
                    <h3>Đăng Ký Thành Công!</h3>
                    <p style="margin-top: 8px;">Hệ thống đã ghi nhận thông tin của bạn. Vui lòng kiểm tra Email hoặc Chờ điện thoại từ chuyên viên.</p>
                `;
            }
        });
    }

    // =====================
    // ACTIVE NAV HIGHLIGHT
    // =====================
    const sections = document.querySelectorAll('section[id]');
    const allNavLinks = document.querySelectorAll('.nav-links a');

    function highlightNav() {
        const scrollPos = window.scrollY + 200;
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            if (scrollPos >= top && scrollPos < top + height) {
                allNavLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    window.addEventListener('scroll', highlightNav, { passive: true });

    // =====================
    // CARD HOVER TILT (Desktop)
    // =====================
    if (window.matchMedia('(min-width: 769px) and (hover: hover)').matches) {
        document.querySelectorAll('.pain-card, .solution-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const rx = (y - rect.height / 2) / 25;
                const ry = (rect.width / 2 - x) / 25;
                card.style.transform = `perspective(700px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-4px)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    // =====================
    // TIMELINE PROGRESS LINE
    // =====================
    const timelineLine = document.getElementById('timelineLine');
    if (timelineLine) {
        const timelineObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    timelineLine.style.background = `linear-gradient(180deg, var(--gold-500) 0%, var(--gold-500) 100%)`;
                    timelineLine.style.transition = 'background 1.5s ease';
                }
            });
        }, { threshold: 0.2 });

        const processSection = document.getElementById('process');
        if (processSection) timelineObserver.observe(processSection);
    }
});

// =====================
// COPY TO CLIPBOARD (Payment Section)
// =====================
function copyToClipboard(text, btnElement) {
    navigator.clipboard.writeText(text).then(() => {
        btnElement.classList.add('copied');
        const originalHTML = btnElement.innerHTML;
        btnElement.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16">
                <path d="M20 6L9 17l-5-5"/>
            </svg>
        `;
        setTimeout(() => {
            btnElement.classList.remove('copied');
            btnElement.innerHTML = originalHTML;
        }, 2000);
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        btnElement.classList.add('copied');
        setTimeout(() => btnElement.classList.remove('copied'), 2000);
    });
}
