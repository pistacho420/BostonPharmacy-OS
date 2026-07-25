# ============================================================
# PTCB PRACTICE EXAM MODULE
# BostonPharmacy-OS
# ============================================================

import streamlit as st
import random


from data.ptcb_questions import preguntas_ptcb


def modulo_ptcb(progreso):
    
    st.write("Total PTCB Questions:", len(preguntas_ptcb))

    st.header("📝 PTCB Practice Exam")
    
    st.subheader("🎓 Select Exam Mode")

    modo_examen = st.selectbox(
        "Choose exam type:",
        [
            "Quick Practice (10 Questions)",
            "Practice Exam (50 Questions)"
        ]
    )

    if modo_examen == "Quick Practice (10 Questions)":
        cantidad_preguntas = 10
    else:
        cantidad_preguntas = 50

    # Crear examen nuevo
    if "ptcb_questions" not in st.session_state:
        st.session_state.ptcb_questions = random.sample(
            preguntas_ptcb,
            min(cantidad_preguntas, len(preguntas_ptcb))
        )
        
        st.session_state.ptcb_index = 0
        st.session_state.ptcb_score = 0
        st.session_state.ptcb_finished = False

    st.write("Preguntas cargadas:", len(st.session_state.ptcb_questions))



    # Si terminó el examen
    if st.session_state.ptcb_finished:

        score = st.session_state.ptcb_score
        total = len(st.session_state.ptcb_questions)

        porcentaje = int((score / total) * 100)

        st.success("🎓 Exam Completed")
        st.divider()

        if porcentaje >= 80:
            st.success("🏆 STATUS: PASS")
            st.info("🎓 Congratulations! You are PTCB Ready!")
        else:
            st.error("❌ STATUS: FAIL")
            st.warning("📚 Review your weak areas and try again.")

        st.subheader("📊 Exam Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Correct Answers",
                score
            )

        with col2:
            st.metric(
                "Wrong Answers",
                total - score
            )

        with col3:
            st.metric(
                "Accuracy",
                f"{porcentaje}%"
            )

        st.metric(
            "Score",
            f"{score}/{total}"
        )

        st.metric(
            "Percentage",
            f"{porcentaje}%"
        )

        progreso.save_ptcb_result(
            score,
            total
        )

        if porcentaje >= 90:
            xp_ganado = 150
            st.balloons()
            st.success("🏆 Excellent! Pharmacy Master Level!")
        elif porcentaje >= 80:
            xp_ganado = 100
            st.success("✅ Passing Score - PTCB Ready!")
        elif porcentaje >= 60:
            xp_ganado = 50
            st.warning("📚 Good effort! Keep practicing.")
        else:
            xp_ganado = 0
            st.error("❌ Needs Improvement. Keep studying.")

        st.metric(
            "XP Earned",
            f"+{xp_ganado} XP"
        )

        if xp_ganado > 0:
            progreso.add_xp(xp_ganado)
        else:
            st.warning("📚 Keep studying. Try again!")

        if st.button("Restart Exam"):
            del st.session_state.ptcb_questions
            del st.session_state.ptcb_index
            del st.session_state.ptcb_score
            del st.session_state.ptcb_finished
            st.rerun()

        return


    # Pregunta actual

    pregunta = st.session_state.ptcb_questions[
        st.session_state.ptcb_index
    ]


    numero = st.session_state.ptcb_index + 1


    st.info(
        f"Question {numero} of {len(st.session_state.ptcb_questions)}"
    )


    st.subheader(
        pregunta["pregunta"]
    )


    respuesta = st.radio(
        "Choose the correct answer:",
        pregunta["opciones"],
        key=f"ptcb_{numero}"
    )



    if st.button(
        "Submit Answer",
        key=f"submit_{numero}"
    ):


        seleccion = pregunta["opciones"].index(respuesta)


        if seleccion == pregunta["correcta"]:

            st.success(
                "✅ Correct!"
            )

            st.session_state.ptcb_score += 1


        else:

            st.error(
                "❌ Incorrect"
            )


        st.info(
            f"📚 Explanation: {pregunta['explicacion']}"
        )


        if st.session_state.ptcb_index < len(
            st.session_state.ptcb_questions
        ) - 1:

            st.session_state.ptcb_index += 1


        else:

            st.session_state.ptcb_finished = True


        st.rerun()