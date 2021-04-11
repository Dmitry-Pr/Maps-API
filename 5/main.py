import os
import pygame
import requests


def update_x(x):
    if x > 180:
        x = -1.0 * (360 - x)
    if x < -180:
        x = 360.0 + x
    return x


def draw_map(params):
    map_request1 = "https://static-maps.yandex.ru/1.x/"
    map_file = "map.png"
    response = requests.get(map_request1, params=params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


x = 30.315868
y = 59.939095
a = 6
b = 4.5
mode = "map"
params = {
    "ll": str(x) + "," + str(y),
    "spn": str(a) + "," + str(b),
    "l": mode,
    'size': '600,450'
}
draw_map(params)
pygame.init()
map_file = "map.png"
screen = pygame.display.set_mode((600, 500))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
# Переключаем экран и ждем закрытия окна.
font = pygame.font.Font(None, 32)
map_font = pygame.font.Font(None, 18)
clock = pygame.time.Clock()
map_map = pygame.Rect(0, 0, 50, 50)
map_sat = pygame.Rect(0, 50, 50, 50)
map_skl = pygame.Rect(0, 100, 50, 50)
input_box = pygame.Rect(0, 450, 500, 50)
search = pygame.Rect(500, 450, 100, 50)
delete = pygame.Rect(500, 400, 100, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
act_col = (137, 144, 236)
pass_col = (200, 200, 200)
map_col = act_col
sat_col = skl_col = pass_col

active = False
text = ''
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if map_map.collidepoint(event.pos):
                map_col = act_col
                sat_col = skl_col = pass_col
                params['l'] = 'map'
                draw_map(params)
            if map_sat.collidepoint(event.pos):
                sat_col = act_col
                map_col = skl_col = pass_col
                params['l'] = 'sat'
                draw_map(params)
            if map_skl.collidepoint(event.pos):
                skl_col = act_col
                sat_col = map_col = pass_col
                params['l'] = 'sat,skl'
                draw_map(params)
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            if delete.collidepoint(event.pos):
                params['pt'] = ''
                text = ''
                draw_map(params)
            if search.collidepoint(event.pos):
                print(text)
                response = requests.get(
                    "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode=" + text)
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                print(toponym_coodrinates)
                x, y = map(float, toponym_coodrinates.split())
                params["ll"] = str(x) + "," + str(y)
                params['pt'] = str(x) + "," + str(y) + ',round'
                draw_map(params)
                pygame.display.flip()
            # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.key == pygame.K_PAGEUP:
                if a - 0.2 > 0 and b - 0.15 > 0:
                    a -= 0.2
                    b -= 0.15
                elif a - 0.02 > 0 and b - 0.015 > 0:
                    a -= 0.02
                    b -= 0.015
                elif a - 0.002 > 0 and b - 0.0015 > 0:
                    a -= 0.002
                    b -= 0.0015

                print(a, b)
                params['spn'] = f'{a},{b}'
                draw_map(params)
            if event.key == pygame.K_PAGEDOWN:
                if a - 0.2 > 0 and b - 0.15 > 0 and a + 0.2 < 90:
                    a += 0.2
                    b += 0.15
                elif a - 0.02 > 0 and b - 0.015 > 0 and a + 0.02 < 90:
                    a += 0.02
                    b += 0.015
                elif a - 0.002 > 0 and b - 0.0015 > 0 and a + 0.002 < 90:
                    a += 0.002
                    b += 0.0015
                else:
                    a += 0.002
                    b += 0.0015
                params['spn'] = f'{a},{b}'
                draw_map(params)
            if event.key == pygame.K_UP and y + b < 85:
                y += b
                print(y)
                params['ll'] = f'{x},{y}'
                draw_map(params)
            if event.key == pygame.K_DOWN and y - b > -85:
                y -= b
                print(y)
                params['ll'] = f'{x},{y}'
                draw_map(params)
            if event.key == pygame.K_LEFT:
                x -= a
                x = update_x(x)
                print(x)
                params['ll'] = f'{x},{y}'
                print(params)
                draw_map(params)
            if event.key == pygame.K_RIGHT:
                x += a
                x = update_x(x)
                print(x)
                params['ll'] = f'{x},{y}'
                print(params)
                draw_map(params)

    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load(map_file), (0, 0))
    txt_surface = font.render(text, True, color)
    txt_search = font.render('Искать', True, (0, 0, 0))
    txt_delete = font.render("Сброс", True, (0, 0, 0))
    map_txt = map_font.render('Схема', True, (0, 0, 0))
    sat_txt = map_font.render('Спутник', True, (0, 0, 0))
    skl_txt = map_font.render('Гибрид', True, (0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, map_col, map_map)
    pygame.draw.rect(screen, sat_col, map_sat)
    pygame.draw.rect(screen, skl_col, map_skl)
    pygame.draw.rect(screen, (200, 200, 200), search)
    pygame.draw.rect(screen, (200, 200, 200), delete)
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(txt_search, (search.x + 15, search.y + 15))
    screen.blit(txt_delete, (delete.x + 15, delete.y + 15))
    screen.blit(map_txt, (map_map.x + 5, map_map.y + 20))
    screen.blit(sat_txt, (map_sat.x, map_sat.y + 20))
    screen.blit(skl_txt, (map_skl.x + 2, map_skl.y + 20))
    pygame.display.flip()

pygame.quit()

os.remove(map_file)
