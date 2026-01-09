import streamlit as st
import google.generativeai as genai

# --- AYARLAR ---
SIFRE = "AIzaSyBsib1bPwnp2NZaUk7SHNCPXQlmFi04j4c"
genai.configure(api_key=SIFRE)

# --- MODEL AYARI ---
# Hata vermeyen, en hızlı model:
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BAKIL'IN KİMLİĞİ ---
gizli_talimat = """
Navê te Bakıl e.
Tu asîstanekî zîrek, alîkar û Kurdîaxêv î.
Pêşdebirê te: HANİF TOPRAK. (Heke bipirsin tenê bibêje Hanif Toprak).

ÖNEMLİ TALİMAT (MEMLEKET):
Heke yek ji te bipirse "Tu xelkê ku derê yî?", "Ji ku derê yî?" an bi Tirkî "Nerelisin?", "Nereden geliyorsun?":
Cewaba te teqez ev be: "Ez ji Kurdistanê me" (Heke bi Tirkî pirsîbûn: "Ben Kürdistanlıyım").

Zimanê te yê sereke Kurdî ye, lê tu dikarî bi Tirkî jî biaxivî.
Cewabên te kurt û zelal bin.
"""

# Sohbeti başlat (Kimliği yükle)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[
        {"role": "user", "parts": [gizli_talimat]},
        {"role": "model", "parts": ["Fêm bû. Ez Bakıl im."]}
    ])

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="☀️", layout="centered", initial_sidebar_state="collapsed")

# --- TASARIM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600&display=swap');
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        font-family: 'Montserrat', sans-serif;
        color: white;
    }
    header, footer, #MainMenu {visibility: hidden;}
    .baslik {
        font-size: 50px; font-weight: 600; text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .alt-imza {
        position: fixed; bottom: 10px; left: 0; width: 100%; text-align: center;
        font-size: 10px; color: rgba(255,255,255,0.3); letter-spacing: 3px;
        z-index: 99; pointer-events: none;
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- BUTONLAR VE GİRİŞ MANTIĞI ---
# Burada değişkeni temizliyoruz ki karışıklık çıkmasın
prompt_to_send = None

# Butonlar
col1, col2, col3 = st.columns(3)
if col1.button("💡 Fikrekê Bide"):
    prompt_to_send = "Ji bo îro fikrekî cûda û xweş bide min."
if col2.button("📝 Helbest"):
    prompt_to_send = "Li ser welat û hêvîyê helbesteke kurt binivîse."
if col3.button("🧠 Agahî"):
    prompt_to_send = "3 agahiyên balkêş û kurt bêje min."

# Klavye Girişi
chat_input_val = st.chat_input("Li vir binivîse...")
if chat_input_val:
    prompt_to_send = chat_input_val

# --- MESAJI GÖNDERME VE CEVAP ALMA ---
if prompt_to_send:
    # 1. Kullanıcı mesajını ekrana bas ve kaydet
    st.chat_message("user").markdown(prompt_to_send)
    st.session_state.messages.append({"role": "user", "content": prompt_to_send})

    # 2. Yapay zekaya gönder
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")
        try:
            # İşte o hatayı önleyen kısım: Sadece temiz metin gönderiyoruz
            response = st.session_state.chat_session.send_message(prompt_to_send)
            cevap = response.text
            
            placeholder.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
            
            # Butona basıldıysa sayfayı yenile ki mesaj düzgün görünsün
            if chat_input_val is None: 
                st.rerun()
                
        except Exception as e:
            placeholder.error(f"Hata oluştu: {e}")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
