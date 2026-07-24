import streamlit as st
import json
import os
import random
from modules.module5_medications import modulo_medicamentos

# ============================================================
# PAGE CONFIG & BACKGROUND
# ============================================================
st.set_page_config(page_title="BostonPharmacy-OS", page_icon="💊", layout="centered")
# ============================================================
# LOAD STUDENT PROGRESS
# ============================================================

archivo_progreso = "progress.json"
if os.path.exists(archivo_progreso):
    with open(archivo_progreso, "r") as file:
        progreso = json.load(file)

    # Crear datos nuevos si no existen
    if "xp" not in progreso:
        progreso["xp"] = 0

    if "correctas" not in progreso:
        progreso["correctas"] = 0

    if "incorrectas" not in progreso:
        progreso["incorrectas"] = 0

    if "racha" not in progreso:
        progreso["racha"] = 0

else:
    progreso = {
        "nombre": "Melvin",
        "xp": 0,
        "correctas": 0,
        "incorrectas": 0,
        "racha": 0
    }

st.markdown("""
<style>
.stApp { 
    background: radial-gradient(circle at center, #2f8fd1 0%, #1a5f9e 45%, #0d3b6b 100%);
}
[data-testid="stAppViewContainer"] > .main .block-container {
    background-color: rgba(255, 255, 255, 0.93);
    border-radius: 14px;
    padding: 2rem 2.5rem;
}
[data-testid="stSidebar"] {
    background-color: rgba(13, 59, 107, 0.92);
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

st.title("💊 BostonPharmacy-OS v2026")
st.subheader("Pharmacy Technician Training Simulator - Boston, MA")
st.write("---")
# ============================================================
# STUDENT PROGRESS
# ============================================================

st.sidebar.header("👨‍🎓 Mi Progreso")

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "correctas" not in st.session_state:
    st.session_state.correctas = 0

if "incorrectas" not in st.session_state:
    st.session_state.incorrectas = 0


nivel = "Beginner Pharmacy Technician"

if st.session_state.xp >= 100:
    nivel = "Intermediate Pharmacy Technician"

if st.session_state.xp >= 250:
    nivel = "Advanced Pharmacy Technician"

st.sidebar.write(f"🏆 XP: {st.session_state.xp}")
st.sidebar.write(f"✅ Correctas: {st.session_state.correctas}")
st.sidebar.write(f"❌ Incorrectas: {st.session_state.incorrectas}")
st.sidebar.write(f"🔥 Racha: {progreso['racha']}")
st.sidebar.write(f"🎓 Nivel: {nivel}")
# ============================================================
# CASE DATABASE
# ============================================================

# ---------- MODULE 1: DATA ENTRY & E-PRESCRIBING ----------
# Mix of tablets, capsules, and oral liquids (suspensions)
casos_m1 = [
    {"patient": "Sarah Johnson", "dob": "03/22/1990", "doctor": "Dr. Alan Reyes", "npi": "1122334455",
     "med": "Metformin 500mg tablets", "sig": "1 tab PO bid x 30 days", "qty": "60",
     "keywords": ["bid", "twice a day", "twice daily"], "dias": 30},

    {"patient": "Michael Chen", "dob": "07/09/1985", "doctor": "Dr. Elizabeth Smith", "npi": "1234567890",
     "med": "Amoxicillin 500mg capsules", "sig": "1 cap PO tid x 10 days", "qty": "30",
     "keywords": ["tid", "three times a day", "three times daily"], "dias": 10},

    {"patient": "Emily Rodriguez", "dob": "12/01/2018", "doctor": "Dr. Priya Nair", "npi": "1987654321",
     "med": "Amoxicillin 250mg/5mL oral suspension", "sig": "10 mL PO tid x 10 days", "qty": "300 mL",
     "keywords": ["tid", "three times a day", "three times daily"], "dias": 10},

    {"patient": "David Kim", "dob": "05/17/1978", "doctor": "Dr. James Carter", "npi": "1029384756",
     "med": "Lisinopril 10mg tablets", "sig": "1 tab PO qd x 30 days", "qty": "30",
     "keywords": ["qd", "once a day", "once daily"], "dias": 30},

    {"patient": "Jessica Martinez", "dob": "09/30/1995", "doctor": "Dr. Rebecca Hall", "npi": "1029384999",
     "med": "Cephalexin 500mg capsules", "sig": "1 cap PO q8h x 10 days", "qty": "30",
     "keywords": ["q8h", "every 8 hours"], "dias": 10},

    {"patient": "Robert Taylor", "dob": "02/14/2020", "doctor": "Dr. Priya Nair", "npi": "1987654321",
     "med": "Cephalexin 250mg/5mL oral suspension", "sig": "5 mL PO qid x 7 days", "qty": "140 mL",
     "keywords": ["qid", "four times a day", "four times daily"], "dias": 7},

    {"patient": "Amanda White", "dob": "06/25/1988", "doctor": "Dr. Alan Reyes", "npi": "1122334455",
     "med": "Prednisone 10mg tablets", "sig": "1 tab PO qid x 7 days", "qty": "28",
     "keywords": ["qid", "four times a day", "four times daily"], "dias": 7},

    {"patient": "Christopher Lee", "dob": "11/11/1992", "doctor": "Dr. James Carter", "npi": "1029384756",
     "med": "Fluoxetine 20mg capsules", "sig": "1 cap PO qd x 30 days", "qty": "30",
     "keywords": ["qd", "once a day", "once daily"], "dias": 30},

    {"patient": "Nicole Brown", "dob": "08/19/2021", "doctor": "Dr. Rebecca Hall", "npi": "1029384999",
     "med": "Acetaminophen (Children's) 160mg/5mL oral suspension", "sig": "5 mL PO q6h x 5 days", "qty": "100 mL",
     "keywords": ["q6h", "every 6 hours"], "dias": 5},

    {"patient": "Olivia Davis", "dob": "04/03/1975", "doctor": "Dr. Elizabeth Smith", "npi": "1234567890",
     "med": "Warfarin 5mg tablets", "sig": "1 tab PO qhs x 30 days", "qty": "30",
     "keywords": ["qhs", "at bedtime", "before bed"], "dias": 30},
]

# ---------- MODULE 2: INSURANCE BILLING (MASSHEALTH) ----------
casos_m2 = [
    {"patient": "John Doe", "rechazo": "'Prior Authorization Required' for Lipitor 20mg.",
     "opciones": ["Call the police.",
                  "Switch to a generic medication without notifying the doctor.",
                  "Notify the patient and send a fax/electronic alert to the doctor's office to process the authorization."],
     "correcta": 2,
     "explicacion": "The prescriber must justify the use to MassHealth through the Prior Authorization process."},

    {"patient": "Maria Gonzalez", "rechazo": "'Refill Too Soon' — patient requests early refill of Metformin.",
     "opciones": ["Override the rejection immediately without asking anything.",
                  "Ask the reason (travel, lost medication) and check with the pharmacist if an override applies.",
                  "Tell the patient to pay cash without any explanation."],
     "correcta": 1,
     "explicacion": "Always investigate the reason before an override; the pharmacist decides if it's appropriate."},

    {"patient": "Kevin Wright", "rechazo": "'Non-Formulary Drug' — the prescribed medication is not on the plan's formulary.",
     "opciones": ["Contact the prescriber to suggest a covered therapeutic alternative or request a formulary exception.",
                  "Dispense the drug and charge the difference without telling anyone.",
                  "Tell the patient to try another pharmacy."],
     "correcta": 0,
     "explicacion": "The technician coordinates with the doctor's office to find a covered alternative or request an exception."},

    {"patient": "Linda Park", "rechazo": "'Patient/Member Not Found' — the system doesn't recognize the patient's eligibility.",
     "opciones": ["Verify the insurance card information and confirm eligibility with MassHealth.",
                  "Assume the patient no longer has insurance and charge full price without checking.",
                  "Ignore the rejection and try again without changing anything."],
     "correcta": 0,
     "explicacion": "Data entry errors (ID, date of birth) are the most common cause; always verify before assuming no coverage."},

    {"patient": "Brian Scott", "rechazo": "'Quantity Limit Exceeded' — the prescribed quantity exceeds the plan's limit.",
     "opciones": ["Reduce the quantity without telling the doctor or the patient.",
                  "Check the plan's limit and contact the prescriber to request an override if clinically justified.",
                  "Cancel the prescription entirely."],
     "correcta": 1,
     "explicacion": "The technician requests quantity authorization from the doctor; clinical decisions are never made independently."},

    {"patient": "Angela Reed", "rechazo": "Drug Utilization Review (DUR) alert for a possible drug interaction.",
     "opciones": ["Dispense anyway because the system could be wrong.",
                  "Ignore the alert if the patient insists it's fine.",
                  "Alert the pharmacist immediately before continuing the dispensing process."],
     "correcta": 2,
     "explicacion": "DUR alerts related to interactions always require pharmacist review before dispensing."},

    {"patient": "Daniel Foster", "rechazo": "The prescription has expired (past its valid fill period).",
     "opciones": ["Dispense anyway because the patient urgently needs it.",
                  "Contact the doctor's office to obtain a new or renewed prescription.",
                  "Change the date in the system so it passes validation."],
     "correcta": 1,
     "explicacion": "Never dispense on an expired prescription or alter the date; a new one must be requested from the prescriber."},

    {"patient": "Rachel Adams", "rechazo": "The patient has two insurances and the claim was rejected for 'Coordination of Benefits'.",
     "opciones": ["Bill the primary insurance first, then the secondary for the remaining balance.",
                  "Bill only the secondary insurance because it's easier.",
                  "Charge the patient the full amount and let them file for reimbursement."],
     "correcta": 0,
     "explicacion": "Coordination of benefits requires billing the primary insurance first, then the secondary."},

    {"patient": "Steven Clark", "rechazo": "'NDC Not Covered' — the specific manufacturer's NDC is not covered by the plan.",
     "opciones": ["Check if a covered generic/equivalent NDC is available for substitution.",
                  "Charge the patient full price without looking for alternatives.",
                  "Leave the prescription unfilled indefinitely."],
     "correcta": 0,
     "explicacion": "Often the same drug from a different manufacturer (same generic) is covered."},

    {"patient": "Karen Bell", "rechazo": "Rejection due to a missing DAW (Dispense as Written) code on a brand-name prescription.",
     "opciones": ["Verify with the doctor if brand-name use is justified and enter the correct DAW code, or dispense the generic if allowed.",
                  "Enter a random DAW code so the system accepts it.",
                  "Dispense the brand without a code and have the pharmacy absorb the cost."],
     "correcta": 0,
     "explicacion": "The DAW code must accurately reflect the prescriber's instruction or the real clinical situation."},
]

# ---------- MODULE 3: CONTROLLED SUBSTANCES (MASSPAT) ----------
casos_m3 = [
    {"patient": "Thomas Nguyen", "caso": "New patient presents a prescription for Oxycodone 10mg (Schedule II).",
     "opciones": ["Dispense immediately since the prescription looks valid.",
                  "Check MassPAT to review usage patterns, other active prescriptions, or red flags.",
                  "Ask for cash payment before reviewing anything."],
     "correcta": 1,
     "explicacion": "MassPAT review is mandatory before dispensing Schedule II-V in Massachusetts."},

    {"patient": "Laura Bennett", "caso": "Patient requests an early refill of Xanax (Schedule IV, benzodiazepine).",
     "opciones": ["Review MassPAT history and consult the pharmacist before deciding.",
                  "Give the refill right away since she's a known patient.",
                  "Refuse without explanation and without checking anything."],
     "correcta": 0,
     "explicacion": "Any early refill of a controlled substance requires history review and pharmacist approval."},

    {"patient": "Mark Sullivan", "caso": "Patient says he lost his Percocet (Schedule II) prescription and asks for a replacement.",
     "opciones": ["Refill the same quantity without issue since he's a regular customer.",
                  "Do not replace without a new prescription from the doctor; a police report may be required per pharmacy policy.",
                  "Give him half the quantity as a compromise."],
     "correcta": 1,
     "explicacion": "Lost Schedule II prescriptions are not automatically replaced; a new prescription from the doctor is required."},

    {"patient": "Patricia Diaz", "caso": "Patient requests to transfer her Oxycodone (Schedule II) prescription to another pharmacy.",
     "opciones": ["It can be transferred without issue, just like any other medication.",
                  "Schedule II prescriptions generally CANNOT be transferred between pharmacies.",
                  "It can only be transferred if the patient pays an extra fee."],
     "correcta": 1,
     "explicacion": "Unlike Schedule III-V, Schedule II prescriptions are not transferable between pharmacies (with very limited exceptions)."},

    {"patient": "George Turner", "caso": "Patient arrives at the counter to pick up a controlled substance.",
     "opciones": ["Verify a government-issued photo ID that matches the name on the prescription.",
                  "No ID is necessary if the patient is already known.",
                  "It's enough to simply ask the patient to state their name out loud."],
     "correcta": 0,
     "explicacion": "A government-issued photo ID is always verified when handing over a controlled substance."},

    {"patient": "Susan Perry", "caso": "The prescriber calls in a verbal order for Oxycodone (Schedule II).",
     "opciones": ["It's accepted without issue, just like any verbal prescription.",
                  "Verbal orders for Schedule II are generally NOT permitted, except in very specific emergencies.",
                  "It's accepted only if the doctor confirms it twice by phone."],
     "correcta": 1,
     "explicacion": "Schedule II requires a written or electronic prescription; verbal orders are only allowed in very limited emergency situations."},

    {"patient": "Confidential patient record", "caso": "MassPAT shows the patient has multiple opioid prescriptions from different doctors ('doctor shopping').",
     "opciones": ["Dispense anyway; it's not the technician's job to judge the patient.",
                  "Alert the pharmacist immediately before continuing with dispensing.",
                  "Call all the prescribers directly without notifying the pharmacist."],
     "correcta": 1,
     "explicacion": "Any red flag in MassPAT is reported to the pharmacist first, who decides the next step."},

    {"patient": "Jason Ramirez", "caso": "Patient in Suboxone (Schedule III, buprenorphine) treatment requests his monthly refill.",
     "opciones": ["Check MassPAT and confirm the refill authorization is active in the system.",
                  "Give the refill without checking anything since it's chronic treatment.",
                  "Automatically deny the refill because it's a controlled substance."],
     "correcta": 0,
     "explicacion": "Even for chronic treatments, MassPAT and refill authorization are verified before dispensing."},

    {"patient": "Chloe Simmons", "caso": "A family member wants to pick up Chloe's Adderall (Schedule II, ADHD medication) on her behalf.",
     "opciones": ["It can be handed to any family member without issue.",
                  "It can only be given to the patient or a documented, authorized agent under state law.",
                  "It can be handed over if the family member pays in cash."],
     "correcta": 1,
     "explicacion": "Schedule II pickup is restricted to the patient or a formally authorized agent."},

    {"patient": "Pharmacy stock case", "caso": "The pharmacy has only partial stock of a Schedule II medication and must do a partial fill.",
     "opciones": ["It's not allowed under any circumstances.",
                  "It's allowed under DEA rules if properly documented, with the remainder filled within 72 hours.",
                  "It can be completed at any time with no time limit."],
     "correcta": 1,
     "explicacion": "The DEA allows documented partial fills of Schedule II, with the remaining quantity provided within 72 hours."},
]

# ---------- MODULE 4: PATIENT POS & COPAY ----------
casos_m4 = [
    {"patient": "Henry Wilson", "costo": 120.00, "tipo": "percent", "cobertura": 0.80, "descripcion": "Insurance covers 80% of the cost."},
    {"patient": "Grace Lee", "costo": 200.00, "tipo": "percent", "cobertura": 0.90, "descripcion": "Insurance covers 90% of the cost."},
    {"patient": "Oscar Martinez", "costo": 75.00, "tipo": "flat", "copago_fijo": 10.00, "descripcion": "The plan has a flat $10 copay for this medication."},
    {"patient": "Ava Thompson", "costo": 150.00, "tipo": "percent", "cobertura": 0.70, "descripcion": "Insurance covers 70% of the cost."},
    {"patient": "Lucas Garcia", "costo": 50.00, "tipo": "percent", "cobertura": 1.00, "descripcion": "MassHealth covers 100% of the cost for this medication."},
    {"patient": "Sophia Robinson", "costo": 300.00, "tipo": "percent", "cobertura": 0.60, "descripcion": "Insurance covers 60% of the cost."},
    {"patient": "Ethan Walker", "costo": 40.00, "tipo": "flat", "copago_fijo": 5.00, "descripcion": "The plan has a flat $5 copay (Tier 1 generic)."},
    {"patient": "Mia Hall", "costo": 500.00, "tipo": "percent", "cobertura": 0.85, "descripcion": "Insurance covers 85% of the cost."},
    {"patient": "Noah Allen", "costo": 90.00, "tipo": "percent", "cobertura": 0.75, "descripcion": "Insurance covers 75% of the cost."},
    {"patient": "Isabella Young", "costo": 25.00, "tipo": "flat", "copago_fijo": 3.00, "descripcion": "The plan has a flat $3 copay (preferred generic)."},
]

# ============================================================
# SIDEBAR MENU
# ============================================================
opcion = st.sidebar.selectbox(
    "Select a system function:",
    [
        "1. Data Entry & E-Prescribing",
        "2. Insurance Billing (MassHealth)",
        "3. Controlled Substances (MassPAT)",
        "4. Patient POS & Copay",
        "5. Medication Knowledge"
    ]
)

# ============================================================
# MODULE 1
# ============================================================
if opcion == "1. Data Entry & E-Prescribing":
    st.header("📝 Prescription Data Entry Module")

    num_caso = st.sidebar.selectbox("Practice case:", list(range(1, 11)), key="caso_m1")
    caso = casos_m1[num_caso - 1]

    st.info(f"Case {num_caso} of 10: Electronic prescription received from Massachusetts General Hospital.")

    receta_texto = (
        f"PATIENT: {caso['patient']}\nDOB: {caso['dob']}\nDR: {caso['doctor']} (NPI: {caso['npi']})\n"
        f"MED: {caso['med']}\nSIG: {caso['sig']}\nQTY: {caso['qty']}"
    )
    st.text_area("Digital Prescription Received:", value=receta_texto, height=120, key=f"ta_{num_caso}")

    sig_input = st.text_input("Translate the SIG code into patient instructions (in English or Spanish):", key=f"sig_{num_caso}")
    days_supply = st.number_input("How many days supply is this prescription for?", min_value=0, value=0, key=f"days_{num_caso}")

    if st.button("Verify Prescription", key=f"btn_{num_caso}"):
        sig_ok = any(k in sig_input.lower() for k in caso["keywords"])
        dias_ok = days_supply == caso["dias"]
        if sig_ok and dias_ok:
            progreso.get("xp", 0)
            progreso["correctas"] += 1

            with open("progress.json", "w") as file:
                json.dump(progreso, file, indent=4)

            st.success("✅ Correcto")
            st.info("🏆 +10 XP")
        elif not sig_ok and not dias_ok:
            st.session_state.incorrectas += 1
            st.error(f"❌ Review both the SIG translation and the days supply calculation. Correct days supply: {caso['dias']}.")
        elif not sig_ok:
            st.session_state.incorrectas += 1
            st.warning(f"⚠️ Review the translation of the SIG code: '{caso['sig']}'.")
        else:
            st.session_state.incorrectas += 1
            st.error(f"❌ Days supply error. The correct calculation for this prescription is {caso['dias']} days.")

# ============================================================
# MODULE 2
# ============================================================
elif opcion == "2. Insurance Billing (MassHealth)":
    st.header("💳 Insurance Claim Adjudication")

    num_caso = st.sidebar.selectbox("Practice case:", list(range(1, 11)), key="caso_m2")
    caso = casos_m2[num_caso - 1]

    st.warning(f"SYSTEM ALERT — Case {num_caso} of 10: Claim Rejected by MassHealth. Patient: {caso['patient']}.")
    st.error(f"REJECTION: {caso['rechazo']}")

    st.write("As the Pharmacy Technician, what is your correct next step?")
    accion = st.radio("Select the correct action:", caso["opciones"], key=f"radio_m2_{num_caso}")

    if st.button("Process Action", key=f"btn_m2_{num_caso}"):
        if caso["opciones"].index(accion) == caso["correcta"]:
            st.success(f"✅ Correct! {caso['explicacion']}")
        else:
            st.error(f"❌ Incorrect. {caso['explicacion']}")

# ============================================================
# MODULE 3
# ============================================================
elif opcion == "3. Controlled Substances (MassPAT)":
    st.header("🔒 Controlled Substance Verification")

    num_caso = st.sidebar.selectbox("Practice case:", list(range(1, 11)), key="caso_m3")
    caso = casos_m3[num_caso - 1]

    st.info(f"Case {num_caso} of 10 — Patient: {caso['patient']}. {caso['caso']}")
    st.write("What is the correct action according to Massachusetts regulations (MassPAT / DEA)?")

    accion = st.radio("Select the correct action:", caso["opciones"], key=f"radio_m3_{num_caso}")

    if st.button("Process Verification", key=f"btn_m3_{num_caso}"):
        if caso["opciones"].index(accion) == caso["correcta"]:
            st.success(f"✅ Correct! {caso['explicacion']}")
        else:
            st.error(f"❌ Incorrect. {caso['explicacion']}")

# ============================================================
# MODULE 4
# ============================================================
elif opcion == "4. Patient POS & Copay":
    st.header("💵 Point of Sale & Copay Calculation")

    num_caso = st.sidebar.selectbox("Practice case:", list(range(1, 11)), key="caso_m4")
    caso = casos_m4[num_caso - 1]

    st.info(f"Case {num_caso} of 10 — Patient {caso['patient']} at the pickup counter.")
    st.write("**Insurance information:**")
    st.write(f"- Total cost of medication: **${caso['costo']:.2f}**")
    st.write(f"- {caso['descripcion']}")

    copay_input = st.number_input(
        "Calculate the copay the patient must pay ($):",
        min_value=0.0, value=0.0, step=0.01, format="%.2f", key=f"copay_{num_caso}"
    )

    if st.button("Verify Copay", key=f"btn_m4_{num_caso}"):
        if caso["tipo"] == "percent":
            copago_correcto = round(caso["costo"] * (1 - caso["cobertura"]), 2)
        else:
            copago_correcto = caso["copago_fijo"]

        if abs(copay_input - copago_correcto) < 0.01:
            st.success(f"✅ Correct! The copay is ${copago_correcto:.2f}.")
        else:
            st.error(f"❌ Incorrect. The correct copay is ${copago_correcto:.2f}.")
            
# ============================================================
# MODULE 5: MEDICATION KNOWLEDGE
# ============================================================
elif opcion == "5. Medication Knowledge":

    modulo_medicamentos(progreso)
   
# ============================================================
# FOOTER
# ============================================================

# ============================================================
# FOOTER
# ============================================================
st.write("---")
st.caption("Compliant with HIPAA regulations and the Massachusetts Board of Registration in Pharmacy.")