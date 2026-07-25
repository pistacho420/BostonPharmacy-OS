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
        caso["opciones"],
        key="med_answer"
    )



    if st.button(
        "Check Answer",
        key="btn_medication"
    ):



        if caso["opciones"].index(respuesta) == caso["correcta"]:



            progreso.correct_answer(10)


            progreso.complete_module(
                "Module 5 - Medication Knowledge"
            )


            st.success(
                "✅ Correct! +10 XP"
            )


            st.balloons()



        else:



            progreso.wrong_answer()


            st.error(
                "❌ Incorrect"
            )