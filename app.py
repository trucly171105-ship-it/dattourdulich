import streamlit as st
import socket
import uuid
from datetime import datetime, date

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# ============================================================
# CẤU HÌNH ỨNG DỤNG
# ============================================================

st.set_page_config(
    page_title="VietTour - Đặt Tour Du Lịch",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hiển thị banner nếu file tồn tại; tránh làm app lỗi nếu thiếu VT.jpg
try:
    st.image("VT.jpg", use_container_width=True)
except Exception:
    pass

# ============================================================
# KẾT NỐI AIVEN MYSQL
# ============================================================

# Ưu tiên lấy cấu hình từ st.secrets khi triển khai Streamlit Cloud.
# Nếu chưa có secrets, app sẽ dùng cấu hình Aiven bên dưới.
try:
    DB_USER = st.secrets["mysql"]["user"]
    DB_PASSWORD = st.secrets["mysql"]["password"]
    DB_HOST = st.secrets["mysql"]["host"]
    DB_PORT = st.secrets["mysql"]["port"]
    DB_NAME = st.secrets["mysql"]["database"]
except Exception:
    DB_USER = "avnadmin"
    DB_PASSWORD = "AVNS_cyQyD8Ez8n3Ggy-ax8l"
    DB_HOST = "mysql-d660cbf-trucly171105-b953.k.aivencloud.com"
    DB_PORT = 27221
    DB_NAME = "defaultdb"

# ------------------------------------------------------------------
# Làm sạch dữ liệu kết nối
# ------------------------------------------------------------------

DB_USER = str(DB_USER).strip()
DB_PASSWORD = str(DB_PASSWORD).strip()
DB_HOST = str(DB_HOST).strip()
DB_NAME = str(DB_NAME).strip()
DB_PORT = int(DB_PORT)

# ============================================================
# DEBUG KẾT NỐI AIVEN
# ============================================================

with st.expander("🔧 Kiểm tra kết nối Aiven", expanded=False):
    st.write("**HOST:**", repr(DB_HOST))
    st.write("**PORT:**", repr(DB_PORT))
    st.write("**DATABASE:**", repr(DB_NAME))
    st.write("**USER:**", repr(DB_USER))

    if DB_HOST != DB_HOST.strip():
        st.error("HOST đang có khoảng trắng ở đầu hoặc cuối. Đã tự động loại bỏ.")
    else:
        st.success("HOST không có khoảng trắng.")

    if st.button("🔍 Kiểm tra DNS Aiven", key="check_dns_aiven"):
        try:
            ip_address = socket.gethostbyname(DB_HOST)
            st.success(f"DNS OK - Host Aiven trỏ tới IP: {ip_address}")
        except Exception as e:
            st.error(f"DNS ERROR: Không phân giải được hostname Aiven.\n\n{e}")

# ============================================================
# TẠO DATABASE URL
# ============================================================

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

# ============================================================
# DATABASE ENGINE
# ============================================================

@st.cache_resource
def get_db_engine():
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        connect_args={"connect_timeout": 15},
    )

# ============================================================
# KIỂM TRA KẾT NỐI MYSQL
# ============================================================

def test_database_connection():
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        return True, "Kết nối Aiven MySQL thành công!"
    except Exception as e:
        return False, str(e)

# ============================================================
# DATABASE - KHỞI TẠO BẢNG VÀ DỮ LIỆU MẪU
# ============================================================

def init_database():
    engine = get_db_engine()

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tours (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                destination VARCHAR(255) NOT NULL,
                duration VARCHAR(100) NOT NULL,
                price DECIMAL(15,2) NOT NULL,
                category VARCHAR(100) NOT NULL,
                image TEXT,
                description TEXT,
                schedule TEXT,
                max_people INT DEFAULT 30
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                booking_code VARCHAR(50) UNIQUE NOT NULL,
                tour_id INT NOT NULL,
                customer_name VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                email VARCHAR(255),
                people INT NOT NULL,
                departure_date VARCHAR(50) NOT NULL,
                payment_method VARCHAR(100) NOT NULL,
                note TEXT,
                total_price DECIMAL(15,2) NOT NULL,
                status VARCHAR(100) DEFAULT 'Chờ xác nhận',
                created_at VARCHAR(50) NOT NULL,
                CONSTRAINT fk_bookings_tour
                    FOREIGN KEY (tour_id) REFERENCES tours(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """))

        count = conn.execute(text("SELECT COUNT(*) FROM tours")).scalar_one()

        if count == 0:
            tours = [
                (
                    "Khám phá Vũng Tàu 2N1Đ",
                    "Vũng Tàu",
                    "2 ngày 1 đêm",
                    1890000,
                    "Biển",
                    "https://images.unsplash.com/photo-1563492065599-3520f775eeed?auto=format&fit=crop&w=1200&q=80",
                    "Khám phá những điểm đến nổi bật tại Vũng Tàu như Bạch Dinh, Núi Lớn, Bãi Trước và thưởng thức đặc sản địa phương.",
                    "Ngày 1: TP.HCM - Vũng Tàu - Bạch Dinh - Bãi Trước\nNgày 2: Núi Lớn - Hải đăng - Mua đặc sản - TP.HCM",
                    30
                ),
                (
                    "Phú Quốc Thiên Đường 3N2Đ",
                    "Phú Quốc",
                    "3 ngày 2 đêm",
                    4590000,
                    "Nghỉ dưỡng",
                    "https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=1200&q=80",
                    "Hành trình nghỉ dưỡng tại đảo ngọc Phú Quốc, kết hợp tham quan biển đảo, vui chơi và thưởng thức ẩm thực.",
                    "Ngày 1: Đến Phú Quốc - Grand World\nNgày 2: Nam đảo - Hòn Thơm\nNgày 3: Chợ Dương Đông - Tiễn sân bay",
                    25
                ),
                (
                    "Đà Nẵng - Hội An 4N3Đ",
                    "Đà Nẵng",
                    "4 ngày 3 đêm",
                    5290000,
                    "Khám phá",
                    "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?auto=format&fit=crop&w=1200&q=80",
                    "Khám phá Đà Nẵng, Hội An và những địa danh nổi tiếng miền Trung.",
                    "Ngày 1: Đà Nẵng - Sơn Trà\nNgày 2: Bà Nà Hills\nNgày 3: Hội An\nNgày 4: Mua sắm - Tiễn sân bay",
                    30
                ),
                (
                    "Đà Lạt Mộng Mơ 3N2Đ",
                    "Đà Lạt",
                    "3 ngày 2 đêm",
                    3290000,
                    "Nghỉ dưỡng",
                    "https://images.unsplash.com/photo-1557750255-c76072a7aad1?auto=format&fit=crop&w=1200&q=80",
                    "Hành trình khám phá thành phố ngàn hoa với nhiều địa điểm check-in nổi tiếng.",
                    "Ngày 1: Trung tâm Đà Lạt\nNgày 2: Đồi chè - Thác Datanla\nNgày 3: Chợ Đà Lạt - Trả khách",
                    30
                ),
                (
                    "Huế - Dấu ấn Hoàng triều 3N2Đ",
                    "Huế",
                    "3 ngày 2 đêm",
                    3890000,
                    "Văn hóa",
                    "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?auto=format&fit=crop&w=1200&q=80",
                    "Hành trình tìm hiểu văn hóa, lịch sử và kiến trúc cố đô Huế.",
                    "Ngày 1: Đại Nội - Đông Ba\nNgày 2: Lăng Khải Định - Lăng Minh Mạng\nNgày 3: Chùa Thiên Mụ - Trả khách",
                    25
                ),
                (
                    "Nha Trang - Vịnh Nha Trang 3N2Đ",
                    "Nha Trang",
                    "3 ngày 2 đêm",
                    4190000,
                    "Biển",
                    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
                    "Tận hưởng biển xanh Nha Trang và trải nghiệm tour đảo.",
                    "Ngày 1: Nha Trang - Tháp Bà\nNgày 2: Tour đảo - Lặn ngắm san hô\nNgày 3: Mua sắm - Trả khách",
                    30
                ),
            ]

            conn.execute(text("""
                INSERT INTO tours
                (name, destination, duration, price, category, image, description, schedule, max_people)
                VALUES
                (:name, :destination, :duration, :price, :category, :image, :description, :schedule, :max_people)
            """), [
                {
                    "name": t[0], "destination": t[1], "duration": t[2], "price": t[3],
                    "category": t[4], "image": t[5], "description": t[6],
                    "schedule": t[7], "max_people": t[8]
                }
                for t in tours
            ])

# ============================================================
# HÀM DATABASE
# ============================================================

def get_tours():
    engine = get_db_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tours ORDER BY id DESC"))
        return result.mappings().all()


def get_tour(tour_id):
    engine = get_db_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM tours WHERE id = :tour_id"),
            {"tour_id": tour_id}
        )
        return result.mappings().first()


def create_booking(
    tour_id,
    customer_name,
    phone,
    email,
    people,
    departure_date,
    payment_method,
    note,
    total_price
):
    engine = get_db_engine()

    booking_code = (
        "VT" + datetime.now().strftime("%y%m%d") +
        uuid.uuid4().hex[:6].upper()
    )
    created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO bookings
            (
                booking_code, tour_id, customer_name, phone, email, people,
                departure_date, payment_method, note, total_price, status, created_at
            )
            VALUES
            (
                :booking_code, :tour_id, :customer_name, :phone, :email, :people,
                :departure_date, :payment_method, :note, :total_price, :status, :created_at
            )
        """), {
            "booking_code": booking_code,
            "tour_id": tour_id,
            "customer_name": customer_name,
            "phone": phone,
            "email": email,
            "people": people,
            "departure_date": departure_date,
            "payment_method": payment_method,
            "note": note,
            "total_price": total_price,
            "status": "Chờ xác nhận",
            "created_at": created_at,
        })

    return booking_code


def get_booking(booking_code):
    engine = get_db_engine()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                bookings.*,
                tours.name AS tour_name,
                tours.destination,
                tours.duration
            FROM bookings
            JOIN tours ON bookings.tour_id = tours.id
            WHERE bookings.booking_code = :booking_code
        """), {"booking_code": booking_code})
        return result.mappings().first()


def get_all_bookings():
    engine = get_db_engine()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                bookings.*,
                tours.name AS tour_name
            FROM bookings
            JOIN tours ON bookings.tour_id = tours.id
            ORDER BY bookings.id DESC
        """))
        return result.mappings().all()


def cancel_booking(booking_code):
    engine = get_db_engine()
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE bookings
                SET status = 'Đã hủy'
                WHERE booking_code = :booking_code
            """),
            {"booking_code": booking_code}
        )

# ============================================================
# FORMAT TIỀN
# ============================================================

def format_price(price):
    return f"{price:,.0f}".replace(",", ".") + " VNĐ"


# ============================================================
# CSS
# ============================================================

def load_css():
    st.markdown("""
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .hero {
        padding: 45px 35px;
        border-radius: 20px;
        margin-bottom: 30px;
        background: linear-gradient(
            135deg,
            #0077b6 0%,
            #00b4d8 100%
        );
        color: white;
    }

    .hero h1 {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
        opacity: 0.95;
    }

    .tour-card {
        background: white;
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #eeeeee;
    }

    .price {
        color: #e63946;
        font-size: 22px;
        font-weight: 800;
    }

    .tour-title {
        font-size: 21px;
        font-weight: 700;
        margin-top: 10px;
    }

    .badge {
        background: #e8f7ff;
        color: #0077b6;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    .info-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }

    .success-box {
        padding: 25px;
        border-radius: 15px;
        background: #ecfdf5;
        border: 1px solid #10b981;
    }

    .footer {
        text-align: center;
        color: #777;
        padding: 30px;
        margin-top: 40px;
    }

    </style>
    """, unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_tour" not in st.session_state:
    st.session_state.selected_tour = None

if "booking_code" not in st.session_state:
    st.session_state.booking_code = None


# ============================================================
# HEADER / SIDEBAR
# ============================================================

def sidebar():
    with st.sidebar:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/201/201623.png",
            width=80
        )

        st.title("VietTour")
        st.caption("Nền tảng đặt tour du lịch")

        st.divider()

        if st.button("🏠 Trang chủ", use_container_width=True):
            st.session_state.page = "home"

        if st.button("🗺️ Tất cả tour", use_container_width=True):
            st.session_state.page = "tours"

        if st.button("🔎 Tra cứu đặt tour", use_container_width=True):
            st.session_state.page = "lookup"

        if st.button("📊 Quản lý đơn", use_container_width=True):
            st.session_state.page = "admin"

        st.divider()

        st.markdown("""
        **VietTour**

        📞 Hotline: 1900 6868  
        📧 Email: support@viettour.vn  
        📍 TP. Hồ Chí Minh, Việt Nam
        """)


# ============================================================
# TRANG CHỦ
# ============================================================

def home_page():

    st.markdown("""
    <div class="hero">
        <h1>🌴 Khám phá Việt Nam cùng VietTour</h1>
        <p>
            Đặt tour du lịch nhanh chóng – đơn giản – tiện lợi.
            Khám phá những điểm đến tuyệt vời trên khắp Việt Nam.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔎 Tìm tour phù hợp với bạn")

    tours = get_tours()

    destinations = ["Tất cả"] + sorted(
        list(set(t["destination"] for t in tours))
    )

    categories = ["Tất cả"] + sorted(
        list(set(t["category"] for t in tours))
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        keyword = st.text_input(
            "Từ khóa",
            placeholder="Ví dụ: Phú Quốc..."
        )

    with col2:
        destination = st.selectbox(
            "Điểm đến",
            destinations
        )

    with col3:
        category = st.selectbox(
            "Loại tour",
            categories
        )

    filtered = []

    for tour in tours:

        match_keyword = (
            keyword.lower() in tour["name"].lower()
            or keyword.lower() in tour["destination"].lower()
        )

        match_destination = (
            destination == "Tất cả"
            or tour["destination"] == destination
        )

        match_category = (
            category == "Tất cả"
            or tour["category"] == category
        )

        if match_keyword and match_destination and match_category:
            filtered.append(tour)

    st.subheader(f"🌟 Tour nổi bật ({len(filtered)})")

    if not filtered:
        st.warning("Không tìm thấy tour phù hợp.")

    cols = st.columns(3)

    for index, tour in enumerate(filtered):

        with cols[index % 3]:

            st.markdown('<div class="tour-card">', unsafe_allow_html=True)

            if tour["image"]:
                st.image(
                    tour["image"],
                    use_container_width=True
                )

            st.markdown(
                f'<span class="badge">{tour["category"]}</span>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="tour-title">{tour["name"]}</div>',
                unsafe_allow_html=True
            )

            st.write(f"📍 {tour['destination']}")
            st.write(f"⏱️ {tour['duration']}")

            st.markdown(
                f'<div class="price">{format_price(tour["price"])}</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "Xem chi tiết",
                key=f"detail_{tour['id']}",
                use_container_width=True
            ):
                st.session_state.selected_tour = tour["id"]
                st.session_state.page = "detail"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# TRANG TẤT CẢ TOUR
# ============================================================

def tours_page():

    st.title("🗺️ Tất cả tour du lịch")

    tours = get_tours()

    col1, col2 = st.columns(2)

    with col1:
        keyword = st.text_input(
            "🔎 Tìm kiếm tour",
            placeholder="Tên tour hoặc điểm đến..."
        )

    with col2:
        sort_option = st.selectbox(
            "Sắp xếp",
            [
                "Mặc định",
                "Giá thấp → cao",
                "Giá cao → thấp"
            ]
        )

    filtered = [
        tour for tour in tours
        if keyword.lower() in tour["name"].lower()
        or keyword.lower() in tour["destination"].lower()
    ]

    if sort_option == "Giá thấp → cao":
        filtered = sorted(filtered, key=lambda x: x["price"])

    elif sort_option == "Giá cao → thấp":
        filtered = sorted(
            filtered,
            key=lambda x: x["price"],
            reverse=True
        )

    for tour in filtered:

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                tour["image"],
                use_container_width=True
            )

        with col2:

            st.markdown(
                f"### {tour['name']}"
            )

            st.write(
                f"📍 **Điểm đến:** {tour['destination']}"
            )

            st.write(
                f"⏱️ **Thời lượng:** {tour['duration']}"
            )

            st.write(
                f"🏷️ **Loại tour:** {tour['category']}"
            )

            st.markdown(
                f"### {format_price(tour['price'])}"
            )

            st.write(tour["description"])

            if st.button(
                "Xem tour",
                key=f"tour_{tour['id']}"
            ):
                st.session_state.selected_tour = tour["id"]
                st.session_state.page = "detail"
                st.rerun()

        st.divider()


# ============================================================
# CHI TIẾT TOUR
# ============================================================

def detail_page():

    tour_id = st.session_state.selected_tour

    if not tour_id:
        st.session_state.page = "tours"
        st.rerun()

    tour = get_tour(tour_id)

    if not tour:
        st.error("Không tìm thấy tour.")
        return

    st.title(tour["name"])

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.image(
            tour["image"],
            use_container_width=True
        )

    with col2:

        st.markdown(
            f"## {format_price(tour['price'])}"
        )

        st.write(f"📍 **Điểm đến:** {tour['destination']}")
        st.write(f"⏱️ **Thời lượng:** {tour['duration']}")
        st.write(f"🏷️ **Loại tour:** {tour['category']}")
        st.write(f"👥 **Số khách tối đa:** {tour['max_people']} người")

        st.divider()

        if st.button(
            "🛒 ĐẶT TOUR NGAY",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "booking"
            st.rerun()

    st.divider()

    st.subheader("📝 Giới thiệu")

    st.write(tour["description"])

    st.subheader("🗓️ Lịch trình")

    schedule_lines = tour["schedule"].split("\n")

    for line in schedule_lines:
        st.write(f"• {line}")


# ============================================================
# TRANG ĐẶT TOUR
# ============================================================

def booking_page():

    tour_id = st.session_state.selected_tour
    tour = get_tour(tour_id)

    if not tour:
        st.error("Không tìm thấy thông tin tour.")
        return

    st.title("🛒 Đặt tour")

    col1, col2 = st.columns([1, 2])

    with col1:

        st.image(
            tour["image"],
            use_container_width=True
        )

        st.markdown(f"### {tour['name']}")
        st.write(f"📍 {tour['destination']}")
        st.write(f"⏱️ {tour['duration']}")

        st.markdown(
            f"**Giá:** {format_price(tour['price'])}/người"
        )

    with col2:

        st.subheader("👤 Thông tin khách hàng")

        with st.form("booking_form"):

            customer_name = st.text_input(
                "Họ và tên *",
                placeholder="Nguyễn Văn A"
            )

            phone = st.text_input(
                "Số điện thoại *",
                placeholder="0901234567"
            )

            email = st.text_input(
                "Email",
                placeholder="email@example.com"
            )

            col_a, col_b = st.columns(2)

            with col_a:
                people = st.number_input(
                    "Số lượng khách *",
                    min_value=1,
                    max_value=tour["max_people"],
                    value=2,
                    step=1
                )

            with col_b:
                departure_date = st.date_input(
                    "Ngày khởi hành *",
                    min_value=date.today()
                )

            payment_method = st.selectbox(
                "Phương thức thanh toán",
                [
                    "Thanh toán tại văn phòng",
                    "Chuyển khoản ngân hàng",
                    "Thanh toán online"
                ]
            )

            note = st.text_area(
                "Ghi chú",
                placeholder="Yêu cầu đặc biệt nếu có..."
            )

            total_price = tour["price"] * people

            st.markdown("---")

            st.markdown(
                f"### 💰 Tổng thanh toán: "
                f"{format_price(total_price)}"
            )

            agree = st.checkbox(
                "Tôi xác nhận thông tin đặt tour là chính xác."
            )

            submitted = st.form_submit_button(
                "🎫 XÁC NHẬN ĐẶT TOUR",
                type="primary",
                use_container_width=True
            )

            if submitted:

                errors = []

                if not customer_name.strip():
                    errors.append("Vui lòng nhập họ và tên.")

                if not phone.strip():
                    errors.append("Vui lòng nhập số điện thoại.")

                if len(phone.strip()) < 9:
                    errors.append(
                        "Số điện thoại không hợp lệ."
                    )

                if not agree:
                    errors.append(
                        "Vui lòng xác nhận thông tin đặt tour."
                    )

                if errors:

                    for error in errors:
                        st.error(error)

                else:

                    booking_code = create_booking(
                        tour_id=tour["id"],
                        customer_name=customer_name.strip(),
                        phone=phone.strip(),
                        email=email.strip(),
                        people=people,
                        departure_date=departure_date.strftime(
                            "%d/%m/%Y"
                        ),
                        payment_method=payment_method,
                        note=note.strip(),
                        total_price=total_price
                    )

                    st.session_state.booking_code = booking_code
                    st.session_state.page = "success"
                    st.rerun()


# ============================================================
# TRANG ĐẶT TOUR THÀNH CÔNG
# ============================================================

def success_page():

    booking_code = st.session_state.booking_code

    if not booking_code:
        st.session_state.page = "home"
        st.rerun()

    booking = get_booking(booking_code)

    if not booking:
        st.error("Không tìm thấy đơn đặt tour.")
        return

    st.markdown(
        """
        <div class="success-box">
            <h2>🎉 Đặt tour thành công!</h2>
            <p>
                Cảm ơn bạn đã lựa chọn VietTour.
                Nhân viên sẽ liên hệ để xác nhận thông tin.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        ### 🎫 Mã đặt tour: `{booking['booking_code']}`
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 👤 Thông tin khách hàng")

        st.write(
            f"**Họ tên:** {booking['customer_name']}"
        )

        st.write(
            f"**Số điện thoại:** {booking['phone']}"
        )

        st.write(
            f"**Email:** {booking['email'] or 'Không có'}"
        )

        st.write(
            f"**Số khách:** {booking['people']}"
        )

    with col2:

        st.markdown("### 🗺️ Thông tin tour")

        st.write(
            f"**Tour:** {booking['tour_name']}"
        )

        st.write(
            f"**Ngày khởi hành:** {booking['departure_date']}"
        )

        st.write(
            f"**Thanh toán:** {booking['payment_method']}"
        )

        st.write(
            f"**Tổng tiền:** {format_price(booking['total_price'])}"
        )

        st.write(
            f"**Trạng thái:** {booking['status']}"
        )

    st.divider()

    st.info(
        "Vui lòng lưu mã đặt tour để tra cứu hoặc liên hệ "
        "với VietTour khi cần hỗ trợ."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🏠 Về trang chủ",
            use_container_width=True
        ):
            st.session_state.page = "home"
            st.rerun()

    with col2:
        if st.button(
            "🔎 Tra cứu đơn",
            use_container_width=True
        ):
            st.session_state.page = "lookup"
            st.rerun()


# ============================================================
# TRA CỨU ĐƠN
# ============================================================

def lookup_page():

    st.title("🔎 Tra cứu đặt tour")

    st.write(
        "Nhập mã đặt tour để xem thông tin đơn hàng."
    )

    booking_code = st.text_input(
        "Mã đặt tour",
        placeholder="Ví dụ: VT260928ABC123"
    )

    if st.button(
        "🔎 Tra cứu",
        type="primary"
    ):

        if not booking_code.strip():

            st.warning(
                "Vui lòng nhập mã đặt tour."
            )

        else:

            booking = get_booking(
                booking_code.strip().upper()
            )

            if not booking:

                st.error(
                    "Không tìm thấy đơn đặt tour."
                )

            else:

                st.success(
                    "Đã tìm thấy đơn đặt tour."
                )

                st.markdown(
                    f"## 🎫 {booking['booking_code']}"
                )

                st.write(
                    f"**Tour:** {booking['tour_name']}"
                )

                st.write(
                    f"**Điểm đến:** {booking['destination']}"
                )

                st.write(
                    f"**Khách hàng:** {booking['customer_name']}"
                )

                st.write(
                    f"**Số khách:** {booking['people']}"
                )

                st.write(
                    f"**Ngày khởi hành:** "
                    f"{booking['departure_date']}"
                )

                st.write(
                    f"**Tổng tiền:** "
                    f"{format_price(booking['total_price'])}"
                )

                st.write(
                    f"**Trạng thái:** {booking['status']}"
                )

                if booking["status"] != "Đã hủy":

                    st.divider()

                    if st.button(
                        "❌ Hủy đặt tour",
                        type="secondary"
                    ):

                        cancel_booking(
                            booking["booking_code"]
                        )

                        st.success(
                            "Đã hủy đơn đặt tour."
                        )

                        st.rerun()


# ============================================================
# TRANG QUẢN LÝ
# ============================================================

def admin_page():

    st.title("📊 Quản lý đơn đặt tour")

    st.warning(
        "Đây là khu vực quản lý demo. "
        "Khi triển khai thực tế cần bổ sung hệ thống đăng nhập quản trị."
    )

    bookings = get_all_bookings()

    if not bookings:

        st.info("Chưa có đơn đặt tour.")
        return

    # Thống kê
    total_bookings = len(bookings)

    confirmed = len([
        x for x in bookings
        if x["status"] == "Đã xác nhận"
    ])

    pending = len([
        x for x in bookings
        if x["status"] == "Chờ xác nhận"
    ])

    cancelled = len([
        x for x in bookings
        if x["status"] == "Đã hủy"
    ])

    revenue = sum(
        x["total_price"]
        for x in bookings
        if x["status"] != "Đã hủy"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Tổng đơn",
        total_bookings
    )

    col2.metric(
        "Chờ xác nhận",
        pending
    )

    col3.metric(
        "Đã xác nhận",
        confirmed
    )

    col4.metric(
        "Đã hủy",
        cancelled
    )

    col5.metric(
        "Doanh thu",
        format_price(revenue)
    )

    st.divider()

    st.subheader("📋 Danh sách đơn đặt tour")

    for booking in bookings:

        with st.expander(
            f"🎫 {booking['booking_code']} "
            f"— {booking['customer_name']} "
            f"— {booking['status']}"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Tour:** {booking['tour_name']}"
                )

                st.write(
                    f"**Khách hàng:** "
                    f"{booking['customer_name']}"
                )

                st.write(
                    f"**Điện thoại:** "
                    f"{booking['phone']}"
                )

                st.write(
                    f"**Email:** "
                    f"{booking['email'] or 'Không có'}"
                )

            with col2:

                st.write(
                    f"**Số khách:** "
                    f"{booking['people']}"
                )

                st.write(
                    f"**Ngày đi:** "
                    f"{booking['departure_date']}"
                )

                st.write(
                    f"**Thanh toán:** "
                    f"{booking['payment_method']}"
                )

                st.write(
                    f"**Tổng tiền:** "
                    f"{format_price(booking['total_price'])}"
                )

            if booking["note"]:

                st.info(
                    f"📝 Ghi chú: {booking['note']}"
                )


# ============================================================
# FOOTER
# ============================================================

def footer():

    st.markdown(
        """
        <div class="footer">
            <hr>
            <p>
                🌴 <b>VietTour</b> – Nền tảng đặt tour du lịch
            </p>
            <p>
                © 2026 VietTour. All rights reserved.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN
# ============================================================

def main():

    init_database()
    load_css()
    sidebar()

    if st.session_state.page == "home":
        home_page()

    elif st.session_state.page == "tours":
        tours_page()

    elif st.session_state.page == "detail":
        detail_page()

    elif st.session_state.page == "booking":
        booking_page()

    elif st.session_state.page == "success":
        success_page()

    elif st.session_state.page == "lookup":
        lookup_page()

    elif st.session_state.page == "admin":
        admin_page()

    else:
        home_page()

    footer()


if __name__ == "__main__":
    main()
