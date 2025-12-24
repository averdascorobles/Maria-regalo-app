import streamlit as st
import time
from urllib.parse import quote

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Elige tu Aventura - María",
    page_icon="💖",
    layout="centered"
)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    /* Estilo de la Carta */
    .gift-card-container {
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        background-color: #FFF0F5;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        height: 100%; /* Altura flexible */
        min-height: 360px; /* Altura mínima asegurada */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 2px solid #FF4081;
        transition: all 0.3s ease;
    }
    
    /* Efecto Borroso (Bloqueado) */
    .locked {
        filter: blur(5px) grayscale(80%);
        opacity: 0.6;
        pointer-events: none;
    }
    
    /* Título flexible */
    .gift-title { 
        color: #C2185B; 
        font-weight: bold; 
        font-size: 17px; 
        margin-bottom: 8px; 
        min-height: 50px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        line-height: 1.3;
    }
    
    .gift-desc { 
        font-size: 13px; 
        color: #555; 
        margin-bottom: 10px; 
        flex-grow: 1; 
        display: flex; 
        align-items: center; 
        justify-content: center;
    }
    
    .gift-link { 
        text-decoration: none; 
        color: #FF4081; 
        font-weight: bold; 
        font-size: 12px;
        display: block;
        margin-top: auto; 
        padding-top: 5px;
    }

    /* Caja de Pregunta */
    .question-box {
        background-color: #E0F7FA;
        border: 2px solid #00BCD4;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 19px;
        font-weight: bold;
        color: #006064;
        margin-bottom: 20px;
    }

    /* Botones */
    div.stButton > button {
        width: 100%;
        min-height: 60px;
        height: auto !important;
        padding: 10px !important;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 500;
        white-space: pre-wrap;
        line-height: 1.4;
    }
    
    /* Candado */
    .lock-overlay {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        font-size: 40px;
        z-index: 10;
        text-shadow: 0 0 10px white;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATOS DE LOS REGALOS ---
GIFTS = [
    {
        "id": "Gastro",
        "title": "🕵️‍♀️ Gastro Escape Room",
        "desc": "Misterio y comida rica. Una experiencia diferente.",
        "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1000&auto=format&fit=crop",
        "link": "https://gastroescaperoom.com/menu"
    },
    {
        "id": "Taller",
        "title": "🎨 Taller Creativo",
        "desc": "Cerámica o Cocina. Tú eliges si mancharnos de barro o harina.",
        "img": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?q=80&w=1000&auto=format&fit=crop",
        "link": ""
    },
    {
        "id": "Espectaculo",
        "title": "🎭 Noche de Espectáculo",
        "desc": "Rey León, Monólogos o Teatro. Noche de cultura.",
        "img": "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?q=80&w=1000&auto=format&fit=crop",
        "link": ""
    },
    {
        "id": "Survivor",
        "title": "🏃‍♀️ Survivor Race (3km) 👀",  
        "desc": "Barro, obstáculos y risas. (Mi favorita, guiño guiño 😉).",
        "img": "https://images.unsplash.com/photo-1552674605-5d28c4e1902c?q=80&w=1000&auto=format&fit=crop",
        "link": "https://survivor-race.com"
    },
    {
        "id": "Santoku",
        "title": "🍣 Experiencia Santoku",
        "desc": "Alta cocina o experiencia gastronómica exclusiva.",
        "img": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?q=80&w=1000&auto=format&fit=crop",
        "link": "https://www.san-toku.es"
    }
]

# --- PREGUNTAS ---
questions = [
    {
        "q": "1. ¿En qué sitio he sido más feliz este año?",
        "options": ["Rio Pisuerga", "Bar Néstor", "Playa de Muro", "Hotel Aura Logroño"],
        "answer": "Bar Néstor",
        "error": "❌ Frío... Allí se come la tortilla (y chuleta) de los dioses."
    },
    {
        "q": "2. ¿Qué personalidad me ha durado más este año?",
        "options": ["Crossfiter", "Runner", "Padelista", "Todas las anteriores son correctas"],
        "answer": "Todas las anteriores son correctas",
        "error": "❌ ¡Te quedas corta! Soy un hombre polifacético (y me canso rápido)."
    },
    {
        "q": "3. Si tuviéramos un perro, ¿cómo se llamaría?",
        "options": ["Lalo", "Lala", "Lola", "Lolo"],
        "answer": "Lolo",
        "error": "❌ Casi... ¡tiene que hacer juego con mi nombre!"
    },
    {
        "q": "4. ¿Cuál es mi manía más rara?",
        "options": ["El orden extremo", "Cerrar las puertas con cuidado para que no haga ruido", "Dormir con calcetines", "Comer muy despacio"],
        "answer": "Cerrar las puertas con cuidado para que no haga ruido",
        "error": "❌ Ojalá fuera otra, pero no... soy el ninja de las puertas."
    },
    {
        "q": "5. Si me preguntas '¿Qué tal el día?', ¿cuál sería mi respuesta?",
        "options": [
            "Normal",
            "Obviamente te respondería contándote TODO lo que me ha pasado en el día sin dejarme ni un detalle",
            "Sin más",
            "Bien"
        ],
        "answer": "Bien",
        "error": "❌ Jajaja, ¡ojalá! Pero ya sabes que soy mucho más escueto."
    }
]

# --- ESTADO ---
if 'unlocked_count' not in st.session_state:
    st.session_state.unlocked_count = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'final_choice' not in st.session_state:
    st.session_state.final_choice = None

# --- FUNCIÓN DE DIBUJO ---
def draw_gifts():
    st.write("### 🎁 Tus Opciones (Desbloqueadas):")
    
    cols = st.columns(3)
    cols2 = st.columns(2)
    all_cols = cols + cols2 
    
    for i in range(5):
        gift = GIFTS[i]
        col = all_cols[i]
        is_unlocked = i < st.session_state.unlocked_count
        
        with col:
            # Construcción HTML por partes para evitar errores de renderizado
            css_class = "gift-card-container"
            if not is_unlocked:
                css_class += " locked"
            
            link_html = ""
            if gift['link'] and is_unlocked:
                link_html = f'<a href="{gift["link"]}" target="_blank" class="gift-link">Ver web 🔗</a>'
            
            lock_html = '<div class="lock-overlay">🔒</div>' if not is_unlocked else ''
            
            # HTML unido sin espacios para evitar bloque de código
            html_content = (
                f'<div style="position: relative;">'
                f'{lock_html}'
                f'<div class="{css_class}">'
                f'<div class="gift-title">{gift["title"]}</div>'
                f'<img src="{gift["img"]}" style="width:100%; height:120px; object-fit:cover; border-radius:10px;">'
                f'<div class="gift-desc">{gift["desc"]}</div>'
                f'{link_html}'
                f'</div>'
                f'</div>'
            )
            
            st.markdown(html_content, unsafe_allow_html=True)

# --- PANTALLA FINAL (ELECCIÓN REALIZADA) ---
if st.session_state.final_choice:
    st.balloons()
    chosen_gift = next(g for g in GIFTS if g['title'] == st.session_state.final_choice)
    
    st.title("💖 ¡Plan Elegido! 💖")
    st.success(f"Nos vamos a disfrutar de:")
    
    st.image(chosen_gift['img'], use_column_width=True)
    st.markdown(f"<h2 style='text-align:center; color:#E91E63'>{chosen_gift['title']}</h2>", unsafe_allow_html=True)
    
    # Mensajes personalizados
    if "Survivor" in chosen_gift['title']:
        st.info("😏 ¡Sabía que elegirías bien! Prepara las zapatillas viejas, que nos manchamos.")
    elif "Néstor" in chosen_gift['desc']: 
        st.info("🌮 ¡Tortilla time!")
    else:
        st.info("📅 ¡Hecho! Lo organizamos en cuanto quieras.")
        
    if chosen_gift['link']:
        st.write(f"🔗 [Ver detalles en su web]({chosen_gift['link']})")
    
    st.write("---")
    st.write("### 👇 PASO FINAL 👇")
    st.write("Avísame para que vaya reservando:")

    # --- BOTÓN DE WHATSAPP ---
    TU_NUMERO = "34633085734" 
    
    # Preparamos el mensaje
    mensaje = f"¡Hola Verdasco! Ya he decidido mi regalo: {chosen_gift['title']}. ¡Vamos a reservarlo! 😘"
    
    # Convertimos el mensaje para URL
    mensaje_url = quote(mensaje)
    whatsapp_link = f"https://wa.me/{TU_NUMERO}?text={mensaje_url}"
    
    st.link_button("📲 ENVIAR CONFIRMACIÓN A VERDASCO", whatsapp_link, type="primary")
    # -------------------------
    
    if st.button("🔄 Cambiar de opinión"):
        st.session_state.final_choice = None
        st.rerun()
    st.stop()

# --- INTERFAZ PRINCIPAL ---

st.title("💖 Para María 💖")
st.write("Demuestra cuánto me conoces para ver tus regalos.")

# 1. PARTE SUPERIOR: PREGUNTAS
if st.session_state.unlocked_count < 5:
    q_idx = st.session_state.current_q
    q_data = questions[q_idx]
    
    st.markdown(f'<div class="question-box">Pregunta {q_idx + 1}/5:<br>{q_data["q"]}</div>', unsafe_allow_html=True)
    
    options = q_data["options"]
    for opt in options:
        if st.button(opt, key=f"q{q_idx}_{opt}"):
            if opt == q_data["answer"]:
                st.toast("✅ ¡Correcto! Mira abajo 👇", icon="🔓")
                time.sleep(0.8)
                st.session_state.unlocked_count += 1
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error(q_data["error"])

# 2. PARTE SUPERIOR (ALTERNATIVA): SELECTOR FINAL
else:
    st.success("🎉 ¡TODO DESBLOQUEADO!")
    st.markdown("### 🧐 Momento de la verdad:")
    
    gift_titles = [g['title'] for g in GIFTS]
    choice = st.selectbox("Elige tu favorito:", gift_titles)
    
    st.write("")
    if st.button("🎁 CONFIRMAR ELECCIÓN", type="primary"):
        st.session_state.final_choice = choice
        st.rerun()

st.write("---")

# 3. PARTE INFERIOR: CARTAS DE REGALOS
draw_gifts()
