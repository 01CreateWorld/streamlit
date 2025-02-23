import streamlit as st
import time  # 新增时间模块

# 初始化session状态
if 'history' not in st.session_state:
    st.session_state.history = []
if 'followups' not in st.session_state:
    st.session_state.followups = [
        "什么是美拉德反应？",
        "煎虾时应该先给锅放油还是先放虾？",
        "煎牛排推荐用什么锅具？"
    ]

# 设置页面配置
st.set_page_config(
    page_title="Selina的智能助手",
    page_icon="🤖",
    layout="centered"
)

def handle_query(query):
    """处理查询并获取Coze回答"""
    import coze_agent  # 导入coze_agent模块
    
    # 调用coze接口获取答案和后续问题
    with st.spinner("正在查询中..."):  # 添加加载提示
        time.sleep(0.5)  # 保持临时回答可见时间
        answer, follow_ups = coze_agent.ask_coze(query)
    
    # 更新后续问题列表（如果返回的列表不为空）
    if follow_ups:
        st.session_state.followups = follow_ups
    
    # 返回答案或默认提示
    return answer if answer else "未获取到答复"

def main():
    st.title("Selina的智能助手")
    
    # 问题输入表单
    with st.form("question_form"):
        question = st.text_input("请输入您的问题", key="input_question")
        submitted = st.form_submit_button("提交")
    
    # 处理问题提交
    if submitted and st.session_state.get("input_question", "").strip():
        current_question = st.session_state.input_question.strip()
        
        # 添加问题到历史
        st.session_state.history.append(("问题", current_question))
        
        # 立即显示临时回答
        with st.empty():  # 创建临时容器
            st.session_state.history.append(("回答", f"正在查询：{current_question}..."))
            # 渲染当前状态
            display_history()
        
        # 获取真实回答
        real_answer = handle_query(current_question)
        
        # 替换临时回答
        st.session_state.history[-1] = ("回答", real_answer)
        # 清除临时容器
        st.rerun()  # 强制刷新界面

    # 显示历史问答
    display_history()
    
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

def display_history():
    """单独封装历史记录显示逻辑"""
    for role, content in st.session_state.history:
        if role == "问题":
            st.markdown(f"**您问**：{content}")
        else:
            st.info(f"**回答**：{content}")

if __name__ == "__main__":
    main()
