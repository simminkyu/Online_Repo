import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from tkinter import font
from PIL import Image, ImageDraw, ImageTk


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")  # 윈도우 제목 설정

        # 기본 설정 (이미지 크기, 색상, 펜 타입 등)
        self.image = Image.new("RGBA", (500, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.last_x, self.last_y = None, None
        self.shape = "pen"  # 기본 도형은 펜
        self.pen_color = "black"  # 기본 펜 색상
        self.text_color = "black"  # 기본 텍스트 색상
        self.stroke = 5  # 기본 선 굵기
        self.pen_type = "기본"  # 기본 펜 타입

        # 캔버스 생성 및 이미지 표시 설정
        self.canvas = tk.Canvas(self.root, width=500, height=700)
        self.canvas.pack()
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor=tk.NW)

        # UI 버튼 생성
        self.create_buttons()

        # 마우스 이벤트 처리 (클릭, 드래그)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.text_boxes = []  # 텍스트 상자 목록 초기화

    def create_buttons(self):
        # 상단 메뉴와 버튼들을 생성하는 함수
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill=tk.X)

        buttons = [
            ("펜", self.toggle_pen_menu), # 펜 버튼
            ("지우개", self.set_eraser), # 지우개 버튼
            ("펜 색상", self.choose_pen_color), # 펜 색상 버튼
            ("텍스트 색상", self.choose_text_color), # 텍스트 색상 버튼
            ("텍스트", self.add_text), # 텍스트 버튼
            ("전체 지우기", self.clear_canvas), # 전체 지우기 버튼
            ("저장", self.save_image), # 저장 버튼
        ]
        for i, (text, command) in enumerate(buttons):
            tk.Button(self.menu_frame, text=text, command=command).grid(row=0, column=i)

        # 선 굵기 슬라이더
        self.stroke_label = tk.Label(self.menu_frame, text="선 굵기:")
        self.stroke_label.grid(row=0, column=8, sticky="w")
        self.stroke_scale = tk.Scale(self.menu_frame, from_=1, to=20, orient=tk.HORIZONTAL)
        self.stroke_scale.set(self.stroke)
        self.stroke_scale.grid(row=0, column=9)

        # 글꼴 크기 슬라이더
        self.font_size_label = tk.Label(self.menu_frame, text="텍스트 크기:")
        self.font_size_label.grid(row=0, column=10, sticky="w")
        self.font_size_scale = tk.Scale(self.menu_frame, from_=1, to_=100, orient=tk.HORIZONTAL)
        self.font_size_scale.set(20)
        self.font_size_scale.grid(row=0, column=11)

    def toggle_pen_menu(self):
        # 펜 종류 메뉴를 표시하는 함수
        pen_types = ["기본", "두껍게", "가늘게", "점선"]
        pen_type_menu = tk.Menu(self.root, tearoff=0)
        for pen_type in pen_types:
            pen_type_menu.add_command(label=pen_type, command=lambda pt=pen_type: self.set_pen_type(pt))
        pen_type_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())  # 메뉴 표시 위치

    def set_pen_type(self, pen_type):
        # 선택한 펜 타입에 따라 펜 굵기 설정
        self.pen_type = pen_type
        if pen_type == "기본":
            self.stroke = 5  # 기본 펜 굵기
        elif pen_type == "두껍게":
            self.stroke = 10  # 두껍게 펜 굵기
        elif pen_type == "가늘게":
            self.stroke = 1  # 가늘게 펜 굵기
        elif pen_type == "점선":
            self.stroke = 5  # 점선 펜 굵기
        print(f"현재 선택된 펜 종류: {pen_type} / 굵기: {self.stroke}")

    def set_eraser(self):
        # 지우개 모드로 변경
        self.shape = "eraser"
        print("지우개 활성화됨")

    def choose_pen_color(self):
        # 사용자가 펜 색상을 선택할 수 있도록 하는 함수
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def choose_text_color(self):
        # 사용자가 텍스트 색상을 선택할 수 있도록 하는 함수
        color = colorchooser.askcolor()[1]
        if color:
            self.text_color = color

    def on_click(self, event):
        # 마우스를 클릭했을 때 좌표 저장
        self.last_x, self.last_y = event.x, event.y

    def on_drag(self, event):
        # 마우스를 드래그할 때 그리기 작업 수행
        if self.shape == "pen":
            pen_width = self.stroke
            if self.pen_type in ["기본", "두껍게"]:
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color, width=pen_width)
            elif self.pen_type == "가늘게":
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color, width=1)
            elif self.pen_type == "점선":
                self.draw_dotted_line(self.last_x, self.last_y, event.x, event.y)

            self.update_canvas_image()
            self.last_x, self.last_y = event.x, event.y
        elif self.shape == "eraser":
            # 지우개 모드에서 마우스를 드래그할 때 배경색으로 덮음
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill="white", width=self.stroke)
            self.update_canvas_image()
            self.last_x, self.last_y = event.x, event.y

    def draw_dotted_line(self, x1, y1, x2, y2):
        # 점선 그리기 (두 점 사이를 점선으로 연결)
        step = 10  # 점선 간격 설정
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5  # 두 점 사이의 거리 계산
        for i in range(0, int(distance / step)):
            start_x = x1 + (i * step) * (x2 - x1) / distance
            start_y = y1 + (i * step) * (y2 - y1) / distance
            end_x = x1 + ((i + 1) * step) * (x2 - x1) / distance
            end_y = y1 + ((i + 1) * step) * (y2 - y1) / distance
            self.draw.line([(start_x, start_y), (end_x, end_y)], fill=self.pen_color, width=self.stroke)

    def update_canvas_image(self):
        # 이미지 객체를 캔버스에 업데이트
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor=tk.NW)

    def add_text(self):
        # 사용자가 입력한 텍스트를 캔버스에 추가
        text = simpledialog.askstring("텍스트 입력", "추가할 텍스트 입력:")
        if text:
            x = simpledialog.askinteger("X 좌표", "텍스트의 X 좌표 입력 (0~500):")
            y = simpledialog.askinteger("Y 좌표", "텍스트의 Y 좌표 입력 (0~700):")
            font_size = self.font_size_scale.get()
            self.canvas.create_text(x, y, text=text, fill=self.text_color, font=("Arial", font_size))

    def clear_canvas(self):
        # 캔버스를 초기화 (흰색 배경으로 설정)
        self.image = Image.new("RGBA", (500, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas_image()

    def save_image(self):
        # 이미지를 파일로 저장
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.image.save(file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
