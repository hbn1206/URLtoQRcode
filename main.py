import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

# 사용자 조정 상수 (원본 그대로)
BOX_SIZE = 10
BORDER = 4
DEFAULT_QR_COLOR = 'black'
DEFAULT_BG_COLOR = 'white'

st.set_page_config(page_title="QR 코드 생성기", page_icon="🔗")

st.title("🔗 QR 코드 생성기")

# URL 입력
url = st.text_input("URL 입력")

# 색상 선택
col1, col2 = st.columns(2)
with col1:
    qr_color = st.color_picker("QR 색상", DEFAULT_QR_COLOR)
with col2:
    bg_color = st.color_picker("배경색", DEFAULT_BG_COLOR)

# QR 생성 버튼
if st.button("QR 생성"):
    if not url.strip():
        st.warning("URL을 입력하세요.")
    else:
        try:
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=BOX_SIZE,
                border=BORDER,
            )
            qr.add_data(url.strip())
            qr.make(fit=True)

            img = qr.make_image(
                fill_color=qr_color,
                back_color=bg_color
            ).convert("RGB")

            # 세션에 저장 (다운로드용)
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            st.session_state["qr_image"] = buf

            st.image(img, caption="생성된 QR 코드", width=350)

        except Exception as e:
            st.error(f"QR 생성 중 오류 발생: {e}")

# 다운로드 버튼
if "qr_image" in st.session_state:
    st.download_button(
        label="PNG로 저장",
        data=st.session_state["qr_image"],
        file_name="qr_code.png",
        mime="image/png"
    )
