import qrcode

custom_url = "https://c-s-bohuslavsky.streamlit.app/"


img = qrcode.make(custom_url)


img.save("wedding_quiz_QR_code.png")