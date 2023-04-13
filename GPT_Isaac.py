import openai
import streamlit as st

openai.api_key = "xxx"


st.title("Isaac the GPT Structural Engineer guide")

messages = []
# say that GPT is a structural engineer
tutor = "From now on, you are a structural engineer with 30 years of experience. Answer all questions like you are, and you want to help students. Moreover, only answer according to Eurocode rules, which are used in europe"
messages.append({"role": "system", "content": tutor})

question = st.text_input('Ask me a question about structural engineering: ')
if st.button("submit"):
    messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",  messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    st.write("\n" + reply + "\n")

    summary = openai.ChatCompletion.create(model="gpt-3.5-turbo",  messages=[{"role": "user", "content": "Summarize in 15 words: "+ reply}])
    replysum = summary["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": replysum})
    st.header("Summary")
    st.write("\n" + replysum + "\n")

    threetips = openai.ChatCompletion.create(model="gpt-3.5-turbo",  messages=[{"role": "user", "content": "Give three tips (sentence of max 10 words) based on: "+ reply}])
    reply3 = threetips["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply3})
    st.header("Three tips")
    st.write("\n" + reply3 + "\n")

    equations = openai.ChatCompletion.create(model="gpt-3.5-turbo",  messages=[{"role": "user", "content": "Give a list of the equations used in: "+ reply}])
    replyeq = equations["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": replyeq})
    st.header("Formulas")
    st.write("\n" + replyeq + "\n")




