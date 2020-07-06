"""
{} markuse tarkvara

Tänavasõit
Selles mängus peate juhtima autot ja vältima kokkupõrget
konkurentidega.

Skoor: arvestatakse vastavalt sõidukaugusele
Konkurentide arv: valitakse vastavalt raskusastmele (2 * raskusaste)
Konkurentide kiirus: genereeritakse vastavalt raskusastmele
"""
#kogude ja klasside importimine
import pygame
import sys
from random import *
from Rectangle import *
from KbdControl import *
from TextClass import *

pygame.init()
pygame.mixer.init()
allowhighfps = True
finalfps = 90
if allowhighfps == False: finalfps = 60
res = [800, 600]
backcolor = [randint(0, 255), randint(0, 255), randint(0, 255)]
screen = pygame.display.set_mode(res)
screen.fill([0, 0, 0])
leveltext = TextClass("Arial", 25, [12, res[1] - 40], "Mängu käivitamine...", [255, 255, 255])
leveltext.BlitText(screen)
pygame.display.flip()
bgms = ["emelie.xm", "envisions.s3m", "hotdogs3.xm", "backfromblue.mod", "madness.mod", "carvup-2.mod"]
pygame.mixer.music.load("bgm/" + bgms[randint(0, len(bgms) - 1)])
pygame.mixer.music.play(-1)

engine = pygame.mixer.Sound("snd/fastest_speed.wav")

clock = pygame.time.Clock()
#Kui lubatud, eemaldab kokkupõrkamise funktsiooni
invincible = False

#ekraani initsialiseerimine
#minimaalne resolutsioon: 219, 1
#maksimaalne resolutsioon: 16383, 686 konkurentideta 16383, 881 tehniliselt 16383, 16383
screen.fill([0, 122, 255])
#night - öö või mitte
#öösel on pime ja peamiseks nägemisvahendiks on esivalgustus
#fog - udune või mitte
#kui on udune, siis on kaugusesse raske näha
#sublevels - alatasemete arv ehk mitu sõidukit võib maksimaalselt olla ekraanil
night = False
fog = False
damage = 0
sublevels = 3
headlight_x = -384
#Raskusastme valimine
#0 - liiklust pole
#1 - väga kerge
#2 - kerge
#3 - keskmine
#4 - raske
#5 - väga raske
#6+ - liiga raske, võimalik, et mäng saab alguses kohe läbi
difficulty = 0
speed = 0
score = 0

#RoadTiles - tee keskel olevad tähised
RoadTiles = []

#player_skin - mängija sõiduk
#tekstuurifailid, mis lõpevad f-ga on suunatud üles, need mis lõpevad b-ga on suunatud alla
headlight = Character(0, headlight_x, [0, 0, 0], 1, 1, [False, False, False, False], pygame.image.load("img/headlight.png"))
player_skin = pygame.image.load("img/oblue_f.png")
player = Character(int(res[0] / 2) + int(res[1] / 150), int(res[1] / 2), [randint(0, 255), randint(0, 255), randint(0, 255)], 40, 84)
player.car = True

#genereerib konkurendid, vastusõitjad, kaasliiklejad vms
Obstacles = []
signs = []
fsigns = []
forward_characters = ["oblue_f", "ogreen_f", "oorange_f", "ored_f"]
backward_characters = ["oblue_b", "ogreen_b", "oorange_b", "ored_b"]
dead = False
signs.append(Character(40, 289, [254, 254, 254], 720, 10, [False, False, True, False]))
fsigns.append(Character(40, 0, [100, 100, 100], 15, 300, [False, False, True, False]))
fsigns.append(Character(745, 0, [100, 100, 100], 15, 300, [False, False, True, False]))
fsigns.append(Character(40, 0, [90, 200, 90], 720, 100, [False, False, True, False]))
black = False
finstart = (difficulty * -1000) - (difficulty * 1000)
for x in range(30, 760, 20):
    if black == False:
        signs.append(Character(x, finstart, [255, 255, 255], 20, 20, [False, False, True, False]))
        black = True
        continue
    else:
        signs.append(Character(x, finstart, [0, 0, 255], 20, 20, [False, False, True, False]))
        black = False
        continue
#listide loomine
rightside = [int(res[0]/2) + 10, int(res[0]/2) + 30, int(res[0]/2) + 50, int(res[0]/2) + 70, int(res[0]/2) + 90]
for i in range(0, difficulty * 80, 80):
    Obstacles.append(Character(randint(100, 360), i, [255, 0, 0], 40, 84, [False, False, True, False], pygame.image.load("img/" + backward_characters[randint(0, 3)] + ".png")))
for i in range(0, difficulty * 80, 80):
    Obstacles.append(Character(rightside[randint(0, len(rightside) - 1)], i, [255, 0, 0], 40, 84, [True, False, False, False], pygame.image.load("img/" + forward_characters[randint(0, 3)] + ".png")))
for obstacle in Obstacles:
    obstacle.speed = speed + randint(0, 5)
for i in range(0, 960, 120):
    RoadTiles.append(Character(int(res[0] / 2) - 10, i, [255, 255, 255], 10, 80, [False, False, True, False]))


#põhiprogramm
while True:
    #teeääriste list
    sides = [Character(0, 0, backcolor, 30, res[1], [False, False, True, False]), Character(50, 0, [255, 255, 255], 20, res[1], [False, False, True, False]), Character(res[0] - 70, 0, [255, 255, 255], 20, res[1], [False, False, True, False]), Character(res[0] - 30, 0, backcolor, 30, res[1], [False, False, True, False])]
    #sisendi kontrollimine
    speed = KeyControl(pygame, player, player.speed, dead)
    #vastutab tee liikumise eest
    player.speed = speed
    for tile in RoadTiles:
        tile.speed = speed
    #täidab ekraani
    screen.fill([128, 128, 128])
    #kuvab keskmised teetähised
    for tile in RoadTiles:
        if tile.GetPosition()[1] > 800 + tile.size_y:
            tile.GoToPosition(tile.GetPosition()[0], -tile.size_y + (-880 + tile.GetPosition()[1]))
        elif tile.GetPosition()[1] < 0 - tile.size_y:
            tile.GoToPosition(tile.GetPosition()[0], 800 + tile.size_y)
        tile.UpdatePosition()
        tile.DrawCharacter(screen)
    #kuvab teeäärised
    for side in sides:
        side.DrawCharacter(screen)
    #seadistab kaasliiklejate kiirused
    for obstacle in Obstacles:
        for secstacle in Obstacles:
            if pygame.Rect.colliderect(pygame.Rect(obstacle.GetRect()[0], obstacle.GetRect()[1], obstacle.size_x, obstacle.size_y), pygame.Rect(secstacle.GetRect()[0], secstacle.GetRect()[1], secstacle.size_x, secstacle.size_y)):
                if not obstacle == secstacle:
                    obstacle.location_y = -obstacle.size_y
                    secstacle.location_y = -secstacle.size_y
                    if obstacle.location_x >= res[0] / 2:
                        obstacle.location_x = rightside[randint(0, len(rightside) - 1)]
                        obstacle.location_y = randint(-200, -obstacle.size_y)
                    else:
                        obstacle.location_x = randint(100, 360)
                        obstacle.location_y = randint(-200, -obstacle.size_y)
                    if secstacle.location_x >= res[0] / 2:
                        secstacle.location_x = rightside[randint(0, len(rightside) - 1)]
                        secstacle.location_y = randint(-200, -secstacle.size_y)
                    else:
                        secstacle.location_x = randint(100, 360)
                        secstacle.location_y = randint(-200, -secstacle.size_y)
        if obstacle.keys[2] == True:
            obstacle.speed = speed + difficulty
        elif obstacle.keys[0] == True:
            obstacle.speed = -speed + (difficulty * 2)
    #märkide uuendamine
    finstart = (difficulty * -1000) - (difficulty * 1000)
    for sign in signs:
        if pygame.Rect.colliderect(pygame.Rect(player.GetRect()[0], player.GetRect()[1], player.size_x, player.size_y), pygame.Rect(sign.GetRect()[0], sign.GetRect()[1], sign.size_x, sign.size_y)):
            if sign.GetColor() == [0, 0, 0]:
                difficulty = 0
                Obstacles.clear()
                player.dead = True
                dead = True
            if sign.GetColor() == [0, 0, 255]:
                difficulty = int(len(Obstacles) / 2)
                black = False
                black = [0, 0, 255]
                if difficulty == sublevels - 1:
                    black = [0, 0, 0]
                for i in range(len(signs)):
                    if signs[i].GetColor() == [254, 254, 254] or signs[i].GetColor() == [100, 100, 100]:
                        continue
                    signs[i].location_y = 0 + finstart
                    if difficulty == sublevels - 1:
                        if signs[i].color == [0, 0, 255]:
                            signs[i].color = black
                
                Obstacles.append(Character(rightside[randint(0, len(rightside) - 1)], i, [255, 0, 0], 40, 84, [True, False, False, False], pygame.image.load("img/" + forward_characters[randint(0, 3)] + ".png")))
                Obstacles.append(Character(randint(100, 360), -80, [255, 0, 0], 40, 84, [False, False, True, False], pygame.image.load("img/" + backward_characters[randint(0, 3)] + ".png")))
                difficulty = int(len(Obstacles) / 2)
                for obstacle in Obstacles:
                    obstacle.speed = speed + randint(0, 5)
        if sign.GetColor() == [255, 255, 255] or sign.GetColor() == [0, 0, 255] or sign.GetColor() == [0, 0, 0]:
            if sign.GetPosition()[1] > res[1] + 150:
                difficulty = int(len(Obstacles) / 2)
                black = False
                black = [0, 0, 255]
                if difficulty == sublevels - 1:
                    black = [0, 0, 0]
                for i in range(len(signs)):
                    if signs[i].GetColor() == [254, 254, 254] or signs[i].GetColor() == [100, 100, 100]:
                        continue
                    signs[i].location_y = 0 + finstart
                    if difficulty == sublevels - 1:
                        if signs[i].color == [0, 0, 255]:
                            signs[i].color = black
                Obstacles.append(Character(randint(100, 360), -80, [255, 0, 0], 40, 84, [False, False, True, False], pygame.image.load("img/" + backward_characters[randint(0, 3)] + ".png")))
                Obstacles.append(Character(rightside[randint(0, len(rightside) - 1)], i, [255, 0, 0], 40, 84, [True, False, False, False], pygame.image.load("img/" + forward_characters[randint(0, 3)] + ".png")))
                difficulty = int(len(Obstacles) / 2)
                for obstacle in Obstacles:
                    obstacle.speed = speed + randint(0, 5)
                if difficulty == sublevels + 1: difficulty = 0
                if difficulty == 0:
                    Obstacles.clear()
                    if not invincible: player.dead = True
                    if not invincible: dead = True
        sign.speed = player.speed
        sign.UpdatePosition()
        sign.DrawCharacter(screen)
    #see osa koodi tegeleb kaasliiklejate olukorra kontrollimisega ja kokkupõrke kontrollimisega
    #samuti kuvatakse siin kaasliiklejad ekraanile
    for obstacle in Obstacles:
        if pygame.Rect.colliderect(pygame.Rect(player.GetRect()[0], player.GetRect()[1], player.size_x, player.size_y) , pygame.Rect(obstacle.GetRect()[0], obstacle.GetRect()[1], obstacle.size_x, obstacle.size_y)):
            if obstacle.location_y < player.location_y:
                obstacle.speed += player.speed * 0.9
                player.speed = 0.1 * player.speed
            else:
                player.speed = player.speed + obstacle.speed + difficulty
                obstacle.speed = 0.1 * obstacle.speed
            if not invincible: damage += 0.01 * difficulty
            #if not invincible: dead = True
            if player.keys[1] == True:
                player.keys[1] = False
                obstacle.location_x -= player.traction
            elif player.keys[3] == True:
                player.keys[3] = False
                obstacle.location_x += player.traction
            #for i in range(len(player.keys)):
            #    player.keys[i] = False
        if obstacle.GetPosition()[1] > 800 + obstacle.size_y:
            if obstacle.keys[2] == True:
                obstacle.GoToPosition(randint(100, 360), -obstacle.size_y + (-884 + obstacle.GetPosition()[1]))
                obstacle.speed = speed + randint(0, int(difficulty / 10 * 10))
                obstacle.character = pygame.image.load("img/" + backward_characters[randint(0, 3)] + ".png")
        if obstacle.keys[0] == True:
            if obstacle.GetPosition()[1] > 800 + obstacle.size_y:
                obstacle.GoToPosition(randint(410, 700), -obstacle.size_y)
                obstacle.character = pygame.image.load("img/" + forward_characters[randint(0, 3)] + ".png")
        if obstacle.GetPosition()[1] < 0 - obstacle.size_y:
            if obstacle.keys[0] == True:
                obstacle.GoToPosition(randint(410, 700), 600 + obstacle.size_y)
                obstacle.character = pygame.image.load("img/" + forward_characters[randint(0, 3)] + ".png")
            obstacle.speed = -speed + randint(0, int(difficulty / 10 * 10))
        obstacle.UpdatePosition()
        screen.blit(obstacle.character, obstacle.GetPosition())
        #obstacle.DrawCharacter(screen)
    #muudab mängija positsiooni vastavalt all hoitavatele klahvidele (keys)
    player.UpdatePosition()

    #player.DrawCharacter(screen)
    if player.keys[1] == True:
        if player.location_x <= 0:
            player.location_x += player.traction
        else:
            headlight_x -= player.traction
    if player.keys[3] == True:
        if player.location_x >= 800 - player.size_x:
            player.location_x -= player.traction
        else:
            headlight_x += player.traction
    if fog: screen.blit(pygame.image.load("img/fog.png"), [0, 0])
    screen.blit(player_skin, player.GetPosition())
    for sign in fsigns:
        sign.speed = player.speed
        sign.UpdatePosition()
        sign.DrawCharacter(screen)
    if night: screen.blit(headlight.character, [headlight_x, 0])
    #mäng läbi ekraan
    if dead:
        if dead:
            if difficulty > 0:
                screen.fill([0, 0, 0])
                leveltext = TextClass("Arial", 25, [12, res[1] - 40], "Kaotasite! | FPS: [15]", [0, 0, 0])
                leveltext.BlitText(screen)
                leveltext.textlocation = [leveltext.textlocation[0] - 2, leveltext.textlocation[1] - 2]
                leveltext.textcolor = [255, 255, 255]
                leveltext.BlitText(screen)
                for i in range(200):
                    speed = KeyControl(pygame, player, player.speed, dead)
                    gameover = TextClass("Arial", 52, [randint(0, res[0] - 150), randint(-50, res[1] + 50)], "Kaotasite", [0, 0, 0])
                    gameover.BlitText(screen)
                    gameover.textlocation = [gameover.textlocation[0] - 2, gameover.textlocation[1] - 2]
                    gameover.textcolor = [randint(0, 255), randint(0, 50), randint(0, 128)]
                    gameover.BlitText(screen)
                    scoretext = TextClass("Arial", 25, [int(res[0] / 2) - 30, int(res[1] / 2) + 20], "Skoor: " + str(score), [0, 0, 0])
                    scoretext.BlitText(screen)
                    scoretext.textlocation = [scoretext.textlocation[0] - 2, scoretext.textlocation[1] - 2]
                    scoretext.textcolor = [255, 255, 255]
                    scoretext.BlitText(screen)
                    pygame.display.flip()
                    clock.tick(15)
                pygame.quit()
                sys.exit()
            else:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("bgm/" + bgms[randint(0, len(bgms) - 1)])
                pygame.mixer.music.play(-1)
                night = randint(0, 1)
                if night == False:
                    fog = randint(0, 1)
                else:
                    fog = False
                for i in range(20):
                    screen.fill([0, 0, 0])
                    leveltext = TextClass("Arial", 25, [12, res[1] - 40], "Järgmise taseme laadimine...", [255, 255, 255])
                    leveltext.BlitText(screen)
                    pygame.display.flip()
                    clock.tick(60)
                backcolor = [randint(0, 255), randint(0, 255), randint(0, 255)]
                dead = False
                player.dead = False
                signs.clear()
                sublevels += 1
                signs.append(Character(40, 289, [254, 254, 254], 720, 10, [False, False, True, False]))
                fsigns.append(Character(40, 0, [100, 100, 100], 15, 300, [False, False, True, False]))
                fsigns.append(Character(745, 0, [100, 100, 100], 15, 300, [False, False, True, False]))
                fsigns.append(Character(40, 0, [90, 200, 90], 720, 100, [False, False, True, False]))
                black = False
                finstart = (difficulty * -1000) - (difficulty * 1000)
                for x in range(30, 760, 20):
                    if black == False:
                        signs.append(Character(x, finstart, [255, 255, 255], 20, 20, [False, False, True, False]))
                        black = True
                        continue
                    else:
                        signs.append(Character(x, finstart, [0, 0, 255], 20, 20, [False, False, True, False]))
                        black = False
                        continue
    #skoori muutmine/kuvamine
    if not dead: score += int(speed)
    if not dead: scoretext = TextClass("Arial", 25, [10, 20], "Skoor: " + str(score), [0, 0, 0])
    if not dead and not night: scoretext.BlitText(screen)
    if not dead: scoretext.textlocation = [scoretext.textlocation[0] - 2, scoretext.textlocation[1] - 2]
    if not dead: scoretext.textcolor = [255, 255, 255]
    if not dead and not fog: scoretext.BlitText(screen)
    if not dead:
        leveltext = TextClass("Arial", 25, [12, 50], "Tase: " + str(sublevels - 2) + " (kontrollpunkt " + str(difficulty) + "/" + str(sublevels) + ")", [0, 0, 0])
        if not night: leveltext.BlitText(screen)
        leveltext.textlocation = [leveltext.textlocation[0] - 2, leveltext.textlocation[1] - 2]
        leveltext.textcolor = [255, 255, 255]
        if not fog: leveltext.BlitText(screen)
    if speed > 150:
        speed = 150
    if speed < 0:
        speed *= 10
    if player.traction < 0:
        player.traction = (-1) * player.traction
    if player.location_x < 60:
        player.location_x += (speed + 20)
        headlight_x += (speed + 20)
        damage += 0.0001
    elif player.location_x > res[0] - 100:
        player.location_x -= speed + 20
        headlight_x -= speed + 20
        damage += 0.0001
    leveltext = TextClass("Arial", 25, [12, res[1] - 40], str(int((speed / 45) * 150)) + " km/h | " + str(int(player.traction / 6 * 100)) + "% | Vigastus: " + str(round(damage / 30 * 100, 2)) + "% | FPS: " + str(int(clock.get_fps())), [0, 0, 0])
    if not invincible:
        if round(damage / 30 * 100, 2) > 100:
            leveltext = TextClass("Arial", 25, [12, res[1] - 40], str(int((speed / 45) * 150)) + " km/h | " + str(int(player.traction / 6 * 100)) + "% | Sõiduk hävitatud | FPS: " + str(int(clock.get_fps())), [0, 0, 0])
            dead = True
    if not night: leveltext.BlitText(screen)
    leveltext.textlocation = [leveltext.textlocation[0] - 2, leveltext.textlocation[1] - 2]
    leveltext.textcolor = [255, 255, 255]
    leveltext.BlitText(screen)
    
    #muudatuste ekraanile kuvamine ja ootamine
    pygame.display.flip()
    clock.tick(finalfps)
