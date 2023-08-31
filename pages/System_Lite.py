import streamlit as st
import cv2
import numpy as np

def main():
    st.title("推しのすぅ式化システム[Lite]")
     #閾値を設定して直線の近似式を算出
    upload_image = st.file_uploader("画像をアップロードしてください", type=["png"])
    
    if upload_image is not None:
        image = read_image(upload_image)
        st.image(image, caption="アップロードされた画像", use_column_width=True)
        #輪郭出力
        contours_image = detect_outer_contours(image)
        st.image(contours_image, caption="外側の輪郭検出結果", use_column_width=True)
        
        # 数式の表示
        lines = extract_lines(contours_image)
        
        if st.button("近似式を算出する"):
            equation = generate_equation_from_lines(lines)
            st.write("数式近似:", equation)
        
#画像のnumpy配列への変換処理
def read_image(upload_image):
    image = np.asarray(bytearray(upload_image.read()), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    return image
#数式の簡略化のために画像の輪郭線のみを算出
def detect_outer_contours(image):
    alpha_channel = image[:, :, 3]
    _, thresh = cv2.threshold(alpha_channel, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contour_image = np.zeros_like(image)
    for contour in contours:
        cv2.drawContours(contour_image, [contour], -1, (255, 255, 255, 255), 2)
    
    return contour_image
#座標情報のリスト
def extract_lines(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)  # 画像をグレースケールに変換
    edges = cv2.Canny(gray, threshold1=100, threshold2=200)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=20, maxLineGap=5)
    return lines
#直線の方程式の生成
def generate_equation_from_lines(lines):
    equation = "y = "
    valid_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if x1 == x2 or abs(x2 - x1) < 1e-6:
            continue

        slope = (y2 - y1) / (x2 - x1)
        y_intercept = y1 - slope * x1

        if slope != float("inf") and y_intercept != float("inf"):
            valid_lines.append((slope, y_intercept, x1, x2))

    if valid_lines:
        equation += "("
        for slope, y_intercept, x1, x2 in valid_lines:
            equation += f"{slope:.2f}x + {y_intercept:.2f} (for {x1} <= x <= {x2}), "
        equation = equation.rstrip(", ") + ")"
    else:
        equation = "No valid lines found."

    return equation

if __name__ == "__main__":
    main()