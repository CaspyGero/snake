def gameSnake(totalPositions, boxWidth, marginSprites, speed):
    import pygame
    from os import path
    from random import randint
    from time import sleep
    #Initial variables
    pygame.init()
    pygame.display.set_caption("Snake")
    logoSnake = pygame.image.load(path.dirname(__file__) + "/logoSnake.png")
    pygame.display.set_icon(logoSnake)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    running = True
    margin = {"up" : 30, "right" : 20, "down" : 20, "left" : 20}
    screen = pygame.display.set_mode((boxWidth * totalPositions + margin["left"] + margin["right"], boxWidth * totalPositions + margin["up"] + margin["down"]))
    #Define variables
    points = 0
    positions = {}
    for position in range(0, totalPositions):
        positions[position + 1] = position * boxWidth
    pointsText = font.render(str(points), 1, "white")
    centerPoints = pointsText.get_rect()
    centerPoints.centerx = screen.get_width() // 2
    centerPoints.centery = 15
    startText = font.render("Press space", 1, "white", "black")
    centerStart = startText.get_rect()
    centerStart.centerx = screen.get_width() // 2
    centerStart.centery = screen.get_height() // 2 - boxWidth * 2
    loseText = font.render("You lose!", 1, "white", "black")
    centerLose = loseText.get_rect()
    centerLose.centerx = screen.get_width() // 2
    centerLose.centery = screen.get_height() // 2 + boxWidth * 2
    blackErase = font.render("You lose!", 1, "black", "black")
    #Losing function
    def losing():
        blink = False
        for blinking in range(0, 5):
            if blink == False:
                screen.blit(loseText, centerLose)
                blink = True
            else:
                screen.blit(blackErase, centerLose)
                blink = False
            #Update screen
            pygame.display.flip()
            clock.tick(speed)
            #Span for blinks
            sleep(0.75)
        return True
    #Principal function
    while running:
        #Reset variables
        positionSnake = pygame.Vector2(margin["left"] + positions[totalPositions // 2], margin["up"] + positions[totalPositions // 2])
        positionApple = pygame.Vector2(margin["left"] + positions[randint(totalPositions // 2 + 1, totalPositions)], margin["up"] +  positions[randint(1, totalPositions)])
        direction = "right"
        lose = True
        points = 0
        bodies = 0
        positionBodies = []
        pointsText = font.render(str(points), 1, "white")
        #Detect actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lose = False
        #Draw sprites
        screen.fill("black")
        screen.blit(pointsText, centerPoints)
        screen.blit(startText, centerStart)
        pygame.draw.line(screen, "white", (margin["left"], margin["up"]), (screen.get_width() - margin["right"], margin["up"]), 2)
        pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], margin["up"]), (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), 2)
        pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), (margin["left"], screen.get_height() - margin["down"]), 2)
        pygame.draw.line(screen, "white", (margin["left"], screen.get_height() - margin["down"]), (margin["left"], margin["up"]), 2)
        snake = pygame.draw.rect(screen, "white", (positionSnake.x + marginSprites, positionSnake.y + marginSprites, boxWidth - marginSprites * 2, boxWidth - marginSprites * 2))
        #Update screen
        pygame.display.flip()
        #Only start when space was pressed
        while not lose:
            #Detect actions
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    lose = True
                    continue
                if event.type == pygame.KEYDOWN:
                    #Snake
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and direction != "down":
                        direction = "up"
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and direction != "left":
                        direction = "right"
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and direction != "up":
                        direction = "down"
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and direction != "right":
                        direction = "left"
            for bodie in range(0, bodies):
                try:
                    if bodie < bodies - 1:
                        positionBodies[bodie] = pygame.Vector2(positionBodies[bodie + 1].x, positionBodies[bodie + 1].y)
                    else:
                        if len(positionBodies) < bodies:
                            positionBodies.append(pygame.Vector2(positionSnake.x, positionSnake.y))
                        else:
                            positionBodies[bodie] = pygame.Vector2(positionSnake.x, positionSnake.y)
                except IndexError as e:
                    continue
            #Mobile objects coordinates
            if direction == "up":
                positionSnake.y -= boxWidth
            elif direction == "right":
                positionSnake.x += boxWidth
            elif direction == "down":
                positionSnake.y += boxWidth
            elif direction == "left":
                positionSnake.x -= boxWidth
            if positionSnake.y < margin["up"] + positions[1] or positionSnake.x > margin["right"] + positions[max(positions.keys())] or positionSnake.y > margin["up"] + positions[max(positions.keys())] or positionSnake.x < margin["left"] + positions[1]:
                lose = losing()
                continue
            #Draw sprites
            screen.fill("black")
            pointsText = font.render(str(points), 1, "white")
            screen.blit(pointsText, centerPoints)
            pygame.draw.line(screen, "white", (margin["left"], margin["up"]), (screen.get_width() - margin["right"], margin["up"]), 2)
            pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], margin["up"]), (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), 2)
            pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), (margin["left"], screen.get_height() - margin["down"]), 2)
            pygame.draw.line(screen, "white", (margin["left"], screen.get_height() - margin["down"]), (margin["left"], margin["up"]), 2)
            snake = pygame.draw.rect(screen, "white", (positionSnake.x + marginSprites, positionSnake.y + marginSprites, boxWidth - marginSprites * 2, boxWidth - marginSprites * 2))
            apple = pygame.draw.rect(screen, "red", (positionApple.x + marginSprites, positionApple.y + marginSprites, boxWidth - marginSprites * 2, boxWidth - marginSprites * 2))
            for bodiePosition in range(0, len(positionBodies)):
                pygame.draw.rect(screen, "white", (positionBodies[bodiePosition].x + marginSprites, positionBodies[bodiePosition].y + marginSprites, boxWidth - marginSprites * 2, boxWidth - marginSprites * 2))
            #Collitions
            if snake.colliderect(apple):
                points += 1
                bodies += 1
                if 1 + bodies < totalPositions ** 2:
                    while (positionSnake == positionApple) or (positionApple in positionBodies):
                        positionApple.x = margin["left"] + positions[randint(1, totalPositions)]
                        positionApple.y = margin["up"] + positions[randint(1, totalPositions)]
            if positionSnake in positionBodies:
                lose = losing()
                continue
            #Update screen
            pygame.display.flip()
            clock.tick(speed)
    pygame.quit()
    global hasTkinter
    if __name__ == "__main__" and hasTkinter == "s":
        launcher()

def startGame():
    global root
    totalPositions = int(inputPositions.get())
    boxWidth = int(inputPositions.get())
    maginSprite = int(inputMargin.get())
    speed = int(inputSpeed.get())
    root.destroy()
    gameSnake(totalPositions, boxWidth, maginSprite, speed)

def resetValues():
    global inputPositions, inputWidth, inputMargin, inputSpeed
    inputPositions.delete(0, "end")
    inputWidth.delete(0, "end")
    inputMargin.delete(0, "end")
    inputSpeed.delete(0, "end")
    inputPositions.insert(0, 15)
    inputWidth.insert(0, 32)
    inputMargin.insert(0, 2)
    inputSpeed.insert(0, 7)

def launcher():
    global inputPositions, inputWidth, inputMargin, inputSpeed, root
    import tkinter
    from os import path
    root = tkinter.Tk()
    root.title("Pong launcher")
    root.geometry("300x215+600+300")
    root.resizable(0,0)

    frameMain = tkinter.Frame(root, width=130)
    frameMain.pack(side=tkinter.RIGHT, fill=tkinter.Y, padx=20, pady=5)
    frameImage = tkinter.Frame(root, width=140)
    frameImage.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=5, pady=5)
    
    imageFile = path.dirname(__file__) + "/imagenSnake.png"
    image = tkinter.PhotoImage(file=imageFile)

    labelImage = tkinter.Label(frameImage, image=image)
    labelImage.pack()

    labelPositions = tkinter.Label(frameMain, text="Enter the total positions: ", justify="center")
    labelPositions.pack()
    inputPositions = tkinter.Entry(frameMain)
    inputPositions.pack()
    inputPositions.insert(0, 15)

    labelWidth = tkinter.Label(frameMain, text="Enter the boxes width: ", justify="center")
    labelWidth.pack()
    inputWidth = tkinter.Entry(frameMain)
    inputWidth.pack()
    inputWidth.insert(0, 32)

    labelMargin = tkinter.Label(frameMain, text="Enter the boxes margin: ", justify="center")
    labelMargin.pack()
    inputMargin = tkinter.Entry(frameMain)
    inputMargin.pack()
    inputMargin.insert(0, 2)

    labelSpeed = tkinter.Label(frameMain, text="Enter the speed: ", justify="center")
    labelSpeed.pack()
    inputSpeed = tkinter.Entry(frameMain)
    inputSpeed.pack()
    inputSpeed.insert(0, 7)

    buttonStart = tkinter.Button(frameMain, text="Reset values", command=resetValues)
    buttonStart.pack(pady=10, side=tkinter.LEFT)
    buttonStart = tkinter.Button(frameMain, text="Start game", command=startGame)
    buttonStart.pack(pady=10, side=tkinter.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    hasTkinter = input("Is tkinter installed (S/n)? ").lower()
    if hasTkinter == "s":
        launcher()
    else:
        print("Launching in base config")
        gameSnake(15, 32, 2, 7)