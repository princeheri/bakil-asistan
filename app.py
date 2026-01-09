import streamlit as st
import google.generativeai as genai

# --- AYARLAR ---
# Senin API Anahtarın
SIFRE = "AIzaSyBVPm17FHeyGFqu_dUuWcz6oXwdb-3sOq4"
genai.configure(api_key=SIFRE)

# --- MODEL AYARI ---
# En garantili ve uyumlu model
model = genai.GenerativeModel('gemini-1.5-flash')

# --- GİZLİ KİMLİK ---
GIZLI_KIMLIK = """
Senin adın Bakıl. 
Sen Kürtçe ve Türkçe bilen, çok zeki, yardımsever ve Kürdistanlı bir asistansın.
Geliştiricin: HANİF TOPRAK.
Eğer biri sana "Nerelisin?" derse kesinlikle "Kürdistanlıyım" de.
Cevapların kısa, net ve samimi olsun.
"""

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="🦁", layout="centered", initial_sidebar_state="collapsed")

# --- CSS TASARIM ---
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
    font-size: 50px; 
    font-weight: 600; 
    text-align: center; 
    color: #fcf6ba;
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

# --- ARAYÜZ ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Silav! Ez Bakıl im. Ez dikarim çawa alîkariya te bikim?"})

# Mesajları Ekrana Yaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
user_input = st.chat_input("Li vir binivîse...")

if user_input:
    # Kullanıcı mesajını ekle
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Yapay zeka yanıtı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            tam_prompt = GIZLI_KIMLIK + "\n\nKullanıcı dedi ki: " + user_input
            response = model.generate_content(tam_prompt)
            cevap_metni = response.text
            
            message_placeholder.markdown(cevap_metni)
            st.session_state.messages.append({"role": "assistant", "content": cevap_metni})

        except Exception as e:
            message_placeholder.error(f"Hata: {e}")

st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
