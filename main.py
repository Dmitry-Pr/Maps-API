import os
import sys

import pygame
import requests






x = 133.795384
y = -25.694768
a = 20
b = 20
mode = "sat"
params = {
    "ll": str(x) + "," + str(y),
    "spn": str(a) + "," + str(b),
    "l":  mode

}



map_request1 = "https://static-maps.yandex.ru/1.x/"






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

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
