import pygame
import sys
import math
from tools import Tools

pygame.init()

# экран
W, H = 900, 650
TOOLBAR = 80
CANVAS_H = H - TOOLBAR

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY  = (200,200,200)

font = pygame.font.SysFont("arial", 18)

PALETTE = [
    (0,0,0),(255,0,0),(0,255,0),(0,0,255),
    (255,255,0),(255,128,0),(128,0,255)
]

# ───────── TOOLS ─────────
PENCIL="pencil"
LINE="line"
RECT="rect"
CIRCLE="circle"
SQUARE="square"
RTRI="rtri"
ETRI="etri"
RHOMBUS="rhombus"
ERASER="eraser"
FILL="fill"
TEXT="text"

tools = Tools()

# холст
canvas = pygame.Surface((W, CANVAS_H))
canvas.fill(WHITE)

tool = PENCIL
color = BLACK

brush = 2
brush_map = {1:2,2:5,3:10}

drawing = False
start = None
prev = None
snapshot = None
line_start = None

# TEXT
text_mode = False
text_pos = None
text_buffer = ""

# фигуры
def draw_shape(surf,p1,p2):
    x1,y1=p1
    x2,y2=p2
    b=brush_map[brush]

    if tool==RECT:
        pygame.draw.rect(surf,color,pygame.Rect(min(x1,x2),min(y1,y2),
            abs(x2-x1),abs(y2-y1)),b)

    elif tool==CIRCLE:
        r=int(math.hypot(x2-x1,y2-y1)/2)
        pygame.draw.circle(surf,color,((x1+x2)//2,(y1+y2)//2),r,b)

    elif tool==SQUARE:
        s=max(abs(x2-x1),abs(y2-y1))
        pygame.draw.rect(surf,color,pygame.Rect(x1,y1,s,s),b)

    elif tool==RTRI:
        pygame.draw.polygon(surf,color,[(x1,y1),(x1,y2),(x2,y2)],b)

    elif tool==ETRI:
        pygame.draw.polygon(surf,color,[(x1,y2),(x2,y2),((x1+x2)//2,y1)],b)

    elif tool==RHOMBUS:
        cx=(x1+x2)//2
        cy=(y1+y2)//2
        pygame.draw.polygon(surf,color,[(cx,y1),(x2,cy),(cx,y2),(x1,cy)],b)

# loop
while True:
    clock.tick(60)

    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # толщина кисти по цифрам, через клавиатуру ввод
        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_1: brush=1
            if e.key == pygame.K_2: brush=2
            if e.key == pygame.K_3: brush=3

            if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                tools.save(canvas)

            # текст 
            if text_mode:
                if e.key == pygame.K_RETURN:
                    if text_buffer.strip():
                        canvas.blit(font.render(text_buffer,True,color),text_pos)
                    text_mode=False
                    text_buffer=""

                elif e.key == pygame.K_ESCAPE:
                    text_mode=False
                    text_buffer=""

                elif e.key == pygame.K_BACKSPACE:
                    text_buffer=text_buffer[:-1]

                else:
                    if len(e.unicode)==1 and e.unicode.isprintable():
                        text_buffer+=e.unicode

        # срабатывание при нажатии мыши
        if e.type == pygame.MOUSEBUTTONDOWN:
            x,y=e.pos

            # palette
            for i,c in enumerate(PALETTE):
                if 10+i*35<x<40+i*35 and 10<y<40:
                    color=c

            # tools
            names=[PENCIL,LINE,FILL,TEXT,ERASER,
                   RECT,CIRCLE,SQUARE,RTRI,ETRI,RHOMBUS]

            for i,t in enumerate(names):
                if 10+i*70<x<80+i*70 and 50<y<75:
                    tool=t

            # clear button
            if W-120 < x < W-20 and 20 < y < 60:
                canvas.fill(WHITE)
                text_mode=False
                text_buffer=""
                drawing=False

            cx,cy=x,y-TOOLBAR

            if tool==TEXT:
                text_mode=True
                text_pos=(cx,cy)
                text_buffer=""
                continue

            drawing=True
            start=(cx,cy)
            prev=(cx,cy)
            snapshot=canvas.copy()

            if tool=="line":
                line_start=(cx,cy)

            if tool==PENCIL:
                pygame.draw.circle(canvas,color,(cx,cy),brush_map[brush])

            if tool==ERASER:
                pygame.draw.circle(canvas,WHITE,(cx,cy),brush_map[brush])

            if tool==FILL:
                target=canvas.get_at((cx,cy))
                tools.flood_fill(canvas,(cx,cy),target,color,W,CANVAS_H)

        # ───────── DRAW ─────────
        if e.type==pygame.MOUSEMOTION and drawing:

            x,y=e.pos
            cx,cy=x,y-TOOLBAR

            if tool==PENCIL:
                pygame.draw.line(canvas,color,prev,(cx,cy),brush_map[brush])
                prev=(cx,cy)

            elif tool==ERASER:
                pygame.draw.circle(canvas,WHITE,(cx,cy),brush_map[brush])

            elif tool=="line":
                canvas.blit(snapshot,(0,0))
                pygame.draw.line(canvas,color,line_start,(cx,cy),brush_map[brush])

            elif tool in [RECT,CIRCLE,SQUARE,RTRI,ETRI,RHOMBUS]:
                canvas.blit(snapshot,(0,0))
                draw_shape(canvas,start,(cx,cy))

        if e.type==pygame.MOUSEBUTTONUP:
            drawing=False

            if tool=="line":
                x,y=e.pos
                cx,cy=x,y-TOOLBAR
                pygame.draw.line(canvas,color,line_start,(cx,cy),brush_map[brush])

    
    screen.fill(WHITE)

    screen.blit(canvas,(0,TOOLBAR))

    pygame.draw.rect(screen,GRAY,(0,0,W,TOOLBAR))

    # palette
    for i,c in enumerate(PALETTE):
        pygame.draw.rect(screen,c,(10+i*35,10,30,25))

    # tools
    labels=["Pen","Line","Fill","Text","Erase",
            "Rect","Circle","Square","Rtri","Etri","Rhomb"]

    for i,l in enumerate(labels):
        pygame.draw.rect(screen,(180,180,180),(10+i*70,50,65,25))
        screen.blit(font.render(l,True,BLACK),(12+i*70,55))

    # brush info
    screen.blit(font.render(f"Brush {brush}",True,BLACK),(650,10))

    # clear button
    pygame.draw.rect(screen, (220, 70, 70), (W-120, 20, 100, 40))
    screen.blit(font.render("CLEAR", True, WHITE), (W-95, 30))

    # text preview
    if text_mode:
        screen.blit(font.render(text_buffer+"|",True,color),text_pos)

    pygame.display.flip()