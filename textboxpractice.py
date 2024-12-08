import tkinter as tk

class SelectAreaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("구역 지정 및 텍스트 입력")

        # 캔버스 생성
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        # 드래그 상태 관리 변수
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.text_widget = None

        # 마우스 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def on_mouse_press(self, event):
        # 드래그 시작 위치 저장
        self.start_x = event.x
        self.start_y = event.y

        # 이전에 그려진 사각형이 있으면 삭제
        if self.rect:
            self.canvas.delete(self.rect)

        # 새로운 사각형 그리기 시작
        self.rect = None

    def on_mouse_drag(self, event):
        # 드래그 중인 구역을 실시간으로 업데이트
        if self.rect:
            self.canvas.delete(self.rect)

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="blue")

    def on_mouse_release(self, event):
        # 드래그가 끝난 후, 구역의 좌표를 출력
        end_x, end_y = event.x, event.y
        print(f"구역이 선택되었습니다: 시작({self.start_x}, {self.start_y}), 끝({end_x}, {end_y})")

        # 지정된 구역 안에 Text 위젯 생성
        if self.text_widget:
            self.text_widget.destroy()  # 이전에 생성된 텍스트 위젯을 제거

        # Text 위젯을 드래그한 영역에 맞게 생성
        self.text_widget = tk.Text(self.root, wrap="word", height=5, width=20)
        self.text_widget.place(x=self.start_x, y=self.start_y, width=abs(end_x - self.start_x), height=abs(end_y - self.start_y))

# Tkinter 윈도우 생성
root = tk.Tk()

# 애플리케이션 객체 생성
app = SelectAreaApp(root)

# GUI 실행
root.mainloop()