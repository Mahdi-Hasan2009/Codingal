# main.py (Streamlit)
# Switch provider by changing the import line:
from groq import generate_response
# from groq import generate_response

import io
import re
import streamlit as st

def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return True
    t = text.strip()
    # common "cut" signs: ends mid-word, mid-markdown, or no closing punctuation
    if t.endswith(("**", "*", "-", "—", ":", ",", "(", "[", "{")):
        return True
    if re.search(r"\d+\.\s*\*\*$", t):  # like "3. **"
        return True
    if not re.search(r"[.!?]\s*$", t):  # no sentence-ending punctuation
        return True
    return False

def complete_answer(question: str, max_rounds: int = 2) -> str:
    # 1) Ask for a clean structured answer (helps avoid unfinished bullets)
    base_prompt = (
        "Answer clearly in numbered points. "
        "Do not cut sentences. Finish each point fully.\n\n"
        f"Question: {question}"
    )

    ans = generate_response(base_prompt, temperature=0.3, max_tokens=1024)

    # 2) If it looks cut, continue from last line without repeating
    rounds = 0
    while rounds < max_rounds and looks_incomplete(ans):
        cont_prompt = (
            "Continue EXACTLY from where you stopped. "
            "Do NOT repeat earlier text. "
            "Finish the incomplete point and complete the answer.\n\n"
            f"Question: {question}\n\n"
            f"Answer so far:\n{ans}\n\nContinue:"
        )
        more = generate_response(cont_prompt, temperature=0.3, max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans = (ans.rstrip() + "\n" + more.lstrip()).strip()
        rounds += 1

    return ans

def export_bytes(history):
    text = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(history, 1)])
    return io.BytesIO(text.encode("utf-8"))

def setup_ui():
    st.set_page_config(page_title="AI Teaching Assistant", layout="centered")
    st.title("🤖 AI Teaching Assistant")
    st.write("Ask me anything about various subjects, and I'll provide an insightful answer.")
    st.session_state.setdefault("history", [])

    col_clear, col_export = st.columns([1, 2])
    with col_clear:
        if st.button("🧹 Clear Conversation"):
            st.session_state.history = []
            st.rerun()
    with col_export:
        if st.session_state.history:
            st.download_button(
                label="📤 Export Chat History",
                data=export_bytes(st.session_state.history),
                file_name="AI_Teaching_Assistant_Conversation.txt",
                mime="text/plain",
            )

    user_input = st.text_input("Enter your question here:")
    if st.button("Ask"):
        q = user_input.strip()
        if q:
            with st.spinner("Generating AI response..."):
                a = complete_answer(q)
            st.session_state.history.insert(0, {"question": q, "answer": a})
            st.rerun()
        else:
            st.warning("⚠️ Please enter a question before clicking Ask.")

    st.markdown("### Conversation History")

    history_container = st.container(height=420)
    with history_container:
        for i, h in enumerate(st.session_state.history, 1):
            with st.container(border=True):
                st.markdown(f"**Q{i}: {h['question']}**")
                st.write(h["answer"])

def main():
    setup_ui()

if __name__ == "__main__":
    main()
