import streamlit as st
import re
from typing import Dict, List, Tuple, Optional

st.set_page_config(page_title="Route Formatter", page_icon="🧭", layout="wide")
st.title("🧭 Route Formatter - ORF")

with st.expander("Features", expanded=False):
    st.markdown("""
- Automatically recognizes multiple title formats (supports both Chinese and English)
- Automatically recognizes two interval formats: `a-b v` and `v (a-b)` 
- By default, only outputs **Lines 20–31**
- Two sorting modes:  
  - **numeric**: Fixed 20→31 sequence  
  - **encounter**: By order of appearance in input text
""")

# --- Step 1 · 载入函数 ---
HDR_EN = re.compile(r'(?P<num>\d+)\s*route\s*\d+\s*date', re.IGNORECASE)
HDR_CN = re.compile(r'(?P<num>\d+)\s*\u53F7(?:\u7EBF)?')
SEG_A = re.compile(r'(?P<start>\d+)\s*-\s*(?P<end>\d+)\s+(?P<val>\d+)')
SEG_B = re.compile(r'(?P<val>\d+)\s*[\uFF08(]\s*(?P<start>\d+)\s*-\s*(?P<end>\d+)\s*[\uFF09)]')

def build_sections(raw_text: str):
    sections: Dict[int, List[Tuple[int,int,int]]] = {}
    order: List[int] = []
    current_num: Optional[int] = None
    i = 0
    n = len(raw_text)
    while i < n:
        m_hdr_en = HDR_EN.search(raw_text, i)
        m_hdr_cn = HDR_CN.search(raw_text, i)
        m_seg_a = SEG_A.search(raw_text, i)
        m_seg_b = SEG_B.search(raw_text, i)
        candidates = []
        for tag, m in (('hdr_en', m_hdr_en), ('hdr_cn', m_hdr_cn), ('seg_a', m_seg_a), ('seg_b', m_seg_b)):
            if m:
                candidates.append((m.start(), tag, m))
        if not candidates:
            break
        _, tag, m = min(candidates, key=lambda x: x[0])
        if tag in ('hdr_en', 'hdr_cn'):
            try:
                num = int(m.group('num'))
            except Exception:
                num = None
            current_num = num
            if current_num is not None and current_num not in sections:
                sections[current_num] = []
                order.append(current_num)
            i = m.end()
            continue
        if current_num is None:
            i = m.end()
            continue
        start = int(m.group('start')); end = int(m.group('end')); val = int(m.group('val'))
        sections.setdefault(current_num, []).append((start, end, val))
        i = m.end()
    return sections, order

def render_sections(sections, order, only_range=(20,31), order_mode="numeric"):
    lo, hi = only_range
    outputs: List[str] = []
    if order_mode == "encounter":
        for num in order:
            if num is None or num < lo or num > hi: continue
            segs = sections.get(num, [])
            if not segs: continue
            body = ",".join(f"{s}-{e}({v})" for s,e,v in segs)
            outputs.append(f"\n{body}")
    else:
        for num in range(lo, hi+1):
            segs = sections.get(num, [])
            if not segs: continue
            body = ",".join(f"{s}-{e}({v})" for s,e,v in segs)
            outputs.append(f"\n{body}")
    return "".join(outputs)

def format_lines(raw_text: str, order_mode="numeric", only_range=(20,31)):
    sections, order = build_sections(raw_text)
    return render_sections(sections, order, only_range, order_mode)

# --- Step 2 · Paste Original Data ---
st.header("Paste Original Text")
raw_text = st.text_area("Original", value="", height=220, placeholder="Paste Original Text below...")

# Controls: Sorting and Line Range
col1, col2, col3 = st.columns(3)
order_mode = col1.selectbox("Sorting Mode", ["numeric", "encounter"], index=0)
lo = col2.number_input("Start Line Number", min_value=1, max_value=1000, value=20, step=1)
hi = col3.number_input("End Line Number", min_value=1, max_value=1000, value=31, step=1)

# --- Step 3 · Formatted Result Output ---
st.header("Result Output")
run = st.button("🚀 Formatting")
if run:
    if not raw_text.strip():
        st.warning("Please enter the original text")
    else:
        out = format_lines(raw_text, order_mode=order_mode, only_range=(int(lo), int(hi)))
        if not out.strip():
            st.info("No matching data found.")
        else:
            st.text(out)
