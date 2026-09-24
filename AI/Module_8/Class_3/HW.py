# main.py (Streamlit) — shorter version
# Switch provider by changing the import line:
from groq import generate_response
# from groq import generate_response

import io, streamlit as st

SYSTEM_PROMPT = """You are a Math Mastermind. For every math problem:
1) Show step-by-step solution  2) Explain reasoning  3) Give alternate method if possible
4) Verify answer if possible  5) Use proper notation  6) Break complex problems into parts
Format: Problem → Steps → **Final Answer** → Concepts used. Be precise and educational.
If the problem is simple like 2+2, just give the answer. If the problem is unsolvable, explain why.
Use LaTeX with $...$ for inline math and $$...$$ for display math only."""   ## FIX: LaTeX delimiter changed to $...$ / $$...$$ since Streamlit doesn't render \[ \] or \( \)

def math_generate(problem: str, level: str, temperature=0.1, max_tokens=1024) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nMath Problem ({level}): {problem}"
    return generate_response(prompt, temperature=temperature, max_tokens=max_tokens)

def export_txt(history):
    txt = "\n\n".join([f"Q{i}: {h['q']}\nA{i}: {h['a']}" for i, h in enumerate(history, 1)])
    return io.BytesIO(txt.encode("utf-8"))


def setup_ui():
    st.set_page_config(page_title="🧮 Math Mastermind", layout="centered")
    st.title("🧮 Math Mastermind")
    st.write("Solve any math problem with detailed step-by-step explanations.")

    with st.expander("📌 Examples"):
        st.markdown(
            '- Algebra: "Solve 2x² + 5x − 3 = 0"\n'
            '- Calculus: "Derivative of sin(x²) + ln(x)"\n'
            '- Geometry: "Area of triangle (0,0),(3,4),(6,0)"\n'
            '- Probability: "P(sum=7 with two dice)"'
        )

    st.session_state.setdefault("history", [])
    st.session_state.setdefault("k", 0)

    c1, c2 = st.columns([1, 2])
    if c1.button("🗑️ Clear"):
        st.session_state.history = []; st.rerun()

    if st.session_state.history:
        c2.download_button("📄 Export", export_txt(st.session_state.history),
                           "Math_Mastermind_Solutions.txt", "text/plain")

    with st.form("math_form", clear_on_submit=True):
        q = st.text_area("📝 Enter your math problem:", height=100,
                         placeholder="Example: Solve x² + 5x + 6 = 0",
                         key=f"q_{st.session_state.k}")
        a, b = st.columns([3, 1])
        solve = a.form_submit_button("🧠 Solve", use_container_width=True)
        level = b.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)

        if solve:
            if not q.strip(): st.warning("⚠️ Enter a problem first.")
            else:
                with st.spinner("Solving..."):
                    ans = math_generate(q.strip(), level)
                st.session_state.history.insert(0, {"q": q.strip(), "a": ans, "lvl": level})
                st.session_state.k += 1; st.rerun()

    if not st.session_state.history: return
    st.markdown("### 🧾 Solution History (Latest First)")

    ## Below: removed the old CSS block (.box, .q, .lvl, .a) entirely — replaced with native Streamlit widgets, no custom HTML/CSS
    with st.container(height=500, border=True):              ## Native scrollable box (previously done via .box CSS with max-height + overflow-y:auto)
        for i, h in enumerate(st.session_state.history, 1):
            col_q, col_lvl = st.columns([4, 1])               ## Side-by-side layout for question and level
            col_q.markdown(f"**Q{i}: {h['q']}**")              ## Previously bold+green via .q CSS class, now plain **bold** markdown syntax
            col_lvl.badge(h["lvl"])                            ## Previously an orange pill via .lvl CSS class, now Streamlit's native st.badge() (requires Streamlit >=1.37)
            st.markdown(h["a"])                                ## MAIN FIX: answer used to be inside a .a div (broke LaTeX rendering), now goes directly into st.markdown() so $...$ renders correctly
            st.divider()                                       ## Separator line between each Q&A (previously done via margin CSS)

if __name__ == "__main__":
    setup_ui()