import os
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta

from workalendar.asia import SouthKorea


def get_korean_weekday(num):
    WEEKDAYS = ['일', '월', '화', '수', '목', '금', '토']
    return WEEKDAYS[num]


class LectureFolderCreator:
    """
    폴더 생성기 클래스
    """

    def __init__(self):
        """
        초기화 함수
        """
        self.path_var = None
        self.name_var = None
        self.date_var = None
        self.total_weeks_var = None
        self.midterm_var = None
        self.final_var = None
        self.tree = None
        self.root = tk.Tk()
        self.root.geometry("640x480")
        self.root.title("강의 주차별 폴더 생성기")

        # UI 생성
        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        """
        UI 위젯 생성 함수
        """
        # 좌측 프레임
        left_frame = tk.Frame(self.root, width=320, height=480)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 사용자가 지정한 경로
        self.path_var = tk.StringVar()
        tk.Label(left_frame, text="저장폴더 경로", anchor="center").grid(row=0, column=0, pady=5)
        tk.Entry(left_frame, textvariable=self.path_var).grid(row=1, column=0, pady=5, sticky="we")

        # 강의명
        self.name_var = tk.StringVar()
        tk.Label(left_frame, text="강의명", anchor="center").grid(row=2, column=0, pady=5)
        tk.Entry(left_frame, textvariable=self.name_var).grid(row=3, column=0, pady=5)

        # 시작일자
        self.date_var = tk.StringVar()
        tk.Label(left_frame, text="시작일자", anchor="center").grid(row=4, column=0, pady=5)
        tk.Entry(left_frame, textvariable=self.date_var).grid(row=5, column=0, pady=5)

        # 총 주차
        self.total_weeks_var = tk.StringVar()
        tk.Label(left_frame, text="총 주차", anchor="center").grid(row=6, column=0, pady=5)
        tk.Entry(left_frame, textvariable=self.total_weeks_var).grid(row=7, column=0, pady=5)

        # 중간고사/기말고사
        tk.Label(left_frame, text="중간/기말고사 주차", anchor="center").grid(row=8, column=0, pady=5)
        midterm_frame = tk.Frame(left_frame)
        midterm_frame.grid(row=9, column=0, pady=5)
        self.midterm_var = tk.StringVar()
        tk.Label(midterm_frame, text="중간고사 주차", anchor="center").grid(row=0, column=0)
        tk.Entry(midterm_frame, textvariable=self.midterm_var, width=5).grid(row=0, column=1)
        tk.Label(midterm_frame, text="주차", anchor="center").grid(row=0, column=2)

        final_frame = tk.Frame(left_frame)
        final_frame.grid(row=10, column=0, pady=5)
        self.final_var = tk.StringVar()
        tk.Label(final_frame, text="기말고사 주차", anchor="center").grid(row=0, column=0)
        tk.Entry(final_frame, textvariable=self.final_var, width=5).grid(row=0, column=1)
        tk.Label(final_frame, text="주차", anchor="center").grid(row=0, column=2)

        # 폴더 미리보기
        tk.Button(left_frame, text="폴더 미리보기", command=self.preview).grid(row=11, column=0, pady=10)

        # 생성 버튼
        tk.Button(left_frame, text="폴더 생성", command=self.create_folders).grid(row=12, column=0, pady=10)

        # 우측 프레임
        right_frame = tk.Frame(self.root, width=320, height=480)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Treeview
        self.tree = ttk.Treeview(right_frame)
        self.tree.heading("#0", text="폴더명")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def preview(self):
        # Treeview 초기화
        self.tree.delete(*self.tree.get_children())

        # 사용자 입력값 읽기
        name = self.name_var.get()
        date_str = self.date_var.get()
        weeks = self.total_weeks_var.get()
        midterm = self.midterm_var.get()
        final = self.final_var.get()

        try:
            # 시작일자와 주차 수를 읽어옴
            start_date = datetime.strptime(date_str, "%Y-%m-%d")
            total_weeks = int(weeks)
        except ValueError:
            # 날짜나 주차 수가 잘못 입력되면 함수를 종료함
            return

        # 폴더 구조 생성
        weeks = []
        cur_date = start_date
        cur_week = 1
        cal = SouthKorea()
        for i in range(1, total_weeks + 1):
            if midterm.strip() != "" and i == int(midterm):
                week_str = f"{cur_week}주차 ({cur_date.strftime('%Y.%m.%d.')}{get_korean_weekday(cur_date.weekday())}) - 중간고사"
            elif final.strip() != "" and i == int(final):
                week_str = f"{cur_week}주차 ({cur_date.strftime('%Y.%m.%d.')}{get_korean_weekday(cur_date.weekday())}) - 기말고사"
            else:
                week_str = f"{cur_week}주차 ({cur_date.strftime('%Y.%m.%d.')}{get_korean_weekday(cur_date.weekday())})"

            # 주차 추가
            weeks.append({
                "name": week_str,
                "start": cur_date,
                "end": cur_date + timedelta(days=6)
            })

            cur_date += timedelta(days=7)
            cur_week += 1

        # Treeview에 추가
        parent_id = self.tree.insert("", "end", text=name, open=True)
        for week in weeks:
            date_str = f"{week['start'].strftime('%Y.%m.%d')} ~ {week['end'].strftime('%Y.%m.%d')}"
            # 부모 노드에 주차 노드 추가
            self.tree.insert(parent_id, "end", text=week["name"], values=(date_str))

    def create_folders(self):
        # 사용자 입력값 읽기
        path = self.path_var.get()
        name = self.name_var.get()
        date_str = self.date_var.get()
        weeks = self.total_weeks_var.get()
        midterm = self.midterm_var.get()
        final = self.final_var.get()

        try:
            start_date = datetime.strptime(date_str, "%Y-%m-%d")
            total_weeks = int(weeks)
        except ValueError:
            return

        # 폴더 구조 생성
        weeks = []
        cur_date = start_date
        cur_week = 1
        for i in range(1, total_weeks + 1):
            if midterm.strip() != "" and i == int(midterm):
                week_str = f"{cur_week}주차 ({cur_date.strftime('%Y.%m.%d.')}{get_korean_weekday(cur_date.weekday())}) - 중간고사"
            elif final.strip() != "" and i == int(final):
                week_str = f"{cur_week}주차 ({cur_date.strftime('%Y.%m.%d.')}{get_korean_weekday(cur_date.weekday())}) - 기말고사"
            else:
                week_str = f"{cur_week}주차 ({cur_date.strftime('%Y.%m.%d.')}{get_korean_weekday(cur_date.weekday())})"

            # 주차 추가
            week_path = os.path.join(path, name, week_str)
            os.makedirs(week_path, exist_ok=True)
            weeks.append({
                "name": week_str,
                "path": week_path,
                "start": cur_date,
                "end": cur_date + timedelta(days=6)
            })

            cur_date += timedelta(days=7)
            cur_week += 1

        # Treeview 초기화
        self.tree.delete(*self.tree.get_children())

        # 생성된 폴더 구조 Treeview에 추가
        parent_id = self.tree.insert("", "end", text=name, open=True)
        for week in weeks:
            date_str = f"{week['start'].strftime('%Y.%m.%d')} ~ {week['end'].strftime('%Y.%m.%d')}"
            # 각 주차에 해당하는 노드 추가
            self.tree.insert(parent_id, "end", text=week["name"], values=(date_str))

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    creator = LectureFolderCreator()
    creator.run()
