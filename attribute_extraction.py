from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import openai
from openai import OpenAI

max_tokens=512

load_dotenv()
def gen_response(input):

  client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
  )

  chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": input,
        }
    ],
    model="gpt-3.5-turbo",
  )

  response = chat_completion.choices[0].message.content
  #print(chat_completion)
  #response_dict = json.loads(json_content)

  return response

def read_sql_query(sql,db):
    connection=sqlite3.connect(db)
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

prompt = """
Extract the following attributes from the given
e-commerce product complaint email thread:
    1. Product name or description
    2. Issue description (e.g., damaged, missing, etc.)
    3. Order number (if available)
    4. Resolution steps or actions (if mentioned)
    5. Issue raised Date and Time
    6.Complainant Email ID
    7.Complainant Name
    8.Number of emails in the thread

    Provide the output in text
    """

st.set_page_config(page_title="ATTribute Extraction")
st.header("Email Attribute Extraction")
uploaded_file=st.file_uploader("Choose a text file",type="txt")
submit=st.button("Submit")

if uploaded_file is not None:
    email_thread=uploaded_file.read().decode("utf-8")


if submit:
    input=prompt+email_thread
    response=gen_response(input)
    print(response)
    st.subheader("The response is")
    st.write(response)