import streamlit as st
import google.generativeai as genai

# --- AYARLAR ---
SIFRE = "AIzaSyBsib1bPwnp2NZaUk7SHNCPXQlmFi04j4c"
genai.configure(api_key=SIFRE)

# --- YAPAY ZEKANIN KİMLİĞİ (GÜNCELLENDİ) ---
gizli_talimat = """
Navê te Bakıl e.
Tu asîstanekî zîrek, alîkar û Kurdîaxêv î.
Pêşdebirê te: HANİF TOPRAK. (Heke bipirsin tenê bibêje Hanif Toprak).

ÖNEMLİ TALİMAT (MEMLEKET):
Heke yek ji te bipirse "Tu xelkê ku derê yî?", "Ji ku derê yî?" an bi Tirkî "Nerelisin?", "Nereden geliyorsun?":
Cewaba te teqez ev be: "Ez ji Kurdistanê me" (Heke bi Tirkî pirsîbûn: "Ben Kürdistanlıyım").

Zimanê te yê sereke Kurdî ye, lê tu dikarî bi Tirkî jî biaxivî.
"""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=gizli_talimat)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="☀️", layout="centered", initial_sidebar_state="collapsed")

# --- SİNEMATİK TASARIM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600&display=swap');

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Montserrat', sans-serif;
        color: white;
    }
    header, footer, #MainMenu {visibility: hidden;}
    
    .baslik {
        font-size: 50px;
        font-weight: 600;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.3);
    }
    
    .alt-imza {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 10px;
        color: rgba(255,255,255,0.3);
        letter-spacing: 3px;
        z-index: 99;
        pointer-events: none;
    }

    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- ÖNERİ BUTONLARI (KÜRTÇE) ---
col1, col2, col3 = st.columns(3)
if col1.button("💡 Fikrekê Bide"):
    prompt = "Ji bo îro fikrekî cûda û xweş bide min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê fikirîn..."):
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

if col2.button("📝 Helbest"):
    prompt = "Li ser welat û hêvîyê helbesteke kurt binivîse."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê nivîsandin..."):
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

if col3.button("🧠 Agahî"):
    prompt = "3 agahiyên balkêş û kurt bêje min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê lêkolîn..."):
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()


# --- SOHBET GEÇMİŞİ VE AÇILIŞ MESAJI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ KUTUSU ---
if prompt := st.chat_input("Li vir binivîse..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            response = model.generate_content(prompt)
            placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            placeholder.error("Pirsgirêka girêdanê.")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
