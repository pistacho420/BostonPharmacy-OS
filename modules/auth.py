import streamlit as st

from database.database import register_user, login_user



def login_screen():


    st.title("💊 BostonPharmacy-OS")

    st.subheader(
        "Pharmacy Technician Training Platform"
    )


    opcion = st.radio(
        "Select option:",
        [
            "Login",
            "Create Account"
        ]
    )


    if opcion == "Create Account":


        st.header("👤 Create Student Account")


        name = st.text_input(
            "Full Name"
        )


        email = st.text_input(
            "Email"
        )


        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "Register"
        ):


            result = register_user(
                name,
                email,
                password
            )


            if result:

                st.success(
                    "✅ Account created successfully"
                )

            else:

                st.error(
                    "❌ Email already registered"
                )



    else:


        st.header(
            "🔐 Student Login"
        )


        email = st.text_input(
            "Email"
        )


        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "Login"
        ):


            user = login_user(
                email,
                password
            )


            if user:


                st.session_state.user = dict(user)

                st.success(
                    "Welcome to BostonPharmacy-OS"
                )

                st.rerun()


            else:

                st.error(
                    "Invalid email or password"
                )