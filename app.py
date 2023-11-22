from flask import Flask, render_template, request, send_file
from io import BytesIO
import matplotlib.pyplot as plt

def result(소비카테고리, 소비금액, y입력2020, y입력2021, y입력2022):
    from matplotlib import font_manager, rc
    font_path = "C:/Windows/Fonts/malgun.ttf"  # 사용하고자 하는 한글 폰트 파일 경로
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
    x축 = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    y축2020 = [int(금액) for 금액 in y입력2020.split(',')]
    y축2021 = [int(금액) for 금액 in y입력2021.split(',')]
    y축2022 = [int(금액) for 금액 in y입력2022.split(',')]
    평균2020 = sum(y축2020) / len(y축2020)
    평균2021 = sum(y축2021) / len(y축2021)
    평균2022 = sum(y축2022) / len(y축2022)
    소비카테고리 = 소비카테고리.split(',')
    소비금액 = 소비금액.split(',')
    소비금액 = [int(금액) for 금액 in 소비금액]
    이번달소비금액합계 = sum(소비금액)

    print(f"작년 평균 소비 금액: {평균2020}")
    print(f"재작년 평균 소비 금액: {평균2021}")
    print(f"올해 평균 소비 금액: {평균2022}")
    print(f"이번달 소비 금액 합계: {이번달소비금액합계}")

    plt.subplot(3, 1, 1)
    plt.title("지난 3년간 월별 카드값 사용 내역 (단위: 만)")
    plt.plot(x축, y축2020, marker="o", label="재작년")
    plt.plot(x축, y축2021, marker="o", label="작년")
    plt.plot(x축, y축2022, marker="o", label="올해")
    plt.legend()
    plt.xlabel("월")
    plt.ylabel("카드사용금액")
    plt.grid(True, axis="y")

    x = ["이번달 소비금액", "재작년 평균", "작년 평균", "올해 평균"]
    plt.figure()
    plt.title("이번달 소비금액과 지난 3년의 평균치 소비금액 비교그래프 (단위: 만)")
    plt.bar(x[0], 이번달소비금액합계, label="이번달")
    plt.bar(x[1], 평균2020, label="재작년")
    plt.bar(x[2], 평균2021, label="작년")
    plt.bar(x[3], 평균2022, label="올해")
    plt.legend()
    plt.xlabel("이번달 소비금액 & 연도별 평균 소비금액")
    plt.ylabel("카드사용금액")
    plt.grid(True, axis="y", linestyle=":")

    plt.figure()
    plt.title("이번달 소비금액 카테고리별 비율")
    plt.pie(소비금액, labels=소비카테고리, autopct="%.1f%%")
    plt.legend(소비카테고리)
    plt.show()

    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def post():
    global y입력2020, y입력2021, y입력2022, 소비카테고리, 소비금액
    y입력2020 = request.form['y입력2020']
    y입력2021 = request.form['y입력2021']
    y입력2022 = request.form['y입력2022']
    소비카테고리 = request.form['소비카테고리']
    소비금액 = request.form['소비금액']
    return result(소비카테고리, 소비금액, y입력2020, y입력2021, y입력2022)

@app.route('/home')
def home():
    return 'Hello, World!'

@app.route("/result", methods=['GET'])
def post2():
    return result([], [], "", "", "")
    
if __name__ == '__main__':
    app.run(debug=True)
