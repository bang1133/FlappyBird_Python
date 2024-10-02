import pygame,random 
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((432,650))
#Tiêu 
name = pygame.display.set_caption("Flappy Bird")
#load icon 
icon = pygame.image.load('./FileGame/assets/yellowbird-downflap.png')
#set logo
pygame.display.set_icon(icon)
#load background
bg = pygame.image.load('./FileGame/assets/background-night.png')
bg = pygame.transform.scale2x(bg)
'''Full Floor'''
#floor
floor = pygame.image.load('./FileGame/assets/floor.png')
floor = pygame.transform.scale2x(floor)
x_pos = 0
#load sàn
def load_floor() : 
    screen.blit(floor,(x_pos,550)) 
    #tạo thêm một sàn cho chuyển động liên tục
    screen.blit(floor,(x_pos+433,600))
# chạy hết 432 thì nó set lại vị trí 0
if x_pos == -432 : 
    x_pos = 0
#cho sàn chạy 
x_pos -= 1
'''Full Bird'''
#load bird 
bird_down = pygame.image.load('./FileGame/assets/yellowbird-downflap.png')
bird_mid = pygame.image.load('./FileGame/assets/yellowbird-midflap.png')
bird_up = pygame.image.load('./FileGame/assets/yellowbird-upflap.png')
list_bird = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = list_bird[bird_index]
bird_rect = bird.get_rect(center = (30,320))
#tạo timer cho bird
chim_bay = pygame.USEREVENT+1 # +1 để phân biệt event của chim 
pygame.time.set_timer(chim_bay,200) #add full event vào while
def chimdapcanh() : 
    newbird = list_bird[bird_index]
    newbird_rect = newbird.get_rect(center = (30,bird_rect.centery))
    return newbird,newbird_rect
#tạo trọng lực cho chim rớt
trong_luc = 0.1 #lực húttttt trái đất !
bird_y = 0 
#xoay chim 
def active_bird(chim) : 
    new_bird = pygame.transform.rotozoom(chim,-bird_y*4,1)
    return new_bird

'''Full Score'''
#add score 
score_game = 0 #điểm start
highScore = 0 #điểm cao nhất 
fontgame = pygame.font.Font('./FileGame/04B_19.TTF',40) #40 size
#high Score
def updateScore(score_game,highScore) : 
    if score_game > highScore : 
        highScore = score_game 
    return highScore    
#tạo một hàm  
def score(playgame) :
    if playgame :
        score_font = fontgame.render((f'Score :{int(score_game)}'),True,(255,0,0))
        score_rect = score_font.get_rect(center = (220,100)) 
        screen.blit(score_font,score_rect)  
    if playgame == False : 
        score_font = fontgame.render(f'Score: {int(score_game)}',True,(255,255,0)) 
        score_rect = score_font.get_rect(center = (220,100)) 
        screen.blit(score_font,score_rect)

        hScore = fontgame.render(f'High Score: {int(highScore)}',True,(255,0,0)) 
        highScore_rect = hScore.get_rect(center = (215,155)) 
        screen.blit(hScore,highScore_rect) 
 
        '''      Full Pipes   '''
#tạo ống 
ong_list = []
ongnuoc = pygame.image.load("./FileGame/assets/pipe-green.png")
ongnuoc = pygame.transform.scale2x(ongnuoc)
#lenght_pipes
len_pipes = [150,200,250]
#timer 
xuathienongnuoc = pygame.USEREVENT
pygame.time.set_timer(xuathienongnuoc,1200) #1.2s
#hàm vẽ hình chữ cho ống nước 
def create_ong() :
    random_pipes = random.choice(len_pipes)
    bot_pipe = ongnuoc.get_rect(midtop = (500,random_pipes))
    top_pipe = ongnuoc.get_rect(midtop = (500,random_pipes-600))
    return bot_pipe,top_pipe
#hàm ống chạy
def move_pipe(pipes) : 
    for pipe in pipes : 
        pipe.centerx -=5
    return pipes 
#hàm vẽ ống
def draw_pipes(pipes) :
    for pipe in pipes: 
        if pipe.bottom >= 600 :
            screen.blit(ongnuoc,pipe)
        else :
            xoay_ong = pygame.transform.flip(ongnuoc,False,True) #false : x, True : y
            screen.blit(xoay_ong,pipe)
#chèn âm thanh 
sound_win = pygame.mixer.Sound('./FileGame/sound/sfx_wing.wav')
sound_hit = pygame.mixer.Sound('./FileGame/sound/sfx_hit.wav')
'''Full Checkgame'''
#kiểm tra va chạm top and bottom
playgame = True
#xử lí va chạm
def check_game(pipes) :
    for pipe in pipes : 
        if bird_rect.colliderect(pipe): 
            sound_hit.play()
            return False 

        if bird_rect.bottom >= 600 or bird_rect.top <= -50:
            return False    
    return True
#screen outgame
outgame = pygame.image.load('./FileGame/assets/message.png')
outgame = pygame.transform.scale2x(outgame)
rect_outgame = outgame.get_rect(center = (210,400))

'''biến chạy cho chương trình'''
running = True
#set độ fps
fps = pygame.time.Clock()
while running : 
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT : 
            running = False
        #tương tác với space
        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_SPACE : 
                bird_y = -5
                sound_win.play()
            if event.key == pygame.K_SPACE and playgame== False :
                playgame = True
                bird_y = 0 
                ong_list.clear()
                bird_rect.center = (30,320)
                score_game = 0
                 
        #xuất hiện ống nước
        if event.type == xuathienongnuoc: 
            ong_list.extend(create_ong())
        if event.type == chim_bay : 
            if bird_index < 2 : 
                bird_index += 1
            else : 
                bird_index = 0
            bird,bird_rect = chimdapcanh()  #hàm chim đập cánh
    #load nền vào cửa sổ
    screen.blit(bg,(0,0))
    #check
    if playgame : 
        #xoay chim 
        active_chim = active_bird(bird)
        #load chim 
        screen.blit(active_chim,(bird_rect))
        #tăng trọng lực 
        bird_y += trong_luc
        #toạ độ hình chữ nhật = toạ độ của bird_y
        bird_rect.centery += bird_y
        #load điểm
        '''thời gian chạy thì score + 1'''
        score_game+=0.01
        score(True)
        playgame = check_game(ong_list)
        #Ống 
        ong_list = move_pipe(ong_list)
        draw_pipes(ong_list)
        load_floor()
    else : 
        screen.blit(outgame,(rect_outgame))
        highScore = updateScore(score_game,highScore)
        score(False)
         
    pygame.display.flip()      
    fps.tick(150)  