import streamlit as st
import random

from data.medications import medicamentos


def modulo_medicamentos(progreso):

    st.header("💊 Medication Knowledge")

    caso = random.choice(medicamentos)


    st.info(
        f"""
💊 Medication: {caso['nombre']} {caso['strength']}

📌 Form: {caso['forma']}

🩺 Used for: {caso['uso']}
"""
    )


    st.subheader(caso["pregunta"])


    respuesta = st.radio(
        "Choose the correct answer:",
        caso["opciones"]
    )


    if st.button("Check Answer"):

        if caso["opciones"].index(respuesta) == caso["correcta"]:

            st.success("✅ Correct! +10 XP")

            progreso["xp"] += 10
            progreso["correctas"] += 1
            progreso["racha"] += 1


        else:

            st.error("❌ Incorrect")

            progreso["incorrectas"] += 1
            progreso["racha"] = 0


        st.session_state.progreso = progreso