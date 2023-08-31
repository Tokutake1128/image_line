import streamlit as st
import cv2
import numpy as np

def main():
    st.title("推しのすぅ式化システム")
    
    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = read_image(uploaded_file)
        st.image(image, caption="アップロード画像", use_column_width=True)
        
        # スライダーでエッジの閾値を設定
        max_threshold = 255
        edge_threshold = st.slider("エッジの閾値", min_value=1, max_value=max_threshold, value=100)
        st.write("閾値が大きいほど線分は少なくなり，数式も短くなります．")
        edges_image = detect_edges(image, edge_threshold)
        st.image(edges_image, caption="抽出された線分", use_column_width=True)
        
        lines = extract_lines(edges_image)
        
        if st.button("近似式を算出する"):
            equation = generate_equation_from_lines(lines)
            st.write("結果:", equation)

def read_image(uploaded_file):
    image = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def detect_edges(image, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=threshold, threshold2=2*threshold)
    return edges

def extract_lines(edges_image):
    lines = cv2.HoughLinesP(edges_image, 1, np.pi / 180, threshold=50, minLineLength=20, maxLineGap=5)
    return lines

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
            equation += f"{slope:.2f}x + {y_intercept:.2f} ({x1} <= x <= {x2}), "
        equation = equation.rstrip(", ") + ")"
    else:
        equation = "No valid lines found."

    return equation

if __name__ == "__main__":
    main()
