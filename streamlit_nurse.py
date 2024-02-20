#  streamlit run streamlit_nurse.py : streamlit 실행 명령 streamlit run "실행파일명"
from openai import OpenAI
import streamlit as st
import time

assistant_id = "asst_lgZaU0e2nlpW8GJxMK4nGb13"

# thread_id = "thread_dXZl6AiXu7WPNY7Meiog1cUt" : 고정된 thread_id 사용시 적용, 지금은 변수로 정의하여 생성

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", value="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")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# 위에 내용은 사이드바에 표출되는 사항으로 편집하여 사용 가능함.

    client = OpenAI(api_key=openai_api_key)
   
    thread_id = st.text_input("thread ID")

    thread_btn = st.button("Create a new thread")
    
    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id
        
        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("Thread가 생성되었습니다.")
    
st.title("💬 면접도우미 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "상황별 또는 직무별 면접 시 적절한 대응을 위해 궁금한 내용이 있으면 편하게 질문하세요."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not thread_id:
        st.info("Please add your thread ID to continue.")
        st.stop()
 
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.beta.threads.messages.create(
        thread_id,
        role = "user",
        content = prompt,
    )
    # print(response)
    
    run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id
    )
    # print(run)
    
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id = thread_id, 
            run_id = run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)        
#        print(run)
        
    thread_messages = client.beta.threads.messages.list(thread_id)
#    print(thread_messages.data)
    
    msg = thread_messages.data[0].content[0].text.value
#    print(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg) 
   
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg) 