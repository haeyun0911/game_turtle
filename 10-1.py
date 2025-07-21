import turtle
import random

# --- 1. 화면 설정 ---
screen = turtle.Screen()
screen.setup(width=700, height=500)
screen.bgcolor("lightgray")
screen.title("거북이 경마 게임")
screen.tracer(0) # 화면 업데이트를 끔

# --- 2. 플레이어 거북이 설정 ---
players_data = [
    {"name": "초록 거북이", "color": "green", "start_y": 150},
    {"name": "파랑 거북이", "color": "blue", "start_y": 50},
    {"name": "빨강 거북이", "color": "red", "start_y": -50},
    {"name": "노랑 거북이", "color": "gold", "start_y": -150}
]

turtles = []

for player_info in players_data:
    new_turtle = turtle.Turtle()
    new_turtle.color(player_info["color"])
    new_turtle.shape("turtle")
    new_turtle.penup()
    new_turtle.goto(-300, player_info["start_y"])
    new_turtle.speed(0)
    turtles.append(new_turtle)

# --- 3. 결승선 그리기 ---
finish_line_x = 280
finish_line_pen = turtle.Turtle()
finish_line_pen.speed(0)
finish_line_pen.penup()
finish_line_pen.goto(finish_line_x, 200)
finish_line_pen.pendown()
finish_line_pen.pensize(5)
finish_line_pen.color("darkred")
finish_line_pen.setheading(270)
finish_line_pen.forward(400)
finish_line_pen.hideturtle()

# --- 4. 게임 상태 메시지 펜 설정 ---
game_status_pen = turtle.Turtle()
game_status_pen.speed(0)
game_status_pen.color("black")
game_status_pen.penup()
game_status_pen.hideturtle()
game_status_pen.goto(0, 200)

# --- 5. 게임 변수 ---
game_on = True
min_speed = 5
max_speed = 15
max_angle_change = 15
selected_turtle_color = "" # 플레이어가 선택한 거북이의 영어 색상 코드 (내부용)
selected_turtle_name = ""  # 플레이어가 선택한 거북이의 한글 이름 (출력용)

# --- 6. 플레이어 거북이 선택 ---
def choose_turtle():
    global selected_turtle_color, selected_turtle_name # 전역 변수 수정
    choice = ""
    while choice not in ["초록", "파랑", "빨강", "노랑"]:
        choice = input("어떤 거북이에 걸겠습니까? (초록, 파랑, 빨강, 노랑 중 하나를 입력하세요): ").strip()
        if choice not in ["초록", "파랑", "빨강", "노랑"]:
            print("잘못된 입력입니다. 다시 입력해주세요.")
            
    # 사용자가 선택한 한글 이름을 직접 저장합니다.
    selected_turtle_name = choice 

    # 그리고 그에 맞는 영어 색상 코드도 저장하여 내부 로직에서 사용합니다.
    if choice == "초록": selected_turtle_color = "green"
    elif choice == "파랑": selected_turtle_color = "blue"
    elif choice == "빨강": selected_turtle_color = "red"
    elif choice == "노랑": selected_turtle_color = "gold"
    
    print(f"'{selected_turtle_name}' 거북이를 선택하셨습니다. 경주를 시작합니다!")

# --- 7. 게임 진행 함수 ---
def race_step():
    global game_on

    if not game_on:
        return

    winner_found = False
    winning_turtle_index = -1 # 승리한 거북이의 인덱스

    for i, t in enumerate(turtles):
        forward_distance = random.randint(min_speed, max_speed)
        angle_change = random.randint(-max_angle_change, max_angle_change)
        t.left(angle_change)

        current_x, current_y = t.xcor(), t.ycor()
        
        if current_y > 230 or current_y < -230:
            t.setheading(t.heading() + 180)
        
        t.forward(forward_distance)

        if t.xcor() >= finish_line_x:
            winning_turtle_index = i # 승리한 거북이의 인덱스 저장
            winner_found = True
            game_on = False
            break

    screen.update()

    if winner_found:
        game_status_pen.clear()
        # 승리한 거북이의 한글 이름을 players_data에서 가져옵니다.
        winning_turtle_name = players_data[winning_turtle_index]['name'] 
        winning_turtle_color_code = players_data[winning_turtle_index]['color'] # 비교를 위한 영어 색상 코드도 가져옵니다.

        if winning_turtle_color_code == selected_turtle_color: # 선택한 거북이의 색상 코드로 비교
            game_status_pen.write("축하합니다! 당신의 거북이가 승리했습니다.", 
                                  align="center", font=("Arial", 22, "bold"))
        else:
            game_status_pen.write(f"아쉽네요. {winning_turtle_name}가 먼저 도착했습니다.", # 한글 이름 출력
                                  align="center", font=("Arial", 22, "bold"))
    else:
        screen.ontimer(race_step, 50)

# --- 8. 게임 시작 프로세스 ---
choose_turtle()

game_status_pen.write("경주 시작! 잠시 기다려 주세요...", align="center", font=("Arial", 20, "normal"))
screen.update()

screen.ontimer(lambda: game_status_pen.clear(), 2000)
screen.ontimer(race_step, 2000)

# --- 9. 터틀 이벤트 루프 시작 ---
screen.mainloop()