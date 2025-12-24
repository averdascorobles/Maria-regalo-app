import streamlit as st
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Elige tu Aventura - María",
    page_icon="💖",
    layout="centered"
)

# --- ESTILOS CSS (Cartas de Regalo y Diseño Romántico) ---
st.markdown("""
    <style>
    /* Estilo de la Carta DESBLOQUEADA */
    .gift-card {
        border: 2px solid #FF4081;
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        background-color: #FFF0F5; /* Rosa muy suave */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        height: 320px; /* Altura fija para que queden alineadas */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s;
    }
    .gift-card:hover { transform: scale(1.02); }
    
    .gift-title { color: #C2185B; font-weight: bold; font-size: 18px; margin-bottom: 5px; height: 50px; display: flex; align-items: center; justify-content: center;}
    .gift-desc { font-size: 14px; color: #555; margin-bottom: 10px; height: 60px; overflow: hidden;}
    .gift-link { text-decoration: none; color: #FF4081; font-weight: bold; font-size: 12px;}

    /* Estilo de la Carta BLOQUEADA */
    .locked-card {
        border: 2px dashed #999;
        border-radius: 15px;
        height: 320px;
        background-color: #eee;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #777;
    }
    .lock-icon { font-size: 50px; margin-bottom: 10px; }

    /* Caja de Pregunta */
    .question-box {
        background-color: #E0F7FA;
        border: 2px solid #00BCD4;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #006064;
        margin-bottom: 20px;
    }

    /* Botones */
    div.stButton > button {
        width: 100%;
        height: 50px !important;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATOS DE LOS REGALOS (Las opciones) ---
# He buscado imágenes genéricas de calidad para cada actividad
GIFTS = [
    {
        "id": "Gastro",
        "title": "🕵️‍♀️ Gastro Escape Room",
        "desc": "Misterio y comida rica. Una experiencia diferente para resolver y saborear.",
        "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1000&auto=format&fit=crop", # Restaurante misterioso
        "link": "https://gastroescaperoom.com/menu"
    },
    {
        "id": "Taller",
        "title": "🎨 Taller Creativo",
        "desc": "Cerámica o Cocina. Tú eliges si mancharnos de barro o de harina.",
        "img": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?q=80&w=1000&auto=format&fit=crop", # Cerámica
        "link": ""
    },
    {
        "id": "Espectaculo",
        "title": "🎭 Noche de Espectáculo",
        "desc": "El Rey León, Monólogos o Concierto Candlelight. Noche de cultura y emoción.",
        "img": "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?q=80&w=1000&auto=format&fit=crop", # Evento
        "link": ""
    },
    {
        "id": "Survivor",
        "title": "🏃‍♀️ Survivor Race (3km)",
        "desc": "Barro, obstáculos y risas (o sufrimiento) juntos. ¿Aceptas el reto?",
        "img": "https://images.unsplash.com/photo-1552674605-5d28c4e1902c?q=80&w=1000&auto=format&fit=crop", # Carrera obstáculos
        "link": "https://survivor-race.com"
    },
    {
        "id": "Santoku",
        "title": "🍣 Experiencia Santoku",
        "desc": "Alta cocina o experiencia gastronómica exclusiva que te mereces.",
        "img": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?q=80&w=1000&auto=format&fit=crop", # Sushi top
        "link": "https://www.san-toku.es"
    }
]

# --- PREGUNTAS SOBRE VUESTRA RELACIÓN (¡EDITA ESTO!) ---
questions = [
    {
        "q": "1. Para desbloquear el primer regalo... ¿Cuál es mi comida favorita?",
        "options": ["Pizza", "Sushi", "Hamburguesa", "Lentejas"],
        "answer": "Sushi", # <--- CAMBIA ESTO
        "error": "❌ ¡Qué va! Eso me gusta, pero no es la favorita."
    },
    {
        "q": "2. ¿Dónde fue nuestro primer viaje/escapada juntos?",
        "options": ["Madrid", "Playa", "Montaña", "París"],
        "answer": "Playa", # <--- CAMBIA ESTO
        "error": "❌ ¡Ay qué memoria! Inténtalo de nuevo."
    },
    {
        "q": "3. Si tuviéramos un perro ahora mismo, ¿cómo le llamaría yo?",
        "options": ["Toby", "Thor", "Coco", "Rex"],
        "answer": "Thor", # <--- CAMBIA ESTO
        "error": "❌ Nop. Ese nombre no me pega."
    },
    {
        "q": "4. ¿Cuál es mi manía más rara?",
        "options": ["El orden", "Ruidos al comer", "Dormir con calcetines", "Morder el boli"],
        "answer": "El orden", # <--- CAMBIA ESTO
        "error": "❌ Jaja, ojalá fuera esa, pero no."
    },
    {
        "q": "5. Última para desbloquear todo: ¿Cuánto te quiero?",
        "options": ["Mucho", "Muchísimo", "Infinito", "Más que ayer pero menos que mañana"],
        "answer": "Más que ayer pero menos que mañana", # <--- CAMBIA ESTO
        "error": "❌ Todas son verdad, pero busco la más cursi."
    }
]

# --- ESTADO ---
if 'unlocked_count' not in st.session_state:
    st.session_state.unlocked_count = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'final_choice' not in st.session_state:
    st.session_state.final_choice = None

# --- FUNCIÓN PARA DIBUJAR LAS CARTAS ---
def draw_gifts():
    st.write("### 🎁 Tus Opciones de Regalo:")
    
    # Organizamos en filas de 3 y 2
    cols = st.columns(3)
    cols2 = st.columns(2)
    all_cols = cols + cols2 # Lista de 5 columnas
    
    for i in range(5):
        gift = GIFTS[i]
        col = all_cols[i]
        
        with col:
            if i < st.session_state.unlocked_count:
                # CARTA DESBLOQUEADA
                st.markdown(f"""
                <div class="gift-card">
                    <div class="gift-title">{gift['title']}</div>
                    <img src="{gift['img']}" style="width:100%; height:120px; object-fit:cover; border-radius:10px;">
                    <div class="gift-desc">{gift['desc']}</div>
                    <a href="{gift['link']}" target="_blank" class="gift-link">Ver web 🔗</a>
                </div>
                """, unsafe_allow_html=True)
            else:
                # CARTA BLOQUEADA
                st.markdown(f"""
                <div class="locked-card">
                    <div class="lock-icon">🔒</div>
                    <div>Opción {i+1}</div>
                    <small>Responde para abrir</small>
                </div>
                """, unsafe_allow_html=True)

# --- PANTALLA FINAL (ELECCIÓN HECHA) ---
if st.session_state.final_choice:
    st.balloons()
    
    # Buscar datos del regalo elegido
    chosen_gift = next(g for g in GIFTS if g['title'] == st.session_state.final_choice)
    
    st.title("💖 ¡Regalo Elegido! 💖")
    st.success(f"Has decidido que nos vamos a disfrutar de:")
    
    st.image(chosen_gift['img'], use_column_width=True)
    st.markdown(f"<h2 style='text-align:center; color:#E91E63'>{chosen_gift['title']}</h2>", unsafe_allow_html=True)
    
    if chosen_gift['id'] == "Survivor":
        st.info("👟 Prepárate para ensuciarte y pasarlo en grande. ¡Yo voy contigo!")
    elif chosen_gift['id'] == "Santoku":
        st.info("🍣 Prepara el paladar, va a ser increíble.")
    else:
        st.info("📅 ¡Pues decidido! Lo organizamos para cuando tú me digas.")
        
    st.write(f"🔗 [Ver más detalles en su web]({chosen_gift['link']})")
    
    if st.button("🔄 Volver a pensar"):
        st.session_state.final_choice = None
        st.rerun()
    st.stop()

# --- INTERFAZ PRINCIPAL ---

st.title("💖 Para María 💖")
st.write("Tengo un regalo para ti, pero... ¡tienes que elegirlo tú!")
st.write("Responde a las preguntas para desbloquear las 5 opciones ocultas.")

# DIBUJAR CARTAS
draw_gifts()

st.write("---")

# FASE DE TRIVIAL
if st.session_state.unlocked_count < 5:
    q_idx = st.session_state.current_q
    q_data = questions[q_idx]
    
    st.markdown(f'<div class="question-box">Pregunta {q_idx + 1}/5:<br>{q_data["q"]}</div>', unsafe_allow_html=True)
    
    col_opts = st.columns(2)
    options = q_data["options"]
    
    for i, opt in enumerate(options):
        # Distribuir botones en 2 columnas
        if col_opts[i % 2].button(opt, key=f"q{q_idx}_{i}"):
            if opt == q_data["answer"]:
                st.toast("✅ ¡Correcto! Una opción desbloqueada.", icon="🔓")
                time.sleep(1)
                st.session_state.unlocked_count += 1
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error(q_data["error"])

# FASE DE ELECCIÓN FINAL
else:
    st.success("🎉 ¡ENHORABUENA! Has desbloqueado todas las opciones.")
    st.markdown("### 🧐 Ha llegado el momento de decidir:")
    
    # Selector final
    gift_titles = [g['title'] for g in GIFTS]
    choice = st.selectbox("Elige tu regalo favorito:", gift_titles)
    
    st.write("")
    if st.button("🎁 CONFIRMAR ESTE REGALO", type="primary"):
        st.session_state.final_choice = choice
        st.rerun()
