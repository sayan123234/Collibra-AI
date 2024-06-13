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

st.write("# Collibra AI Meta-data Analyst")
st.write("##### Engage in insightful conversations with your meta-data in Collibra (Business Glossary for Now) empowering you to uncover valuable insights and make informed decisions effortlessly!")
with st.sidebar:
        #st.title("Collibra AI Meta-data Analyst")
        #st.write("Engage in insightful conversations with your meta-data in Collibra (Business Glossary for Now) empowering you to uncover valuable insights and make informed decisions effortlessly!")
        # Added a divider
        st.divider()
        # Add content to the sidebar/drawer
        #with st.expander("Data Visualization"):
        st.write("Made with Gemini pro and pandas ai.")
        st.write("<div>Developed by - <span style=\"color: cyan; font-size: 24px; font-weight: 600;\">Sayan Sutradhar</span></div>",unsafe_allow_html=True)


# uploaded_file = st.file_uploader("Upload your dataset here (excel)",type="xlsx")
# if uploaded_file is not None:
#         # Read the CSV file
#         df = pd.read_excel(uploaded_file)

#         # Display the data
#         with st.expander("Preview"):
#             st.write(df.tail())

#         # Plot the data
#         user_input = st.text_input("Type your message here",placeholder="Ask me about your data")
#         if st.button("Generate"):
#                 with st.spinner("Generating response..."):
#                         answer = generateResponse(dataFrame=df,prompt=user_input)
#                         st.write(answer)

df = fetch_data()
if df is not None:
        with st.expander("Preview of the Glossary"):
                st.write(df.head())
                        
        user_input = st.text_area("Type your message here",placeholder="Ask me about your data")
        if st.button("Generate"):
                with st.spinner("Generating response..."):
                        answer = generateResponse(dataFrame=df,prompt=user_input)
                        st.write(answer) 