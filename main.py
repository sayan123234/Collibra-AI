from pandasai.llm import GoogleGemini
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.responses.response_parser import  ResponseParser
from configparser import ConfigParser
from Scan_Glossary import fetch_data

class StreamLitResponse(ResponseParser):
        def __init__(self,context) -> None:
              super().__init__(context)
        def format_dataframe(self,result):
               st.dataframe(result['value'])
               return
        def format_plot(self,result):
               st.image(result['value'])
               return
        def format_other(self, result):
               st.write(result['value'])
               return

config = ConfigParser()
config.read('APIKey.ini')
gemini_api_key = config['API_KEY']['google_api_key']

def generateResponse(dataFrame,prompt):
        llm = GoogleGemini(api_key=gemini_api_key)
        pandas_agent = SmartDataframe(dataFrame,config={"llm":llm, "response_parser":StreamLitResponse})
        answer = pandas_agent.chat(prompt)
        return answer

st.write("# Talk with Novelis's Business Glossary")
st.write("##### Engage in insightful conversations with your Glossary, empowering you to uncover valuable insights and make informed decisions effortlessly!")
with st.sidebar:
        st.write("Made with Gemini pro and pandas ai.")
        st.write("<div>Developed by - <span style=\"color: cyan; font-size: 24px; font-weight: 600;\">Sayan Sutradhar</span></div>",unsafe_allow_html=True)

df = fetch_data()
if df is not None:
        with st.expander("Preview of the Glossary"):
                st.write(df.head())
                        
        user_input = st.text_area("Type your message here",placeholder="Ask me about your data")
        if st.button("Generate"):
                with st.spinner("Generating response..."):
                        answer = generateResponse(dataFrame=df,prompt=user_input)
                        st.write(answer) 
