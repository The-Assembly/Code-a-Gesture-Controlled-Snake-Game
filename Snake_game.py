import pygame
import random
import cv2
import mediapipe as mp
pygame.init()
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
hybrid = (23, 234, 223)
Snake_Window = pygame.display.set_mode([600,600])
pygame.display.set_caption("Snake_game")
pygame.display.update()
Clock = pygame.time.Clock()
Score_font = pygame.font.SysFont(None, 30)
def write_score(text,color,x,y):
    screen_text = Score_font.render(text,True,color)
    Snake_Window.blit(screen_text,[x,y])
def create_body(Snake_Window, color, Snake_list, Snake_Size):
    for x, y in Snake_list:
        pygame.draw.rect(Snake_Window, color , [x, y, Snake_Size, Snake_Size])
def Game_loop():
    game_exit = False
    game_over = False
    Snake_head_x = 100
    Snake_head_y = 100
    Score = 0
    Food_x = random.randint(2, 19) * 30
    Food_y = random.randint(2, 19) * 30
    Speed_x = 0
    Speed_y = 0
    Snake_Size = 30
    Snake_list = []
    Snake_length = 1
    fps = 60
    cam = cv2.VideoCapture(0)
    mphand = mp.solutions.hands
    mpHands = mphand.Hands()
    mpDraw  = mp.solutions.drawing_utils
    while not game_exit:
        if game_over == True:
            Snake_Window.fill(Red)
            write_score("Game Over, Press Space to play again  Your Score:" + str(Score), Green, 10, 100 )
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Game_loop()
        else:
            success, img = cam.read()
            image = cv2.resize(img,(600,600))
            output = mpHands.process(image)
            if output.multi_hand_landmarks:
                for landmarks in output.multi_hand_landmarks:
                    for id , pos in enumerate(landmarks.landmark):
                        height,width,z = image.shape
                        pos_x,pos_y = int(width*(pos.x)),int(height*(pos.y))
                        if id == 8:
                            cv2.circle(image, (300, 300), 500, Blue, cv2.FILLED)
                            cv2.circle(image, (300, 300), 30, Red, cv2.FILLED)
                            cv2.circle(image, (pos_x, pos_y), 25, hybrid, cv2.FILLED)
                            if pos_x > 350 and pos_y<350 and pos_y>250:
                                Speed_x = -3
                                Speed_y = 0
                            if pos_x < 250 and pos_y<350 and pos_y>250:
                                Speed_x = 3
                                Speed_y = 0
                            if pos_y < 250 and pos_x<350 and pos_x>250:
                                Speed_y = -3
                                Speed_x = 0
                            if pos_y > 350 and pos_x<350 and pos_x>250:
                                Speed_y = 3
                                Speed_x = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
            if abs(Snake_head_x-Food_x)<30 and abs(Snake_head_y-Food_y)<30:
                Food_x = random.randint(2,19)*30
                Food_y = random.randint(2, 19) * 30
                Score+=5
                Snake_length+=5
            Snake_head_x+= Speed_x
            Snake_head_y+=Speed_y
            Snake_Window.fill(Blue)
            write_score('Score: '+str(Score),Red,10,10)
            body = []
            body.append(Snake_head_x)
            body.append(Snake_head_y)
            Snake_list.append(body)
            if Snake_head_x<0 or Snake_head_x>600 or Snake_head_y<50 or Snake_head_y>600:
                game_over = True
            if Snake_length<len(Snake_list):
                del Snake_list[0]
            if body in Snake_list[:-1] :
                game_over = True
            create_body(Snake_Window,Red,Snake_list,Snake_Size)
            pygame.draw.rect(Snake_Window, hybrid, [0, 0, 600, 50])
            pygame.draw.rect(Snake_Window, Green, [Food_x, Food_y, Snake_Size, Snake_Size])
            pygame.draw.rect(Snake_Window,Red,[Snake_head_x,Snake_head_y,Snake_Size,Snake_Size])
            pygame.display.update()
            cv2.imshow("Snake_game",image)
            cv2.waitKey(1)
            Clock.tick(fps)
Game_loop()
