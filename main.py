# Contents of ~/my_app/streamlit_app.py
import streamlit as st

st.title("推しのすぅ式化システム")
st.write('')
st.write('')
st.write('')
st.write('')
st.write('推しの画像からエッジを抽出し，線分の近似式を求めるアプリです．')
st.write('')
st.write('')
st.write('＜使用方法＞')
st.write('')
st.write('１）アプリなどで背景を削除した推しの画像を用意して下さい．')
st.write('２）Systemのタブに移動し，画像を投稿します．')
st.write('３）エッジの閾値を設定します．')
st.write('エッジの閾値を上げると描画する線が減ります．')
st.write('いい感じに調整してください')
st.write('４）「近似式を算出する」ボタンを押して下さい．')
st.write('')
st.write('数式が長すぎると感じた場合は，Liteのタブに移動して下さい')
st.write('Liteでは画像の外側のエッジのみを取得します．')
st.write('Liteには閾値設定がありません')
def main():
    st.markdown("# Main page")
    st.sidebar.markdown("# Main page")

def page2():
    st.markdown("# Page 2")
    st.sidebar.markdown("# Page 2")
    
def page3():
    st.markdown("# Page 3")
    st.sidebar.markdown("# Page 3")

page_names_to_funcs = {
    "Main Page": main,
    "Page 21": page2,
    "Page 31": page3,
}

