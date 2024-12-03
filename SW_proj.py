from tkinter import *
from tkinter.colorchooser import *
from tkinter.simpledialog import *

# 함수 선언 부분
def mouseClick(event):
    global x1, y1, x2, y2
    x1 = event.x
    y1 = event.y

def mouseDrop(event):
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)

def getColor():
    global penColor
    color = askcolor()
    penColor = color[1]

def getWidth():
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요.",
                          minvalue=1, maxvalue=10)

def insertAction():
    # 삽입 버튼 클릭 시 동작할 코드 작성 (현재는 아무런 동작을 하지 않음)
    print("삽입 버튼이 클릭되었습니다.")  # 예시로 출력하는 코드

# 전역 변수 선언 부분
window = None
canvas = None
x1, x2, y1, y2 = None, None, None, None  # 선의 시작점과 끝점
penColor = 'black'
penWidth = 5

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("그림판 비슷한 프로그램")
    
    # 캔버스 생성
    canvas = Canvas(window, height=300, width=300)
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack()

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    # 설정 메뉴
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)

    # 삽입 버튼 메뉴
    insertMenu = Menu(mainMenu)  # "삽입"이라는 이름의 하위 메뉴를 생성하여 mainMenu에 연결
    mainMenu.add_cascade(label="삽입", menu=insertMenu)  # "삽입" 메뉴를 메인 메뉴에 추가하고, 해당 메뉴 클릭 시 insertMenu가 펼쳐지도록 설정
    insertMenu.add_command(label="삽입 버튼", command=insertAction)  # "삽입 버튼" 항목을 추가하고, 클릭 시 insertAction 함수를 실행하도록 설정

    window.mainloop()