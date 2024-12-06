import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from PIL import Image, ImageDraw, ImageTk


class DrawingApp:
    def __init__(self, root):
        # 애플리케이션 초기화
        self.root = root
        self.root.title("Drawing App")  # 윈도우 제목 설정

        # 기본 설정
        self.image = Image.new("RGBA", (500, 700), "white")  # 새로운 이미지 객체 생성 (흰 배경)
        self.draw = ImageDraw.Draw(self.image)  # 이미지를 그리기 위한 객체
        self.last_x, self.last_y = None, None  # 마우스를 클릭한 좌표
        self.shape = "pen"  # 초기 도형은 펜
        self.pen_color = "black"  # 펜 기본 색상
        self.text_color = "black"  # 텍스트 기본 색상
        self.stroke = 5  # 선의 기본 굵기
        self.pen_type = "normal"  # 기본 펜 타입 (정상 펜)

        # 캔버스 생성 (그림을 그릴 영역)
        self.canvas = tk.Canvas(self.root, width=500, height=700)
        self.canvas.pack()  # 캔버스 화면에 배치

        # 이미지가 캔버스에 표시되도록 연결
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor=tk.NW)

        # 사용자 인터페이스 요소 (버튼 등) 생성
        self.create_buttons()

        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.on_click)  # 마우스 클릭 시 호출
        self.canvas.bind("<B1-Motion>", self.on_drag)  # 마우스 드래그 시 호출

    def create_buttons(self):
        # 다양한 도형을 선택하거나 설정할 수 있는 버튼 생성
        self.pen_button = tk.Button(self.root, text="펜", command=self.toggle_pen_menu)
        self.pen_button.pack(side=tk.LEFT)  # 왼쪽에 배치

        self.rect_button = tk.Button(self.root, text="네모", command=lambda: self.set_shape("rect"))
        self.rect_button.pack(side=tk.LEFT)

        self.line_button = tk.Button(self.root, text="선", command=lambda: self.set_shape("line"))
        self.line_button.pack(side=tk.LEFT)

        self.circle_button = tk.Button(self.root, text="원", command=lambda: self.set_shape("circle"))
        self.circle_button.pack(side=tk.LEFT)

        self.erase_button = tk.Button(self.root, text="지우개", command=self.set_eraser)
        self.erase_button.pack(side=tk.LEFT)

        # 펜 색상 변경 버튼
        self.color_button = tk.Button(self.root, text="펜 색상", command=self.choose_pen_color)
        self.color_button.pack(side=tk.LEFT)

        # 텍스트 색상 변경 버튼
        self.text_color_button = tk.Button(self.root, text="텍스트 색상", command=self.choose_text_color)
        self.text_color_button.pack(side=tk.LEFT)

        # 캔버스를 전체 지우는 버튼
        self.clear_button = tk.Button(self.root, text="전체지우기", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        # 현재 그린 이미지를 저장하는 버튼
        self.save_button = tk.Button(self.root, text="저장", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        # 이미지를 열어서 불러오는 버튼
        self.open_button = tk.Button(self.root, text="열기", command=self.open_image)
        self.open_button.pack(side=tk.LEFT)

        # 선 굵기 조정 슬라이더
        self.stroke_label = tk.Label(self.root, text="선 굵기:")
        self.stroke_label.pack(side=tk.LEFT)

        self.stroke_scale = tk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL)
        self.stroke_scale.set(5)  # 기본 선 굵기 설정
        self.stroke_scale.pack(side=tk.LEFT)

        # 텍스트 추가 버튼
        self.text_button = tk.Button(self.root, text="텍스트", command=self.add_text)
        self.text_button.pack(side=tk.LEFT)

        # 펜 종류 선택을 위한 메뉴 추가
        self.pen_menu = tk.Menu(self.root, tearoff=0)
        self.pen_menu.add_command(label="기본 펜", command=lambda: self.set_pen_type("normal"))
        self.pen_menu.add_command(label="두꺼운 펜", command=lambda: self.set_pen_type("thick"))
        self.pen_menu.add_command(label="점선", command=lambda: self.set_pen_type("dotted"))
        self.pen_menu.add_command(label="지우개", command=self.set_eraser)

    def toggle_pen_menu(self):
        # 펜 메뉴 토글 (펜 버튼을 누르면 펜 종류 메뉴 표시)
        try:
            self.pen_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
        except Exception as e:
            print("펜 메뉴 표시 오류:", e)

    def set_pen_type(self, pen_type):
        # 펜 종류 설정
        self.pen_type = pen_type
        print(f"현재 선택된 펜 종류: {pen_type}")

    def set_eraser(self):
        # 지우개 모드로 설정
        self.shape = "eraser"
        print("지우개 활성화됨")

    def choose_pen_color(self):
        # 펜 색상을 사용자가 선택할 수 있도록 하는 함수
        color = colorchooser.askcolor()[1]  # 색상 선택 대화 상자
        if color:
            self.pen_color = color  # 선택한 색상으로 펜 색상 변경

    def choose_text_color(self):
        # 텍스트 색상을 사용자가 선택할 수 있도록 하는 함수
        color = colorchooser.askcolor()[1]  # 색상 선택 대화 상자
        if color:
            self.text_color = color  # 선택한 색상으로 텍스트 색상 변경

    def on_click(self, event):
        # 마우스 버튼을 클릭했을 때 발생하는 이벤트
        # 클릭한 좌표 (x, y)를 저장하여 그리기 시작 위치를 설정
        self.last_x, self.last_y = event.x, event.y

    def on_drag(self, event):
        # 마우스를 드래그하면서 발생하는 이벤트
        # 마우스를 움직일 때마다 그리기를 수행
        x, y = event.x, event.y
        stroke = self.stroke_scale.get()  # 선 굵기 가져오기

        # 현재 선택된 도형에 따라 그림을 그리기
        if self.shape == "pen":
            self.draw_pen(x, y, stroke)
        elif self.shape == "line":
            self.draw.line([(self.last_x, self.last_y), (x, y)], fill=self.pen_color, width=stroke)
        elif self.shape == "rect":
            self.draw.rectangle([self.last_x, self.last_y, x, y], outline=self.pen_color, width=stroke)
        elif self.shape == "circle":
            self.draw.ellipse([self.last_x, self.last_y, x, y], outline=self.pen_color, width=stroke)
        elif self.shape == "eraser":
            self.draw.line([(self.last_x, self.last_y), (x, y)], fill="white", width=stroke)

        # 마지막 좌표 업데이트
        self.last_x, self.last_y = x, y
        self.update_canvas_image()

    def draw_pen(self, x, y, stroke):
        # 펜 그리기 (펜 종류에 따라 다르게 그리기)
        if self.pen_type == "normal":
            self.draw.line([(self.last_x, self.last_y), (x, y)], fill=self.pen_color, width=stroke)
        elif self.pen_type == "thick":
            self.draw.line([(self.last_x, self.last_y), (x, y)], fill=self.pen_color, width=stroke * 2)
        elif self.pen_type == "dotted":
            # 점선 처리 (적절한 간격으로 선을 그리도록 설정)
            step = 10  # 점선의 길이
            for i in range(0, int(self.distance(self.last_x, self.last_y, x, y) / step)):
                start_x = self.last_x + (i * step) * (x - self.last_x) / self.distance(self.last_x, self.last_y, x, y)
                start_y = self.last_y + (i * step) * (y - self.last_y) / self.distance(self.last_x, self.last_y, x, y)
                end_x = self.last_x + ((i + 1) * step) * (x - self.last_x) / self.distance(self.last_x, self.last_y, x, y)
                end_y = self.last_y + ((i + 1) * step) * (y - self.last_y) / self.distance(self.last_x, self.last_y, x, y)
                self.draw.line([(start_x, start_y), (end_x, end_y)], fill=self.pen_color, width=stroke)

    def distance(self, x1, y1, x2, y2):
        # 두 점 사이의 거리 계산 (점선 그리기 용)
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def update_canvas_image(self):
        # 캔버스에 이미지를 업데이트
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor=tk.NW)

    # 추가적인 메서드들 (저장, 열기, 지우기 등)
    def clear_canvas(self):
        self.image = Image.new("RGBA", (500, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.image.save(file_path)

    def open_image(self):
        file_path = filedialog.askopenfilename(defaultextension=".png")
        if file_path:
            self.image = Image.open(file_path)
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas_image()

    def add_text(self):
        # 텍스트 추가하는 기능 구현 (예시)
        text = simpledialog.askstring("텍스트 입력", "추가할 텍스트 입력:")
        if text:
            self.draw.text((self.last_x, self.last_y), text, fill=self.text_color)
            self.update_canvas_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
