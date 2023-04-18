import streamlit as st

st.title('Patient Details')
patName = st.text_input("Patient Name")
patDOB = st.date_input("Date of Birth")

insuranceId = st.text_input("Insurance ID")
insuranceCompany = st.selectbox('Insurance Company', ('Fortis', 'Cigna', 'Humana', 'Oscar Health', 'Unitrin'))
mrn = st.text_input("Case ID Number")
diagnosis = st.selectbox('Diagnosis', (
'Cholera(A00)', 'Typhoid and paratyphoid fevers(A01)', 'Pulmonary embolism(I26)', 'Disorders of lacrimal system(H04)',
'Erythema multiforme(L51)'))
diagnosticDetails = st.text_area('Diagnositic Details')
treatmentDetails = st.selectbox('Treatment', ('Cancer', 'Heart attack', 'Eye Cataract'))
includeTrialData = st.checkbox('Including trial data supporting FDA approval')
includeReferences = st.checkbox('Include scientific references from book')
clinicalRationale = st.checkbox('Clinical rationale behind the treatment')

patInfo = {
    "patientName": patName,
    "dateOfBirth": patDOB,
    "insuranceId": insuranceId,
    "insuranceCompany": insuranceCompany,
    "mrn": mrn,
    "diagnosis": diagnosis,
    "diagnosticDetails": diagnosticDetails,
    "treatment": treatmentDetails,
    "includeReferences": includeReferences,
    "includeTrialData": includeTrialData,
    "clinicalRationale": clinicalRationale
}


def framePromtCommand():
    st.write(patInfo)


if st.button("Submit", key="my_button"):
    framePromtCommand()