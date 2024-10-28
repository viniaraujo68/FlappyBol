#Vinicius Araujo 2210392// Francisco Fleury 2210641

#IMPORTS

import random
import pygame
from pygame import *
from pygame.time import *
from pygame.font import *
from pygame.locals import *

#VARIAVEIS

#TELA
width, height = 1350, 756

#PASSARO
character = None
x_bird, y_bird = 150,378
r_bird = 35
gravidade = 0.0008
velocidade = 0
score = 0


#CANOS
pipes = []
spacing = 250
canAddPipe = 0
min_pipe = 70
max_pipe = 490
vel_pipe = 0.3
top_col = []
bot_col = []
ref = [(2,2),(10,3),(2,3)]
character_ref = 0

def restart():
    global pipes, top_col, bot_col, velocidade, y_bird, alive, gravidade, score
    alive = True
    pipes = []
    velocidade = 0
    top_col = []
    bot_col = []
    y_bird = 378
    gravidade = 0
    score = 0


def addPipe():
    tamanho = random.randint(min_pipe,max_pipe)
    pipes.append({'tamanho':tamanho, 'x_pos':1430, "scored":False})

def load():
    global bg, clock, bol, pipe_img, menu_img, over_img, rafa, fleu, bol1, baffa, title, nome_bol, nome_fleu, nome_rafa, nome_over, fleu1, rafa1, font, font2, death_sound
    font = pygame.font.SysFont('impact',24)
    font2 = pygame.font.SysFont('impact',50)
    menu_img = pygame.image.load("menu.png")
    menu_img = transform.scale(menu_img,(1350, 756))
    over_img = pygame.image.load("game_over.png")
    over_img = transform.scale(over_img,(1350, 756))
    pipe_img = pygame.image.load("pipe.png")
    pipe_img = transform.scale(pipe_img,(596,610))
    rafa = pygame.image.load("rafap.png")
    fleu = pygame.image.load("fleury.png")
    fleu1 = transform.flip(transform.scale(fleu,(r_bird*ref[1][0],r_bird*ref[1][1])),True,False)
    rafa1 = transform.scale(rafa,(r_bird*ref[2][0],r_bird*ref[2][1]))
    bol1 = pygame.image.load("bol.png")
    bol = transform.scale(bol1,(r_bird*ref[0][0],r_bird*ref[0][1]))
    baffa = pygame.image.load("boss.png")
    title =  pygame.image.load("titulo.png")
    nome_bol =  pygame.image.load("bolnome.png")
    nome_fleu =  pygame.image.load("fleurynome.png")
    nome_rafa = pygame.image.load("rafanome.png")
    nome_over = pygame.image.load("overnome.png")
    bg = pygame.image.load("fundo.png")
    bg = transform.scale(bg,(1350,756))
    pygame.mixer.music.load('tema_menu.mp3')
    death_sound = pygame.mixer.Sound("eren.mp3")
    clock = Clock()

def change_music():
    global menu, alive
    pygame.mixer.music.stop()
    pygame.mixer.music.set_volume(0.05)
    if menu:
        pygame.mixer.music.load('tema_menu.mp3')
    elif alive:
        pygame.mixer.music.load('naruto_fight.mp3')
    else:
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load('lacrimosa.mp3')

    pygame.mixer.music.play(-1)
        

def draw_menu(screen):
    screen.blit(menu_img,(0,0))
    screen.blit(transform.scale(fleu,(500,281)),(565,150))
    screen.blit(transform.flip(transform.scale(rafa,(168,300)),True,False),(200,180))
    screen.blit(transform.flip(transform.scale(bol1,(190,250)),True,False),(990,175))
    screen.blit(transform.scale(baffa,(380,381)),(-50,450))
    screen.blit(transform.scale(nome_fleu,(210,35)), (620,410))
    screen.blit(nome_bol, (990,410))
    screen.blit(nome_rafa,(350,260))
    screen.blit(title,(350,50))
    select = font.render('CLIQUE NO SEU PERSONAGEM',True,(255,165,0))
    screen.blit(select,(420,200))
    #draw.rect(screen,(200,0,200), pygame.Rect(525,480,300,80))

def draw_screen(screen):
    global x_bird,y_bird,r_bird, bird, pipes,pipe_img, brd,top_col, bot_col, character, character_ref, ref, font, score, over_img, nome_over, font2,velocidade, start
    if alive:
        screen.blit(bg, (0,0))
        brd = pygame.Rect(x_bird-r_bird+8,y_bird-r_bird+8,2*r_bird-18,2*r_bird-18)
        #draw.rect(screen,(0,0,0), brd)
        score_img = font.render("SCORE: "+str(score),True,(0,255,0))
        if character_ref == 2:
            bird = screen.blit(transform.rotate(character,35*velocidade),(x_bird-(ref[character_ref][0]*r_bird)/2,y_bird-((ref[character_ref][1]*1.4)*r_bird)/2))
        else:
            bird = screen.blit(transform.rotate(character,35*velocidade),(x_bird-(ref[character_ref][0]*r_bird)/2,y_bird-((ref[character_ref][1])*r_bird)/2))
        top_col = []
        bot_col = []
        for pipe in pipes:
            t = pygame.Rect(pipe["x_pos"]+235,0,130,pipe["tamanho"])
            draw.rect(screen,(0,190,0),t)
            b = pygame.Rect(pipe["x_pos"]+235,pipe["tamanho"]+spacing,130,756-(spacing+pipe["tamanho"]))
            draw.rect(screen,(0,190,0),b)
            top_col.append(t)
            bot_col.append(b)
            screen.blit(pygame.transform.rotate(pipe_img,180),(pipe["x_pos"],pipe["tamanho"]-610))
            screen.blit(pipe_img, (pipe["x_pos"],pipe["tamanho"]+spacing))
        screen.blit(score_img,(20,20))
        if not start:
            press = font.render('PRESS SPACE TO PLAY',True,(0,0,0))
            screen.blit(press,(570,350))
    else:
        screen.blit(over_img,(0,0))
        screen.blit(nome_over,(400,126))
        score_final = font2.render("SCORE: "+str(score),True,(252,15,192))
        info_final = font.render("PRESS 'F' TO QUIT"+ '\n'+"PRESS 'M' TO GO TO THE MENU"+'\n'+"PRESS SPACE TO RESTART",True,(252,15,192))
        screen.blit(score_final,(574,506))
        screen.blit(info_final,(350,700))

def update(dt):
    global y_bird, velocidade, gravidade,canAddPipe, alive, start, running, menu, character, bol, fleu1, rafa1, ref, character_ref, score, death_sound
    if not menu:
        if alive:
            if start:
                velocidade = velocidade -(gravidade*dt)
                y_bird -=  dt * velocidade
                if brd.collidelist(top_col+bot_col) != -1 or y_bird>756 or y_bird<0:
                    alive = False
                    start = False
                    death_sound.set_volume(0.07)
                    pygame.mixer.Sound.play(death_sound)
                    change_music()
                if canAddPipe >200:
                    addPipe()
                    canAddPipe = 0
                canAddPipe += dt * 0.09
                for i in range(len(pipes)):
                    if i < len(pipes):
                        pipe = pipes[i]
                        if pipe["x_pos"] < -350:
                            pipes.pop(i)
                        elif pipe["x_pos"] <= -75 and not pipe["scored"]:
                            score +=1
                            pipe["scored"] = True
                        pipe['x_pos'] = pipe["x_pos"] - (vel_pipe*dt)
            else:
                for e in event.get():
                    if e.type == QUIT:
                        running = False
                        break
                    elif e.type == KEYDOWN:
                        if e.unicode == ' ':
                            start = True
                            gravidade = 0.0008
                            velocidade = 0.5
        else:
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    break
                if e.type == KEYDOWN:
                    if e.unicode == 'f':
                        running = False
                        break
                    elif e.unicode == ' ':
                        restart()
                        change_music()
                    elif e.unicode == 'm':
                        restart()
                        menu = True
                        change_music()
    else:
        for e in event.get():
            if e.type == QUIT:
                running = False
                break
            if e.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0]>=1000 and mouse[0]<=1200 and mouse[1]>=170 and mouse[1]<=420:
                    character = bol
                    character_ref = 0
                    menu = False
                    change_music()
                elif mouse[0]>=710 and mouse[0]<=888 and mouse[1]>=160 and mouse[1]<=380:
                    character = fleu1
                    character_ref = 1
                    menu = False
                    change_music()

                elif mouse[0]>=200 and mouse[0]<=360 and mouse[1]>=261 and mouse[1]<=490:
                    character = rafa1
                    character_ref = 2
                    menu = False
                    change_music()
                
def main_loop():
    global clock, screen, velocidade, alive, start, gravidade, menu, running
    menu = True
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    running = True
    screen.blit(bg, (0,0))
    alive = True
    start = False
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
                break
            elif e.type == KEYDOWN:
                if e.unicode == ' ':
                    velocidade = 0.5
        clock.tick(60)
        dt = clock.get_time()
        if menu:
            draw_menu(screen)
        else:
            draw_screen(screen)
        update(dt)
        display.update()
                
                        
    pygame.quit()

pygame.init()
screen = pygame.display.set_mode((width,height))
display.set_caption("Vini and Fleury's Bird")
load()
main_loop()