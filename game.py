import pygame
import gamebox
import random

camera = gamebox.Camera(900,600)
agreed = False

# images
sky_img = gamebox.from_image(500,160,"santa_sky.png")
santa = gamebox.from_image(200,200,"santa8_resized_converted.png")
grinch = gamebox.from_image(500,500,"grinch.png")
JackFrost = gamebox.from_image(820,50,"JackFrost.png")
santa.yspeed = 0
JackFrost.yspeed = 10
top_border = gamebox.from_color(-100,1, "black", 3000, 2)
ground = gamebox.from_color(-100, 600, "black", 3000, 20)
background_music = gamebox.load_sound("Grinch.wav")

# items
coins = [
    gamebox.from_image(random.randint(10,750), -10, "present1_converted.png"),
    gamebox.from_image(random.randint(10, 750), -18, "present1_converted.png"),
    gamebox.from_image(random.randint(10, 750), -15, "present1_converted.png"),
    gamebox.from_image(random.randint(10, 750), -30, "present1_converted.png")
]
cookies = [
    gamebox.from_image(random.randint(10,750), -40, "cookie1_converted.png"),
    gamebox.from_image(random.randint(10,750), -35, "cookie1_converted.png"),
    gamebox.from_image(random.randint(10,750), -32, "cookie1_converted.png"),
]
fire = []

# meters
time = 1500
score = 0
starting_health = 100


def tick(keys):
    global time
    global score
    global starting_health
    global time, score, minutes, agreed
    if agreed == False:
        camera.clear("white")
        messages = [
            gamebox.from_text(450, 25, "Santa's Big Adventure", "Arial", 34, "red"),
            gamebox.from_text(450, 75, "Created by: Anne Moshyedi and Julie Bond", "Arial", 34, "red"),
            gamebox.from_text(450, 175, "Rules:", "Arial", 30, "dark green"),
            gamebox.from_text(450, 225, "Use arrows to help Santa fly", "Arial", 30, "dark green"),
            gamebox.from_text(450, 275, "Collect presents to increase score", "Arial", 30, "dark green"),
            gamebox.from_text(450, 325, "Collect cookies to increase health", "Arial", 30, "dark green"),
            gamebox.from_text(450, 375, "The Grinch steals presents and lowers the score", "Arial", 30, "dark green"),
            gamebox.from_text(450, 425, "Jack Frost's ice lowers Santa's health", "Arial", 30, "dark green"),
            gamebox.from_text(450, 475, "Collect all the presents you can until time runs out or Santa dies!",
                                  "Arial", 30, "dark green"),
            gamebox.from_text(450, 575, "Press space to start", "Arial", 34, "red"),
        ]
        for message in messages:
            camera.draw(message)
        if pygame.K_SPACE in keys:
            agreed = True
        camera.display()
    if agreed == True:
        background_music.play()
        time -= 1
        seconds = str(int((time / ticks_per_second))).zfill(3)
        time_box = gamebox.from_text(650, 30, "Time Remaining: " + seconds, "arial", 24, "white")
        score_box = gamebox.from_text(75, 30, "Score: " + str(score), "arial", 24, "white")
        health_bar = gamebox.from_color(400, 50, "red", starting_health * 4, 30)
        santa.y = santa.y + santa.yspeed
        JackFrost.y += JackFrost.yspeed
        if JackFrost.bottom_touches(ground):
            JackFrost.yspeed = 0
        if JackFrost.touches(ground):
            JackFrost.move_to_stop_overlapping(ground)

        # santa movement
        if pygame.K_RIGHT in keys:
            santa.x += 6
        if pygame.K_LEFT in keys:
            santa.x -= 6
        if pygame.K_UP in keys:
            santa.y -= 6
        if pygame.K_DOWN in keys:
            santa.y += 6
        if santa.top_touches(top_border):
            santa.move_to_stop_overlapping(top_border)
        if santa.bottom_touches(ground):
            santa.yspeed = 0
        if santa.touches(ground):
            santa.move_to_stop_overlapping(ground)

        grinch.y += grinch.yspeed
        if santa.x < grinch.x:
            grinch.x -= 2
        if santa.x > grinch.x:
            grinch.x += 2
        if santa.y < grinch.y:
            grinch.y -= 2
        if santa.y > grinch.y:
            grinch.y += 2
        if santa.x < 0:
            santa.x = 900
        if santa.x > 900:
            santa.x = 0
        if santa.touches(grinch):
            score -= 1
            grinch.x = 800
            grinch.y = 500
        camera.draw(sky_img)
        for coin in coins:
            coin.speedy += 0.03
            if santa.touches(coin):
                score += 1
                coins.remove(coin)
            elif coin.y >= 610:
                coins.remove(coin)
            else:
                coin.move_speed()
        if len(coins) < 4:
            new_coin = gamebox.from_image(random.randint(10, 750), -10, "present1_converted.png")
            coins.append(new_coin)
        for coin in coins:
            camera.draw(coin)
        for cookie in cookies:
            cookie.speedy += 0.05
            if santa.touches(cookie):
                starting_health += 1
                cookies.remove(cookie)
            elif cookie.y >= 610:
                cookies.remove(cookie)
            else:
                cookie.move_speed()
        if len(cookies) < 3:
            new_cookie = gamebox.from_image(random.randint(10, 750), -15, "cookie1_converted.png")
            cookies.append(new_cookie)
        for cookie in cookies:
            camera.draw(cookie)
        if pygame.K_LEFT in keys:
            new_shot = gamebox.from_color(JackFrost.x,JackFrost.y,"white",12,12)
            fire.append(new_shot)
        for shot in fire:
            shot.x -= 5
            shot.y -= 5
            camera.draw(shot)
            if shot.touches(santa):
                starting_health -= 1
        if starting_health <= 0:
            camera.draw(gamebox.from_text(400, 200, "DEAD", "Helvetica", 70, "red"))
            camera.draw(gamebox.from_text(400,265, "Score" + ": " + str(score), "Helvetica", 40, "red"))
            gamebox.pause()
        if time < 0:
            camera.draw(gamebox.from_text(400, 200, "Game Over!", "Helvetica", 70, "red"))
            camera.draw(gamebox.from_text(400, 265, "Score" + ": " + str(score), "Helvetica", 40, "red"))
            gamebox.pause()
        camera.draw(santa)
        camera.draw(grinch)
        camera.draw(JackFrost)
        camera.draw(time_box)
        camera.draw(score_box)
        camera.draw(health_bar)
        camera.draw(top_border)
        camera.draw(ground)
        camera.display()

def intro(keys):
    global time, score, minutes, agreed

    if agreed == True:
        gamebox.timer_loop(ticks_per_second, tick)
    else:
        camera.clear("white")
        messages = [
            gamebox.from_text(450, 25,"Game project: Santa's Big Adventure","Arial",34,"red"),
            gamebox.from_text(450, 75, "Anne Moshyedi (acm4xb) and Julie Bond (jab5cr)", "Arial", 34, "red"),
            gamebox.from_text(450, 175, "Rules:", "Arial", 34, "red"),
            gamebox.from_text(450, 225, "Use arrows to help Santa fly", "Arial", 34, "red"),
            gamebox.from_text(450, 275, "Collect presents to increase score", "Arial", 34, "red"),
            gamebox.from_text(450, 325, "Collect cookies to increase health", "Arial", 34, "red"),
            gamebox.from_text(450, 375, "The Grinch steals presents and lowers the score", "Arial", 34, "red"),
            gamebox.from_text(450, 425, "Jack Frost's ice lowers Santa's health", "Arial", 34, "red"),
            gamebox.from_text(450, 475, "Collect all the presents you can until the timer runs out or Santa dies!", "Arial", 34, "red"),
            gamebox.from_text(450, 575, "Press space to start", "Arial", 34, "red"),
            ]
        for message in messages:
            camera.draw(message)
        if pygame.K_SPACE in keys:
            agreed = True
        camera.display()




ticks_per_second = 30

# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)

# santa character
# must collect a certain amount of presents before time runs out, Grinch can steal presents
# can increase health meter by eating cookies, jack frost sprays ice and can decrease meter