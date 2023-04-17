import os
import openai
import streamlit

def execute_gpt_command(openai):
    # create a completion
    completion = openai.Completion.create(model="text-davinci-003",prompt="Write Medical Necessity letter to insurance company named AHI for patient named $$patient_name$$ , needs catherization treatment for myocardial infraction. Include scientific references from book, include trial data supporting FDA approval, include clinical rationale behind the treatment  and write letter in assertive tone", max_tokens=4000, temperature=0 )
    return completion


if __name__ == '__main__':
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion= execute_gpt_command(openai)
    print(completion.choices[0].text)
