import streamlit as st
import app
import datetime

min_date = datetime.date.today() - datetime.timedelta(days=365*200)
max_date = datetime.date.today()
st.title('Patient Details')
docName = st.text_input("Requesting Doctor")
patName = st.text_input("Patient Name")
patDOB = st.date_input("Date of Birth", min_value=min_date, max_value=max_date)

insuranceId = st.text_input("Insurance ID")
insuranceCompany = st.selectbox('Insurance Company', ('Fortis', 'Cigna', 'Humana', 'Oscar Health', 'Unitrin'))
mrn = st.text_input("Case ID Number")
diagnosis = st.selectbox('Diagnosis', ('Acute myocardial infarction(I21. 9)', 'Cataract(H26. 9)',
'Cholera(A00)', 'Typhoid and paratyphoid fevers(A01)', 'Pulmonary embolism(I26)', 'Disorders of lacrimal system(H04)',
'Erythema multiforme(L51)'))
diagnosticDetails = st.text_area('Diagnositic Details')
treatmentDetails = st.selectbox('Treatment', ('Catheterization','Phacoemulsification','Cancer', 'Heart attack'))
includeTrialData = st.checkbox('Including trial data supporting FDA approval')
includeReferences = st.checkbox('Include scientific references from book')
clinicalRationale = st.checkbox('Clinical rationale behind the treatment')
tone = st.selectbox("Document Tone", [
    "Formal",
    "Informal",
    "Optimistic",
    "Worried",
    "Friendly",
    "Curious",
    "Assertive",
    "Encouraging",
    "Romantic",
    "Harsh",
    "Abusive",
])


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
    "clinicalRationale": clinicalRationale,
    "tone":tone,
    "doctor_name":docName
}


def framePromtCommand():
    st.write(patInfo)


if st.button("Submit", key="my_button"):
    response= app.execute_gpt_command(patInfo)
    unMaskTemplateResponse = app.unMaskTemplate(response, patInfo)
    print(f'unMaskedTemplate response from gpt :{unMaskTemplateResponse}')
    app.create_document_and_insert(unMaskTemplateResponse)
    st.write('document created successfully')
