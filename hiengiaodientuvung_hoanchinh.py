import pandas
import random
from PyQt6.QtWidgets import QApplication, QWidget
import sys
from tuvung import *  # --- HÀM 1: ĐÁNH GIÁ ---

def danhgia(D, T):
    # S = Số lần sai, T = Tổng số lần đoán
    ti_le_dung= (T-D)/T
    # Đánh giá dựa trên tỉ le ĐÚNG
    if ti_le_dung <= 0.25:
        k = f"""tỉ lệ nhập đúng của bạn là :{ti_le_dung}
        Bạn mất gốc rồi, ráng học lên nhé. 
           Ngày mai ôn lại liền nha."""
    elif ti_le_dung <= 0.5:
        k = f"""tỉ lệ nhập đúng của bạn là:{ti_le_dung}
        Bạn thuộc ít quá. 
         2 ngày sau ôn lại nhé"""
    elif ti_le_dung <= 0.65:
        k = f"""tỉ lệ nhập đúng của bạn là :{ti_le_dung}
        Bạn chưa thuộc lắm đó. 
         3 ngày sau ôn lại nhé"""
    elif ti_le_dung <= 0.8:
        k = f"""tỉ lệ nhập đúng của bạn là :{ti_le_dung}
        Tạm ổn rồi. 
        4 ngày sau ôn lại nhé"""
    else:  #lớn hơn 0.8
        k = f"""tỉ lệ nhập đúng của bạn là :{ti_le_dung}
        Chúc mừng, bạn gần thuộc bài rồi. 
             Tuần sau ôn lại nhé."""
    return k
# --- HÀM 2: BẮT ĐẦU HỌC ---
# Hàm này sẽ được gọi KHI TA NHẤN NÚT "Bắt đầu học" (btnbatdauhoc)
def bat_dau_hoc():
    try:
        # 1. Lấy tên file và đọc dữ liệu
        a = form.lnenhapfile.text()
        data = pandas.read_excel(a)
        # 2. LƯU TRỮ TRẠNG THÁI
        #    Chúng ta lưu danh sách và điểm số vào 'form'
        #    để các hàm khác có thể dùng
        form.list_of_list = data.values.tolist()
        form.D = 0  # Số lần đúng
        form.T = 0  # Tổng số lần đoán
        # 3. Cập nhật giao diện
        form.txtlannhapsai_2.setText(f"{form.D} / {form.T}")
        # 5. Hiển thị từ đầu tiên
        hien_tu_moi()
    except FileNotFoundError:
        form.lnetienganh.setText("LỖI: Không tìm thấy file")
    except Exception as e:
        form.lnetienganh.setText(f"LỖI: {e}")
# --- HÀM 3: HIỂN THỊ TỪ MỚI ---
# Hàm này được gọi bởi (Hàm 2) và (Hàm 4)
def hien_tu_moi():
    # Kiểm tra xem danh sách đã lưu có còn từ không
    if len(form.list_of_list) > 0:
        # 1. Chọn từ ngẫu nhiên
        form.randomlist = random.choice(form.list_of_list)
        # 2. SỬA LỖI: Dùng .setText() để GÁN văn bản
        form.lnetienganh.setText(form.randomlist[0])
    else:
        # ĐÃ HỌC HẾT TỪ!
        form.lnetienganh.setText("HOÀN THÀNH!")
        form.lnetiengviet.setText("HOÀN THÀNH!")
        # Hiển thị đánh giá
        # SỬA LỖI: Phải truyền S và T vào
        k = danhgia(form.D, form.T)
        form.txtloikhuyen.setText(k)
# --- HÀM 4: KIỂM TRA ĐÁP ÁN ---
# Hàm này sẽ được gọi KHI TA NHẤN NÚT "Kiểm tra và hiện từ mới" (btnsubmit)
# (Chúng ta dùng nó làm nút "Kiểm tra")
def kiem_tra_dap_an():
    try:
        # 1. Lấy câu trả lời của người dùng
        b = form.lnetiengviet.text().strip()  # .strip() để xóa khoảng trắng
        # 2. Lấy đáp án đúng (đã được lưu trong form)
        dap_an_dung = form.randomlist[1]
        # 3. Cập nhật điểm
        form.T = form.T + 1  # Tăng tổng số lần đoán
        if b == dap_an_dung:
            # Nếu ĐÚNG, xóa từ này khỏi danh sách
            form.list_of_list.remove(form.randomlist)
            #tăng số lần đúng
            form.D = form.D + 1
        else:
            form.txtloikhuyen.setText(f"Đáp án đúng là {dap_an_dung} ")
        # 4. Cập nhật giao diện điểm số
        form.txtlannhapsai_2.setText(f"{form.D} / {form.T}")
        # 5. Hiển thị từ tiếp theo
        hien_tu_moi()
    except AttributeError:
        # Lỗi này xảy ra nếu người dùng nhấn "Kiểm tra"
        # trước khi nhấn "Học" (form.current_word chưa tồn tại)
        form.txtloikhuyen.setText("Bạn phải nhấn 'Học' trước!")
    except Exception as e:
        form.txtloikhuyen.setText(f"Lỗi: {e}")
# --- PHẦN KHỞI TẠO CHÍNH ---
app = QApplication(sys.argv)
window = QWidget()
form = Ui_Form()
form.setupUi(window)
form.btnbatdauhoc.clicked.connect(bat_dau_hoc)
form.btnsubmit.clicked.connect(kiem_tra_dap_an)
window.show()
app.exec()