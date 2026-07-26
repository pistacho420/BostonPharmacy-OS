import streamlit as st
import os

from database.database import (
    update_profile_image,
    get_achievements
)


def show_profile():

    user = st.session_state.user

    # Profile Picture
    if user["profile_image"]:

        if os.path.exists(user["profile_image"]):

            st.image(
                user["profile_image"],
                width=200
            )

        else:

            st.info("📷 Upload your picture")

    else:

        st.info("📷 Upload your picture")

    st.header(
        f"👨‍🎓 Welcome {user['full_name']}"
    )

    st.caption(
        "🏥 Boston Pharmacy Training Academy"
    )


    st.divider()
    st.divider()


    col1, col2 = st.columns(2)


    with col1:


        st.subheader(
            "📷 Profile Picture"
        )


        image = st.file_uploader(
            "Upload your picture",
            type=[
                "png",
                "jpg",
                "jpeg"
            ]
        )


        if image:


            folder = "profiles"


            if not os.path.exists(folder):

                os.makedirs(folder)


            path = os.path.join(
                folder,
                image.name
            )


            with open(path, "wb") as f:

                f.write(
                    image.getbuffer()
                )


            update_profile_image(
                user["id"],
                path
            )


            st.image(
                path,
                width=200
            )


    with col2:


        st.subheader(
            "📊 Student Progress"
        )


        st.metric(
            "⭐ XP",
            user["xp"]
        )
        xp = user["xp"]


        if xp < 100:

            nivel = "🌱 Pharmacy Beginner"


        elif xp < 300:

            nivel = "💊 Pharmacy Student"


        elif xp < 600:

            nivel = "🧪 Pharmacy Technician Trainee"


        else:

            nivel = "🏆 Pharmacy Technician Master"



        st.subheader(
            nivel
        )


        progreso = min(
            xp / 1000,
            1.0
        )


        st.progress(
            progreso
        )


        st.write(
            f"{xp} / 1000 XP"
        )

        st.write(
            "📚 Progress:"
        )


        st.write(
            "PTCB Practice Exam ✅"
        )


        st.write(
            "📝 PTCB Attempts:"
        )


        st.write(
            user["ptcb_attempts"]
        )

    st.divider()
    st.subheader(
        "📊 PTCB Analytics"
    )
    st.divider()

    st.subheader(
        "🧠 PTCB Study Recommendations"
    )


    if "ptcb_errors" in st.session_state and st.session_state.ptcb_errors:

        errores = st.session_state.ptcb_errors


        for area, cantidad in errores.items():

            st.warning(
                f"⚠️ {area}: {cantidad} incorrect answers - Review this topic"
            )


    else:

        st.success(
            "🎉 Great! No weak areas detected yet."
        )
        st.metric(
            "📝 Exams Completed",
            user["ptcb_attempts"]
        )

        st.metric(
            "🎯 Best Score",
            f"{user['ptcb_best_score']}%"
        )

        st.metric(
            "✅ Correct Answers",
            user["ptcb_correct"]
        )

        st.metric(
            "❌ Wrong Answers",
            user["ptcb_wrong"]
        )

        st.write(
            "🏆 Achievements:"
        )
        achievements = get_achievements(
            user["id"]
        )

        if achievements:
            for item in achievements:
                st.success(
                    item["achievement"]
                )
        else:
            st.info(
                "No achievements yet. Keep studying 💊"
            )

        if user["ptcb_passed"]:
            st.success(
                "🎓 PTCB Ready"
            )
        else:
            st.info(
                "Keep studying 💊"
            )