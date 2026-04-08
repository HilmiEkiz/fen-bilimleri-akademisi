import streamlit as st
import random

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Fen Bilimleri Akademisi", layout="wide")

# --- VERİ BANKASI (Kitabındaki 7 Üniteye Göre) ---
UNIT_DATA = {
    "1. Mevsimler ve İklim": {
        "match": {"Eksen Eğikliği": "Mevsimlerin oluşma sebebi", "Klimatolog": "İklim bilimci", "Hava Olayı": "Dar alanda kısa süreli olay"},
        "true_false": [("Dünya Güneş'e en yakın olduğunda yaz yaşanır.", False), ("İklim, uzun süreli hava olaylarının ortalamasıdır.", True)]
    },
    "2. DNA ve Genetik Kod": {
        "match": {"Nükleotid": "DNA'nın yapı birimi", "Gen": "DNA'nın görev birimi", "Kromozom": "DNA'nın paketlenmiş hali"},
        "true_false": [("Adenin nükleotidi karşısına Guanin gelir.", False), ("Mutasyonlar her zaman zararlıdır.", False)]
    },
    "3. Basınç": {
        "match": {"Pascal Prensibi": "Sıvıların basıncı iletmesi", "Barometre": "Açık hava basıncı ölçer", "Yüzey Alanı": "Katı basıncını azaltan faktör"},
        "true_false": [("Sıvı basıncı derinliğe bağlıdır.", True), ("Ters çevrilen bardağın basıncı artar.", True)]
    },
    "4. Madde ve Endüstri": {
        "match": {"Öz Isı": "Madde için ayırt edici özellik", "Asit": "pH değeri 7'den küçük", "Baz": "Ele kayganlık hissi verir"},
        "true_false": [("Limon suyu bazik bir maddedir.", False), ("Periyodik tabloda 18 grup vardır.", True)]
    },
    "5. Basit Makineler": {
        "match": {"Sabit Makara": "Yoldan kazanç sağlamaz", "Eğik Düzlem": "Kuvvetten kazanç sağlar", "Destek": "Kaldıraçların dönme noktası"},
        "true_false": [("Basit makineler işten kazanç sağlar.", False), ("Makas bir çift taraflı kaldıracıdır.", True)]
    },
    "6. Enerji Dönüşümleri": {
        "match": {"Fotosentez": "Besin üretme olayı", "Besin Zinciri": "Enerji aktarım yolu", "Ayrıştırıcılar": "Madde döngüsü halkası"},
        "true_false": [("Üreticiler güneş enerjisini kullanır.", True), ("Besin piramidinde yukarı çıkıldığında enerji artar.", False)]
    },
    "7. Elektrik Yükleri": {
        "match": {"Elektroskop": "Cismin yükünü belirler", "Topraklama": "Fazla yükün atılması", "Yalıtkan": "Elektriği iletmeyen madde"},
        "true_false": [("Zıt yükler birbirini iter.", False), ("Nötr bir cisimde yük yoktur.", False)]
    }
}

# --- HAFIZA (Session State) ---
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'sayfa' not in st.session_state: st.session_state.sayfa = "ana_menu"
if 'secili_unite' not in st.session_state: st.session_state.secili_unite = None

# --- ÜST PANEL ---
col_exit, col_title, col_score = st.columns([1, 4, 1])
with col_exit:
    if st.session_state.sayfa != "ana_menu":
        if st.button("❌ Çıkış"):
            if st.checkbox("Emin misin?"):
                st.session_state.sayfa = "ana_menu"
                st.rerun()
with col_score:
    st.metric("Puan", st.session_state.puan)

# --- ANA MENÜ ---
if st.session_state.sayfa == "ana_menu":
    st.title("🔬 8. Sınıf Fen Laboratuvarı")
    cols = st.columns(3)
    for i, unit in enumerate(UNIT_DATA.keys()):
        with cols[i % 3]:
            st.button(unit, key=unit, on_click=lambda u=unit: [st.session_state.update({"secili_unite": u, "sayfa": "unite_secim"})])

# --- ÜNİTE İÇİ OYUN SEÇİMİ ---
elif st.session_state.sayfa == "unite_secim":
    unit = st.session_state.secili_unite
    st.header(f"📚 {unit}")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🧩 Eşleştirme")
        if st.button("Oyna", key="match_btn"): st.session_state.sayfa = "game_match"; st.rerun()
    with c2:
        st.subheader("✅ Doğru mu?")
        if st.button("Oyna", key="tf_btn"): st.session_state.sayfa = "game_tf"; st.rerun()

# --- OYUN 1: EŞLEŞTİRME ---
elif st.session_state.sayfa == "game_match":
    unit = st.session_state.secili_unite
    data = UNIT_DATA[unit]["match"]
    st.info("Kavramları doğru tanımlarla eşleştir!")
    
    for k, v in data.items():
        ans = st.selectbox(f"**{k}** nedir?", ["Seçiniz...", *data.values()], key=k)
        if ans == v:
            st.success("Doğru!")
            if f"done_{k}" not in st.session_state:
                st.session_state.puan += 20
                st.session_state[f"done_{k}"] = True
                st.rerun()

# --- OYUN 2: DOĞRU / YANLIŞ ---
elif st.session_state.sayfa == "game_tf":
    unit = st.session_state.secili_unite
    questions = UNIT_DATA[unit]["true_false"]
    st.info("Cümle doğru mu yoksa yanlış mı?")
    
    for i, (q, a) in enumerate(questions):
        col_q, col_ans = st.columns([3, 1])
        col_q.write(f"{i+1}. {q}")
        user_a = col_ans.radio("Kararın:", ["?", "Doğru", "Yanlış"], key=f"tf_{i}")
        if (user_a == "Doğru" and a) or (user_a == "Yanlış" and not a):
            st.success("Bildin! +10 Puan")