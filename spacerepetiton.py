import pandas as pd

def loadData(file_path) -> pd.DataFrame:
    return pd.read_csv(file_path)

def generateSessionQueue():
    """
    Tạo queue cho session:
    - lấy toàn bộ từ falseQueue (chưa thuộc) trước
    - rồi tới trueQueue (đã thuộc)
    """
    global falseQueue
    global trueQueue
    global sessionQueue
    for element in falseQueue:          # Thêm tất cả phần tử trong falseQueue
        sessionQueue.append(element)
    for element in trueQueue:           # Sau đó thêm phần tử trong trueQueue
        sessionQueue.append(element)
    falseQueue.clear()                  # Xóa falseQueue (vì đã copy vào session)
    trueQueue.clear()                   # Xóa trueQueue (vì đã copy vào session)
    #Nếu hong xóa thì khi tụi bây chạy đợt session luyện tập tiếp theo thì mấy từ này nó sẽ lặp lại thêm lần nữa, thì lúc đó tụi bây sẽ bị học trùng lặp


def checkAnswer(data) -> bool:
    """
    Check coi đáp án users nhập có đúng hong
    """
    global questionCol  #col là column á mấy má(ý là tên t tự chế để chia ra cột từ vựng này kia thoi)
    global answerCol
    message = f"{data[questionCol]}: "   # Hiển thị câu hỏi (từ vựng)
    answer = input(message)              # Người dùng nhập nghĩa của từ
    return answer == data[answerCol]     # So sánh với đáp án đúng (True/False)


def practiceQuestion(data) -> int:
    """
    Luyện tập từng từ:
    - Nếu đúng ngay lần đầu → return 1 (kiủ nhớ tốt kh cần hỏi lại)
    - Nếu sai lần đầu nhưng đúng lần hai → return 2 (sai rr mới đúng)
    - Nếu sai cả hai → return 0
    """
    if checkAnswer(data):                # Nếu lần 1 đúng
        return 1
    else:                                # Nếu lần 1 sai
        if checkAnswer(data):            # Hỏi lại lần 2
            return 2                     # Đúng lần 2
        else:
            return 0                     # Sai cả 2 lần


def runSession():
    """
    Chạy 1 phiên học:
    - Gộp falseQueue + trueQueue → sessionQueue
    - Với mỗi từ trong session:
        + Nếu practiceQuestion = 0 → sai cả 2 → cho lại vào cuối session
        + Nếu = 1 → đúng ngay → cho qua trueQueue
        + Nếu = 2 → đúng lần 2 → cho qua falseQueue (để ôn lại sau)
    """
    global sessionQueue
    global falseQueue
    global trueQueue
    generateSessionQueue()               # Tạo queue mới cho session

    for data in sessionQueue:            # Lặp qua từng từ trong session
        match practiceQuestion(data):    # Dùng match-case để kiểm kết quả
            case 0:
                sessionQueue.append(data)  # Sai → cho quay lại cuối session
            case 1:
                trueQueue.append(data)     # Đúng ngay → cho qua trueQueue
            case 2:
                falseQueue.append(data)    # Đúng lần 2 → cho qua falseQueue

    sessionQueue.clear()                 # Xóa sessionQueue khi xong session


def practice():
    """
    Hàm tổng điều khiển toàn bộ quá trình học.
    Hỏi người dùng có mún tiếp tục học hong sau mỗi session.
    """
    global _continue
    while _continue:                     # Nếu vẫn muốn học
        runSession()                     # Chạy 1 session
        continueMessage = (
            "Có mún học nữa hong? (Qua session mới nhó)\n"
            "y for yes, n for no\n"
        )
        continueAnswer = input(continueMessage).strip().lower()  #lower là để chuyển về chữ thường đồ á. vd bấm yes l y hay Y đều akelo
        match continueAnswer:            # Nếu người dùng nhập y hoặc n
            case 'y':
                _continue = True
            case 'n':
                _continue = False


#  CHƯƠNG TRÌNH CHÍNH
file = "vocab.csv"           # file mình tạo
questionCol = "Vocab"        # Cột câu hỏi
answerCol = "Definition"     # Cột đáp án
data = loadData(file)        # Đọc dữ liệu từ file CSV

# Khởi tạo các hàng đợi (queue)
falseQueue = []              # Từ sai (chưa thuộc)
trueQueue = []               # Từ đúng (đã thuộc)
sessionQueue = []            # Queue cho session hiện tại
_continue = True             # Biến điều khiển lặp (True = còn học)

# Ban đầu, cho tất cả từ vựng vào falseQueue
for index, row in data.iterrows(): #Lặp qua từng hàng trong bảng data,mỗi vòng lặp lấy ra chỉ số hàng (index) và nội dung hàng đó (row)

    falseQueue.append(row)

# Bắt đầu luyện tập
practice()
