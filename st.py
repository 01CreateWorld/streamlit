import streamlit as st
import time  # 新增时间模块

# 初始化session状态
if 'history' not in st.session_state:
    st.session_state.history = []
if 'followups' not in st.session_state:
    st.session_state.followups = [
        "你好！",
        "你是谁？",
        "我如何使用？"
    ]

# 设置页面配置
st.set_page_config(
    page_title="Selina的智能助手",
    page_icon="🤖",
    layout="centered"
)

def handle_query(query):
    """模拟处理查询（修改后）"""
    time.sleep(2)  # 添加2秒延迟
    return f"模拟回答：{query}"  # 直接返回问题作为答案

def main():
    st.title("Selina的智能助手")
    
    # 问题输入表单
    with st.form("question_form"):
        question = st.text_input("请输入您的问题", key="input_question")
        submitted = st.form_submit_button("提交")
    
    # 处理问题提交
    if submitted and question.strip():
        # 先显示临时回答
        st.session_state.history.append(("问题", question))
        temp_answer = f"正在查询：{question}..."
        st.session_state.history.append(("回答", temp_answer))
        
        # 获取真实回答
        real_answer = handle_query(question)
        st.session_state.history[-1] = ("回答", real_answer)
    
    # 显示历史问答
    for role, content in st.session_state.history:
        if role == "问题":
            st.markdown(f"**您问**：{content}")
        else:
            st.info(f"**回答**：{content}")
    
    # 显示后续问题
    st.subheader("您可能还想问：")
    for followup in st.session_state.followups:
        st.button(
            followup,
            key=f"followup_{followup}",
            on_click=lambda q=followup: (
                st.session_state.update({
                    "input_question": q,
                    "submitted": True  # 自动触发提交
                })
            )
        )

if __name__ == "__main__":
    main()
