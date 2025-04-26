import streamlit as st
import httpx

# 八卦名稱
BAGUA = ["乾", "兌", "離", "震", "巽", "坎", "艮", "坤"]
BAGUA_SYMBOLS = ["☰", "☱", "☲", "☳", "☴", "☵", "☶", "☷"]
YAO = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

GRADES = [
    ["乾為天", "天澤履", "天火同人", "天雷无妄", "天風姤", "天水訟", "天山遯", "天地否"],
    ["澤天夬", "兌為澤", "澤火革", "澤雷隨", "澤風大過", "澤水困", "澤山咸", "澤地萃"],
    ["火天大有", "火澤睽", "離為火", "火雷噬嗑", "火風鼎", "火水未濟", "火山旅", "火地晉"],
    ["雷天大壯", "雷澤歸妹", "雷火豐", "震為雷", "雷風恒", "雷水解", "雷山小過", "雷地豫"],
    ["風天小畜", "風澤中孚", "風火家人", "風雷益", "巽為風", "風水渙", "風山漸", "風地觀"],
    ["水天需", "水澤節", "水火既濟", "水雷屯", "水風井", "坎為水", "水山蹇", "水地比"],
    ["山天大畜", "山澤損", "山火賁", "山雷頤", "山風蠱", "山水蒙", "艮為山", "山地剝"],
    ["地天泰", "地澤臨", "地火明夷", "地雷復", "地風升", "地水師", "地山謙", "坤為地"],
]

# 呼叫 DeepSeek API
def ai_interpret(question: str, gua: str, line_change: int, api_key: str) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = (
        f"你是一位精通《易經》的大師，請從《易經》正典引用卦辭、彖辭與爻辭，"
        f"並對求卦者做詳盡分析。\n\n"
        f"求卦者問題：{question}\n"
        f"卦名：{gua}\n"
        f"變爻：第 {line_change + 1} 爻（{YAO[line_change]}\n\n"
        "請先引用該卦的【卦辭】、【彖辭】和該爻的【爻辭】，"
        "然後進行詳細解讀，最後給出具體建議與吉凶判斷。"
    )
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ 發生錯誤：{e}"

# Web App 介面
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://pic.616pic.com/ys_bnew_img/00/12/36/5zY7oiNMap.jpg");  /* 可換成你自己的背景圖連結 */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.8); /* 白色半透明背景，提高可讀性 */
        border-radius: 15px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp {
        font-family: "DFKai-SB", "標楷體", "serif";
        color: black;
    }

    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import streamlit as st

# 設定按鈕顏色和樣式
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #f4f1ea; /* 背景顏色 */
        color: white;              /* 白色文字 */
        font-size: 16px;           /* 字體大小 */
        border: none;              /* 無邊框 */
        padding: 10px 20px;        /* 增加內邊距 */
        border-radius: 5px;        /* 圓角 */
        cursor: pointer;          /* 游標顯示為指針 */
    }

    .stButton>button:hover {
        background-color: #45a049; /* 滑鼠懸停時的背景顏色 */
    }
    </style>
    """,
    unsafe_allow_html=True
)




st.title("🖥️ AI問卜 🔍")
st.markdown("在下觀大人之相，許是心有鬱結")
st.markdown("不妨讓在下卜上一卦？")

api_key = "sk-7c027158d8374d498346858b27228d64"
name = st.text_input("敢問大人尊姓大名")
question = st.text_input("大人，不知您所卜何事？")

st.markdown("請大人給我三組三位數：")
col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.text_input("第一組三位數", max_chars=3)  # 輸入框限制為三個字符
with col2:
    n2 = st.text_input("第二組三位數", max_chars=3)  # 輸入框限制為三個字符
with col3:
    n3 = st.text_input("第三組三位數", max_chars=3)  # 輸入框限制為三個字符


if st.button("解卦"):
    if not api_key or not name or not question:
        st.warning("請完整輸入所有欄位。")
    else:
        # 檢查是否為三位數字
        if len(n1) != 3 or len(n2) != 3 or len(n3) != 3 or not n1.isdigit() or not n2.isdigit() or not n3.isdigit():
            st.warning("請確保每組數字都是三位數！")
        else:
            n1, n2, n3 = int(n1), int(n2), int(n3)
            re1, re2, re3 = n1 % 8, n2 % 8, n3 % 6
            upper = BAGUA[re2]
            lower = BAGUA[re1]
            gua = GRADES[re2][re1]
        
            st.markdown(f"### {name} 大人的卦象：")
            st.markdown(f"**上卦：** {upper} {BAGUA_SYMBOLS[re2]}  +  **下卦：** {lower} {BAGUA_SYMBOLS[re1]}")
            st.markdown(f"**卦名：** `{gua}`")
            st.markdown(f"**變爻：** {YAO[re3]}")

            with st.spinner("AI 正在解卦中..."):
                result = ai_interpret(question, gua, re3, api_key)
                st.markdown("## 🧾 解卦結果")
                st.write(result)
