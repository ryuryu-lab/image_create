import requests
import io
import base64
from PIL import Image, PngImagePlugin
import streamlit as st

url = "http://127.0.0.1:7860"

st.set_page_config(
    page_title="Nobel Image Creator", 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items={
         'About': """
         # 画像生成アプリ
         このアプリはstable diffusionを利用した画像生成アプリです
         """
     })

flag = 0

st.title('画像生成')

with st.form("form"):

    #画像生成する際に必要な設定
    text1 = st.text_area("プロンプト(ここに文章を入力し、「生成」ボタンを押すと入力された文章を元に画像生成します。言語は英語です。)",key=2)
    text2 = st.text_area("ネガティブプロンプト(生成した画像に含みたくない要素を入力します。言語は英語です。)",key=3)
    step = st.slider("サンプリングステップ数(画像生成のフィードバックを行う回数です。大きい数を設定すると高画質になりますが、その分時間もかかります。)",1,100,5)
    width = st.slider("幅(生成する画像の幅をピクセル単位で設定します。)",1,2048,512,32)
    height = st.slider("高さ(生成する画像の鷹さをピクセル単位で設定します。)",1,2048,512,32)
    cfgscale = st.slider("CFGスケール(CFGスケールが大きいほどプロンプトに沿ったイラストを生成できます。ただし、大きすぎるとイラストが崩れるリスクが高まります。)",1,30,7)
    submitted = st.form_submit_button("画像を生成")
    
    if submitted:
                
        #画像設定反映
        payload = {
        "prompt": text1,
        "steps": step,
        "cfg_scale" : 7,
        "width" : width,
        "height" : height,
        "negative_prompt" : text2
        }

        #webuiのapiを利用して画像生成、保存
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

        r = response.json()

        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    
            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save('data\output_t2i.png', pnginfo=pnginfo)
            flag=1

with st.container():
    st.title('生成された画像')

    #画像の表示
    if flag:
        img = Image.open('data\output_t2i.png')
        st.image(img)

        #画像をダウンロードするボタン配置
        with open('data\output_t2i.png', 'rb') as file:
            st.download_button(label="生成した画像のダウンロード", data=file, file_name="image.png", mime="image/png")
