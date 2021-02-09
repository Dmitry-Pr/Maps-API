import os
import sys
import pygame
import requests


def update_x(x):
    if x >= 180:
        x = -1 * (360 - x)
    if x < -180:
        x = 360 + x
    return x


x = 0.0
y = 0.0
a = 6
b = 6
mode = "sat"
params = {
    "ll": str(x) + "," + str(y),
    "spn": str(a) + "," + str(b),
    "l": mode
}
map_request1 = "https://static-maps.yandex.ru/1.x/"
# Инициализируем pygame
response = requests.get(map_request1, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request1)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
# Переключаем экран и ждем закрытия окна.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y + 2 * a < 85:
                y += 2 * a
                print(y)
                params['ll'] = f'{x},{y}'
                response = requests.get(map_request1, params=params)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
            if event.key == pygame.K_DOWN and y - 2 * a > -85:
                y -= 2 * a
                print(y)
                params['ll'] = f'{x},{y}'
                response = requests.get(map_request1, params=params)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
            if event.key == pygame.K_LEFT:
                x -= 2 * a
                x = update_x(x)
                print(x)
                params['ll'] = f'{x},{y}'
                response = requests.get(map_request1, params=params)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
            if event.key == pygame.K_RIGHT:
                x += 2 * a
                x = update_x(x)
                print(x)
                params['ll'] = f'{x},{y}'
                response = requests.get(map_request1, params=params)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)

    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
