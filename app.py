import streamlit as st
from datetime import date, timedelta
import random

# ============================================================
# APP ĐẶT TOUR THÔNG MINH
# 3 tính năng chính:
# 1. Trợ lý AI cá nhân hóa tour
# 2. Đổi lịch trình thông minh
# 5. Trợ lý xử lý sự cố
# ============================================================

st.set_page_config(
    page_title="SmartTour - Đặt tour thông minh",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.image("VT.jpg")
# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #666;
        font-size: 17px;
        margin-bottom: 25px;
    }
    .tour-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e6e6e6;
        margin-bottom: 15px;
        background: white;
    }
    .price {
        font-size: 24px;
        font-weight: 700;
    }
    .feature-card {
        padding: 18px;
        border-radius: 14px;
        background: #f7f9fc;
        border: 1px solid #e7ebf0;
        min-height: 150px;
    }
    .success-box {
        padding: 15px;
        border-radius: 12px;
        background: #eaf8ef;
        border: 1px solid #b9e4c7;
    }
    .warning-box {
        padding: 15px;
        border-radius: 12px;
        background: #fff8e6;
        border: 1px solid #f2d58a;
    }
    .incident-box {
        padding: 15px;
        border-radius: 12px;
        background: #fff1f1;
        border: 1px solid #efb3b3;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Dữ liệu mẫu
# -----------------------------
TOURS = [
    {
        "id": 1,
        "name": "Phú Quốc 3N2Đ - Khám phá đảo ngọc",
        "destination": "Phú Quốc",
        "days": 3,
        "nights": 2,
        "price": 4590000,
        "category": ["biển", "nghỉ dưỡng", "ẩm thực"],
        "difficulty": "Dễ",
        "transport": "Máy bay + xe du lịch",
        "description": "Bãi Sao, Hòn Thơm, chợ đêm và trải nghiệm ẩm thực địa phương.",
        "schedule": [
            "Ngày 1: Đón sân bay → nhận phòng → Bãi Sao → ăn tối → chợ đêm",
            "Ngày 2: Hòn Thơm → cáp treo → vui chơi → ăn tối hải sản",
            "Ngày 3: Tham quan trung tâm → mua đặc sản → tiễn sân bay"
        ]
    },
    {
        "id": 2,
        "name": "Đà Nẵng - Hội An 4N3Đ",
        "destination": "Đà Nẵng",
        "days": 4,
        "nights": 3,
        "price": 5290000,
        "category": ["biển", "văn hóa", "ẩm thực", "check-in"],
        "difficulty": "Dễ",
        "transport": "Máy bay + xe du lịch",
        "description": "Bà Nà Hills, phố cổ Hội An, biển Mỹ Khê và ẩm thực miền Trung.",
        "schedule": [
            "Ngày 1: Đà Nẵng → nhận phòng → biển Mỹ Khê → cầu Rồng",
            "Ngày 2: Bà Nà Hills → Cầu Vàng → trở về Đà Nẵng",
            "Ngày 3: Ngũ Hành Sơn → Hội An → phố cổ → thả đèn",
            "Ngày 4: Mua đặc sản → tiễn sân bay"
        ]
    },
    {
        "id": 3,
        "name": "Đà Lạt 3N2Đ - Săn mây & nghỉ dưỡng",
        "destination": "Đà Lạt",
        "days": 3,
        "nights": 2,
        "price": 3290000,
        "category": ["thiên nhiên", "check-in", "nghỉ dưỡng", "ẩm thực"],
        "difficulty": "Dễ",
        "transport": "Xe du lịch",
        "description": "Săn mây, đồi chè, vườn hoa và trải nghiệm cà phê Đà Lạt.",
        "schedule": [
            "Ngày 1: Đà Lạt → nhận phòng → quảng trường → chợ đêm",
            "Ngày 2: Săn mây → đồi chè → vườn hoa → cà phê",
            "Ngày 3: Dinh thự → mua đặc sản → kết thúc tour"
        ]
    },
    {
        "id": 4,
        "name": "Nha Trang 3N2Đ - Biển & vui chơi",
        "destination": "Nha Trang",
        "days": 3,
        "nights": 2,
        "price": 3990000,
        "category": ["biển", "nghỉ dưỡng", "vui chơi"],
        "difficulty": "Dễ",
        "transport": "Máy bay + xe du lịch",
        "description": "Biển Nha Trang, đảo, vui chơi và khám phá ẩm thực.",
        "schedule": [
            "Ngày 1: Nhận phòng → biển Nha Trang → ăn tối",
            "Ngày 2: Tour đảo → vui chơi → ăn hải sản",
            "Ngày 3: Tham quan thành phố → mua đặc sản → kết thúc"
        ]
    },
    {
        "id": 5,
        "name": "Huế 3N2Đ - Dấu ấn hoàng triều",
        "destination": "Huế",
        "days": 3,
        "nights": 2,
        "price": 3490000,
        "category": ["văn hóa", "lịch sử", "ẩm thực"],
        "difficulty": "Dễ",
        "transport": "Xe du lịch",
        "description": "Đại Nội, lăng vua, chùa Thiên Mụ và ẩm thực cung đình.",
        "schedule": [
            "Ngày 1: Đại Nội → Đông Ba → thưởng thức ẩm thực Huế",
            "Ngày 2: Lăng vua → chùa Thiên Mụ → sông Hương",
            "Ngày 3: Mua đặc sản → tham quan tự do → kết thúc"
        ]
    }
]

# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Trang chủ"

if "selected_tour" not in st.session_state:
    st.session_state.selected_tour = None

if "booking" not in st.session_state:
    st.session_state.booking = None

if "custom_tour" not in st.session_state:
    st.session_state.custom_tour = None

if "incident_result" not in st.session_state:
    st.session_state.incident_result = None


def money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


def find_tour_by_id(tour_id):
    return next((t for t in TOURS if t["id"] == tour_id), None)


def recommend_tours(days, budget, people, interests, style):
    """
    Bộ máy đề xuất tour dạng rule-based.
    Có thể thay bằng API AI thật sau này.
    """
    results = []

    for tour in TOURS:
        score = 0

        # Thời lượng
        difference = abs(tour["days"] - days)
        if difference == 0:
            score += 30
        elif difference == 1:
            score += 18
        elif difference == 2:
            score += 8

        # Ngân sách
        if tour["price"] <= budget:
            score += 25
            if tour["price"] >= budget * 0.75:
                score += 5
        else:
            over = tour["price"] - budget
            if over <= 500000:
                score += 8

        # Số khách
        if people >= 4:
            score += 5

        # Sở thích
        for interest in interests:
            if interest in tour["category"]:
                score += 12

        # Phong cách
        if style == "Nghỉ dưỡng" and "nghỉ dưỡng" in tour["category"]:
            score += 15
        elif style == "Khám phá" and (
            "văn hóa" in tour["category"] or "lịch sử" in tour["category"]
        ):
            score += 15
        elif style == "Check-in" and "check-in" in tour["category"]:
            score += 15
        elif style == "Ẩm thực" and "ẩm thực" in tour["category"]:
            score += 15

        results.append((score, tour))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:3]


def build_custom_schedule(tour, date_start, people):
    result = []
    for index, item in enumerate(tour["schedule"]):
        current_date = date_start + timedelta(days=index)
        result.append(f"{current_date.strftime('%d/%m/%Y')} — {item}")
    return result


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 🧳 SmartTour")
    st.caption("Đặt tour & điều hành tour thông minh")

    menu = st.radio(
        "MENU",
        [
            "Trang chủ",
            "🤖 Tạo tour bằng AI",
            "🗺️ Khám phá & đặt tour",
            "🔄 Đổi lịch trình thông minh",
            "🚨 Trợ lý xử lý sự cố",
            "📋 Đơn đặt tour"
        ],
        index=0
    )

    if menu == "Trang chủ":
        st.session_state.page = "Trang chủ"
    elif "Tạo tour" in menu:
        st.session_state.page = "AI"
    elif "Khám phá" in menu:
        st.session_state.page = "TOURS"
    elif "Đổi lịch" in menu:
        st.session_state.page = "CHANGE"
    elif "sự cố" in menu:
        st.session_state.page = "INCIDENT"
    else:
        st.session_state.page = "BOOKING"

    st.divider()
    st.info(
        "💡 Đây là phiên bản demo không cần MySQL/API. "
        "Dữ liệu được lưu trong session của phiên chạy."
    )


# ============================================================
# TRANG CHỦ
# ============================================================
if st.session_state.page == "Trang chủ":
    st.markdown('<div class="main-title">🧳 SmartTour</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Nền tảng đặt tour thông minh — cá nhân hóa, linh hoạt và hỗ trợ khách trong suốt hành trình.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🤖 AI cá nhân hóa</h3>
        <p>Nhập ngân sách, thời gian và sở thích. Hệ thống đề xuất tour phù hợp.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🔄 Đổi lịch thông minh</h3>
        <p>Khi thời tiết hoặc điều kiện thay đổi, app đề xuất phương án thay thế.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>🚨 Hỗ trợ sự cố</h3>
        <p>Khách có thể báo sự cố và nhận hướng xử lý ngay trên app.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("⭐ Các tour nổi bật")

    cols = st.columns(3)
    for i, tour in enumerate(TOURS[:3]):
        with cols[i]:
            st.markdown(f"### {tour['name']}")
            st.write(tour["description"])
            st.write(f"**Từ {money(tour['price'])}/người**")
            if st.button("Xem tour", key=f"home_tour_{tour['id']}"):
                st.session_state.selected_tour = tour["id"]
                st.session_state.page = "TOURS"
                st.rerun()

    st.divider()
    st.subheader("⚙️ Quy trình sử dụng")
    st.markdown("""
    **1. Nhập nhu cầu → 2. Nhận đề xuất → 3. Chọn tour → 
    4. Đặt tour → 5. Theo dõi & thay đổi lịch trình → 6. Hỗ trợ sự cố**
    """)


# ============================================================
# TÍNH NĂNG 1 — AI TẠO TOUR
# ============================================================
elif st.session_state.page == "AI":
    st.title("🤖 Trợ lý AI cá nhân hóa tour")
    st.write(
        "Cho hệ thống biết nhu cầu của bạn. SmartTour sẽ chấm điểm và "
        "đề xuất những tour phù hợp nhất."
    )

    with st.form("ai_form"):
        col1, col2 = st.columns(2)

        with col1:
            destination = st.selectbox(
                "Điểm đến mong muốn",
                ["Không giới hạn"] + sorted(list(set(t["destination"] for t in TOURS)))
            )

            days = st.slider("Số ngày mong muốn", 2, 7, 3)

            budget = st.number_input(
                "Ngân sách / người (VNĐ)",
                min_value=1000000,
                max_value=50000000,
                value=5000000,
                step=500000
            )

        with col2:
            people = st.number_input(
                "Số người",
                min_value=1,
                max_value=100,
                value=2,
                step=1
            )

            interests = st.multiselect(
                "Bạn thích gì?",
                ["biển", "nghỉ dưỡng", "ẩm thực", "văn hóa",
                 "lịch sử", "check-in", "thiên nhiên", "vui chơi"],
                default=["ẩm thực"]
            )

            style = st.selectbox(
                "Phong cách chuyến đi",
                ["Nghỉ dưỡng", "Khám phá", "Check-in", "Ẩm thực"]
            )

        submitted = st.form_submit_button(
            "✨ Tạo đề xuất tour",
            use_container_width=True
        )

    if submitted:
        results = recommend_tours(days, budget, people, interests, style)

        if destination != "Không giới hạn":
            filtered = [
                item for item in results
                if item[1]["destination"] == destination
            ]

            # Nếu có kết quả đúng điểm đến thì ưu tiên
            if filtered:
                results = filtered + [
                    item for item in results if item not in filtered
                ]

        st.session_state.custom_tour = results

    if st.session_state.custom_tour:
        st.divider()
        st.subheader("🎯 Tour được đề xuất cho bạn")

        for rank, (score, tour) in enumerate(st.session_state.custom_tour, start=1):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {rank}. {tour['name']}")
                    st.write(tour["description"])
                    st.write(
                        f"📅 {tour['days']} ngày {tour['nights']} đêm  | "
                        f"🚐 {tour['transport']}  | "
                        f"🎯 Độ phù hợp: **{min(score, 100)}%**"
                    )
                    st.write("**Lịch trình:**")
                    for item in tour["schedule"]:
                        st.write("• " + item)

                with col2:
                    st.markdown(f"### {money(tour['price'])}")
                    st.caption("Giá/người")

                    if st.button(
                        "Đặt tour này",
                        key=f"ai_book_{tour['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_tour = tour["id"]
                        st.session_state.page = "TOURS"
                        st.rerun()


# ============================================================
# KHÁM PHÁ & ĐẶT TOUR
# ============================================================
elif st.session_state.page == "TOURS":
    st.title("🗺️ Khám phá & đặt tour")

    if st.session_state.selected_tour:
        selected = find_tour_by_id(st.session_state.selected_tour)
        st.success(f"Đang chọn: {selected['name']}")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        destination_filter = st.selectbox(
            "Lọc theo điểm đến",
            ["Tất cả"] + sorted(list(set(t["destination"] for t in TOURS)))
        )

    with filter_col2:
        max_price = st.slider(
            "Ngân sách tối đa / người",
            1000000,
            10000000,
            6000000,
            step=500000
        )

    filtered_tours = [
        t for t in TOURS
        if (destination_filter == "Tất cả" or t["destination"] == destination_filter)
        and t["price"] <= max_price
    ]

    if not filtered_tours:
        st.warning("Không có tour phù hợp với bộ lọc.")
    else:
        for tour in filtered_tours:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.subheader(tour["name"])
                    st.write(tour["description"])
                    st.write(
                        f"📅 {tour['days']} ngày {tour['nights']} đêm | "
                        f"🏷️ {', '.join(tour['category'])}"
                    )

                with col2:
                    st.markdown(f"### {money(tour['price'])}")
                    st.caption("/ người")

                    if st.button(
                        "Chọn tour",
                        key=f"select_{tour['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_tour = tour["id"]
                        st.rerun()

                if st.session_state.selected_tour == tour["id"]:
                    st.divider()
                    st.write("### 📅 Lịch trình")
                    for item in tour["schedule"]:
                        st.write("• " + item)

                    with st.form(f"booking_form_{tour['id']}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            customer_name = st.text_input("Họ và tên")
                            customer_phone = st.text_input("Số điện thoại")
                            departure_date = st.date_input(
                                "Ngày khởi hành",
                                value=date.today() + timedelta(days=7),
                                min_value=date.today() + timedelta(days=1)
                            )

                        with c2:
                            customer_email = st.text_input("Email")
                            number_people = st.number_input(
                                "Số lượng khách",
                                min_value=1,
                                max_value=100,
                                value=2
                            )
                            note = st.text_area("Yêu cầu đặc biệt")

                        total = tour["price"] * number_people
                        st.info(f"💰 Tổng tạm tính: **{money(total)}**")

                        confirm = st.form_submit_button(
                            "✅ Xác nhận đặt tour",
                            use_container_width=True
                        )

                    if confirm:
                        if not customer_name.strip() or not customer_phone.strip():
                            st.error("Vui lòng nhập họ tên và số điện thoại.")
                        else:
                            st.session_state.booking = {
                                "code": "ST" + str(random.randint(100000, 999999)),
                                "tour": tour["name"],
                                "date": departure_date,
                                "people": number_people,
                                "name": customer_name,
                                "phone": customer_phone,
                                "email": customer_email,
                                "note": note,
                                "total": total,
                                "status": "Đã xác nhận"
                            }
                            st.success(
                                f"Đặt tour thành công! Mã đặt tour: "
                                f"**{st.session_state.booking['code']}**"
                            )


# ============================================================
# TÍNH NĂNG 2 — ĐỔI LỊCH TRÌNH THÔNG MINH
# ============================================================
elif st.session_state.page == "CHANGE":
    st.title("🔄 Đổi lịch trình thông minh")
    st.write(
        "Mô phỏng tình huống tour bị ảnh hưởng bởi thời tiết, "
        "đóng cửa điểm tham quan hoặc thay đổi điều kiện vận hành."
    )

    if not st.session_state.booking:
        st.warning("Bạn chưa có đơn đặt tour. Hãy đặt một tour trước.")
    else:
        booking = st.session_state.booking
        st.success(
            f"Đơn **{booking['code']}** — {booking['tour']} — "
            f"{booking['people']} khách"
        )

        reason = st.selectbox(
            "Lý do cần thay đổi",
            [
                "🌧️ Thời tiết xấu",
                "🚧 Điểm tham quan tạm đóng cửa",
                "🚌 Phương tiện bị thay đổi",
                "👥 Khách muốn thay đổi nhu cầu",
                "⏰ Đoàn bị trễ thời gian"
            ]
        )

        st.subheader("🤖 Phương án SmartTour đề xuất")

        alternatives = {
            "🌧️ Thời tiết xấu": [
                ("Phương án A", "Thay hoạt động ngoài trời bằng bảo tàng + trải nghiệm ẩm thực.", "Giữ nguyên thời lượng"),
                ("Phương án B", "Chuyển điểm tham quan ngoài trời sang hoạt động trong nhà.", "Giảm 1 hoạt động"),
                ("Phương án C", "Dời hoạt động ngoài trời sang ngày tiếp theo.", "Điều chỉnh toàn bộ lịch trình")
            ],
            "🚧 Điểm tham quan tạm đóng cửa": [
                ("Phương án A", "Thay bằng một điểm tham quan tương đương gần đó.", "Không phát sinh"),
                ("Phương án B", "Tăng thời gian trải nghiệm tại điểm tiếp theo.", "Không đổi tuyến"),
                ("Phương án C", "Điều chỉnh lịch trình theo điểm tham quan dự phòng.", "Có thay đổi thứ tự")
            ],
            "🚌 Phương tiện bị thay đổi": [
                ("Phương án A", "Điều chuyển sang xe dự phòng cùng tiêu chuẩn.", "Ít ảnh hưởng"),
                ("Phương án B", "Chia đoàn thành 2 xe nhỏ.", "Có thay đổi phương tiện"),
                ("Phương án C", "Điều chỉnh giờ khởi hành.", "Thay đổi thời gian")
            ],
            "👥 Khách muốn thay đổi nhu cầu": [
                ("Phương án A", "Bỏ một hoạt động và tăng thời gian tự do.", "Linh hoạt"),
                ("Phương án B", "Thay hoạt động hiện tại bằng trải nghiệm phù hợp sở thích.", "Cá nhân hóa"),
                ("Phương án C", "Giữ lịch trình chính, thêm hoạt động tự chọn.", "Có thể phát sinh phí")
            ],
            "⏰ Đoàn bị trễ thời gian": [
                ("Phương án A", "Rút ngắn thời gian tại điểm hiện tại.", "Giữ toàn bộ lịch trình"),
                ("Phương án B", "Bỏ một điểm ít ưu tiên.", "Giảm 1 điểm"),
                ("Phương án C", "Điều chỉnh giờ ăn và thời gian tham quan.", "Tối ưu thời gian")
            ]
        }

        selected_option = None

        for title, desc, impact in alternatives[reason]:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"### {title}")
                    st.write(desc)
                    st.caption("Ảnh hưởng: " + impact)
                with c2:
                    if st.button("Chọn", key=f"change_{title}"):
                        selected_option = title
                        st.session_state.change_result = {
                            "reason": reason,
                            "option": title,
                            "description": desc
                        }

        if "change_result" in st.session_state:
            result = st.session_state.change_result
            st.divider()
            st.markdown(
                f"""
                <div class="success-box">
                <h3>✅ Đã chọn phương án</h3>
                <b>Lý do:</b> {result['reason']}<br>
                <b>Phương án:</b> {result['option']}<br>
                <b>Xử lý:</b> {result['description']}<br><br>
                📢 Hệ thống có thể gửi thông báo mới cho khách, HDV và tài xế.
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# TÍNH NĂNG 5 — TRỢ LÝ XỬ LÝ SỰ CỐ
# ============================================================
elif st.session_state.page == "INCIDENT":
    st.title("🚨 Trợ lý xử lý sự cố du lịch")
    st.write(
        "Khách chọn vấn đề đang gặp phải. Hệ thống đưa ra hướng xử lý "
        "ban đầu và xác định người cần được thông báo."
    )

    incident = st.selectbox(
        "Bạn đang gặp vấn đề gì?",
        [
            "🚌 Trễ xe / không thấy xe đón",
            "📍 Lạc đoàn",
            "🎒 Thất lạc hành lý / đồ cá nhân",
            "🏨 Vấn đề phòng khách sạn",
            "🌧️ Thời tiết ảnh hưởng lịch trình",
            "📞 Không liên hệ được với HDV",
            "🆘 Tình huống khẩn cấp"
        ]
    )

    detail = st.text_area(
        "Mô tả thêm tình huống",
        placeholder="Ví dụ: Tôi đang ở sảnh khách sạn nhưng chưa thấy xe..."
    )

    if st.button("🚨 Gửi yêu cầu hỗ trợ", use_container_width=True):
        responses = {
            "🚌 Trễ xe / không thấy xe đón": {
                "level": "Cần điều hành kiểm tra ngay",
                "action": [
                    "Kiểm tra vị trí xe và thời gian đón.",
                    "Liên hệ tài xế/HDV.",
                    "Gửi vị trí hiện tại của khách cho điều hành.",
                    "Thông báo thời gian đón dự kiến cho khách."
                ]
            },
            "📍 Lạc đoàn": {
                "level": "Ưu tiên cao",
                "action": [
                    "Khách ở nguyên vị trí an toàn nếu có thể.",
                    "Gửi vị trí hiện tại.",
                    "Liên hệ HDV và điều hành.",
                    "Không tự ý di chuyển đến địa điểm khác khi chưa được hướng dẫn."
                ]
            },
            "🎒 Thất lạc hành lý / đồ cá nhân": {
                "level": "Cần hỗ trợ",
                "action": [
                    "Xác định địa điểm cuối cùng nhìn thấy đồ.",
                    "Thông báo cho HDV.",
                    "Liên hệ địa điểm/nhà hàng/khách sạn liên quan.",
                    "Ghi nhận thông tin tài sản thất lạc."
                ]
            },
            "🏨 Vấn đề phòng khách sạn": {
                "level": "Điều hành/HDV hỗ trợ",
                "action": [
                    "Ghi nhận tình trạng phòng.",
                    "Liên hệ lễ tân.",
                    "Yêu cầu phương án khắc phục hoặc đổi phòng nếu cần.",
                    "Cập nhật kết quả cho khách."
                ]
            },
            "🌧️ Thời tiết ảnh hưởng lịch trình": {
                "level": "Điều hành cần đánh giá",
                "action": [
                    "Kiểm tra điều kiện thời tiết.",
                    "Đánh giá các hoạt động bị ảnh hưởng.",
                    "Đề xuất điểm thay thế.",
                    "Cập nhật lịch trình cho toàn đoàn."
                ]
            },
            "📞 Không liên hệ được với HDV": {
                "level": "Cần điều hành kiểm tra",
                "action": [
                    "Kiểm tra trạng thái HDV.",
                    "Liên hệ qua kênh dự phòng.",
                    "Điều hành liên hệ trưởng đoàn/khách.",
                    "Bố trí nhân sự hỗ trợ nếu cần."
                ]
            },
            "🆘 Tình huống khẩn cấp": {
                "level": "KHẨN CẤP",
                "action": [
                    "Ưu tiên đảm bảo an toàn cho người gặp nạn.",
                    "Liên hệ dịch vụ khẩn cấp phù hợp tại địa phương.",
                    "Thông báo ngay cho HDV và điều hành.",
                    "Cung cấp vị trí và thông tin cần thiết."
                ]
            }
        }

        result = responses[incident]
        st.session_state.incident_result = result

    if st.session_state.incident_result:
        result = st.session_state.incident_result

        st.divider()
        st.markdown(
            f"""
            <div class="incident-box">
            <h3>🚨 Mức độ: {result['level']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("🛠️ Hướng xử lý đề xuất")
        for action in result["action"]:
            st.write("✅ " + action)

        if detail:
            st.info(f"Thông tin khách cung cấp: {detail}")

        st.success(
            "Yêu cầu đã được ghi nhận. Trong phiên bản triển khai thực tế, "
            "hệ thống có thể gửi thông báo trực tiếp đến điều hành và HDV."
        )


# ============================================================
# ĐƠN ĐẶT TOUR
# ============================================================
elif st.session_state.page == "BOOKING":
    st.title("📋 Đơn đặt tour")

    if not st.session_state.booking:
        st.info("Bạn chưa có đơn đặt tour nào trong phiên làm việc này.")
        st.button(
            "🗺️ Đi đặt tour",
            on_click=lambda: st.session_state.update(page="TOURS")
        )
    else:
        booking = st.session_state.booking

        st.markdown(
            f"""
            <div class="success-box">
            <h3>✅ Đặt tour thành công</h3>
            <b>Mã đặt tour:</b> {booking['code']}<br>
            <b>Tour:</b> {booking['tour']}<br>
            <b>Khách hàng:</b> {booking['name']}<br>
            <b>Ngày khởi hành:</b> {booking['date'].strftime('%d/%m/%Y')}<br>
            <b>Số khách:</b> {booking['people']}<br>
            <b>Tổng tiền:</b> {money(booking['total'])}<br>
            <b>Trạng thái:</b> {booking['status']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.subheader("💡 Sau khi đặt tour")
        c1, c2, c3 = st.columns(3)

        with c1:
            st.info("🔄 **Đổi lịch**\n\nXử lý khi tour có thay đổi.")

        with c2:
            st.warning("🚨 **Báo sự cố**\n\nGửi yêu cầu hỗ trợ cho điều hành.")

        with c3:
            st.success("📱 **Thông báo**\n\nPhiên bản thực tế có thể gửi thông báo realtime.")

# Footer
st.divider()
st.caption(
    "SmartTour Demo • Streamlit • Phiên bản không kết nối cơ sở dữ liệu/API • "
    "Có thể mở rộng MySQL, AI API, bản đồ và thanh toán."
)
