import math
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
a = 2.15
b = 2.15
mode = "map"
params = {
    "ll": str(x) + "," + str(y),
    "spn": str(a) + "," + str(b),
    "l": mode,
    'size': '450,450'
}
search_params = {
    "apikey": "9cce441c-5f32-40ef-b228-730f8fb654ca",
    "text": "",
    "lang": "ru_RU",
    "type": "biz",
    'spn': '0.016,0.016',
    'll': '',
    'results': '1'
}

draw_map(params)
pygame.init()
map_file = "map.png"
address = ''
index = ''
ind = False
screen = pygame.display.set_mode((450, 500))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
# Переключаем экран и ждем закрытия окна.
font = pygame.font.Font(None, 32)
map_font = pygame.font.Font(None, 18)
ad_font = pygame.font.Font(None, 26)
clock = pygame.time.Clock()
map_map = pygame.Rect(0, 0, 50, 50)
map_sat = pygame.Rect(0, 50, 50, 50)
map_skl = pygame.Rect(0, 100, 50, 50)
input_box = pygame.Rect(0, 450, 350, 50)
search = pygame.Rect(350, 450, 100, 50)
delete = pygame.Rect(350, 400, 100, 50)
address_r = pygame.Rect(110, 0, 340, 50)
index_r = pygame.Rect(400, 50, 50, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
act_col = (137, 144, 236)
pass_col = (200, 200, 200)
map_col = act_col
ind_col = sat_col = skl_col = pass_col

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
                continue
            if map_sat.collidepoint(event.pos):
                sat_col = act_col
                map_col = skl_col = pass_col
                params['l'] = 'sat'
                draw_map(params)
                continue
            if map_skl.collidepoint(event.pos):
                skl_col = act_col
                sat_col = map_col = pass_col
                params['l'] = 'sat,skl'
                draw_map(params)
                continue

            if index_r.collidepoint(event.pos):
                if ind_col == pass_col:
                    ind_col = act_col
                    address += ' ' + index
                    ind = True
                else:
                    ind = False
                    if f' {index}' in address and index != '':
                        address = address.replace(' ' + index, '')
                    address = address.replace(index, '')
                    ind_col = pass_col
                continue

            if input_box.collidepoint(event.pos):
                active = not active
                color = color_active if active else color_inactive
                continue
            else:
                active = False
                color = color_active if active else color_inactive
            if delete.collidepoint(event.pos):
                params['pt'] = ''
                address = ''
                index = ''
                text = ''
                draw_map(params)
                continue

            if search.collidepoint(event.pos):
                print(text)
                response = requests.get(
                    "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode=" + text)
                json_response = response.json()
                print(json_response)
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                address = toponym['metaDataProperty']['GeocoderMetaData']['text']
                try:
                    index = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                except KeyError:
                    index = ''
                if ind:
                    address += ' ' + index
                print(toponym_coodrinates)
                x, y = map(float, toponym_coodrinates.split())
                params["ll"] = str(x) + "," + str(y)
                params['pt'] = str(x) + "," + str(y) + ',round'
                draw_map(params)
                pygame.display.flip()
                continue

            # Change the current color of the input box.
            color = color_active if active else color_inactive
            if event.button == 1:
                index = ''
                text = ''
                g_p_x = float(params['spn'].split(',')[0]) / 450
                g_p_y = float(params['spn'].split(',')[1]) / 450
                nx = (225 - event.pos[0]) * g_p_x * 2.3
                ny = (225 - event.pos[1]) * g_p_y * 1.18
                prev_x, prev_y = params['ll'].split(',')
                new_x = float(prev_x) - nx
                new_x = update_x(new_x)
                new_y = float(prev_y) + ny
                params['pt'] = str(new_x) + "," + str(new_y) + ',round'
                response = requests.get(
                    "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode="
                    + str(new_x) + "," + str(new_y))
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                address = toponym['metaDataProperty']['GeocoderMetaData']['text']
                try:
                    index = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                except KeyError:
                    index = ''
                if ind:
                    address += ' ' + index
                print(params)
                print(x, y, a)
                draw_map(params)
            if event.button == 3:
                index = ''
                text = ''
                g_p_x = float(params['spn'].split(',')[0]) / 450
                g_p_y = float(params['spn'].split(',')[1]) / 450
                nx = (225 - event.pos[0]) * g_p_x * 2.3
                ny = (225 - event.pos[1]) * g_p_y * 1.18
                prev_x, prev_y = params['ll'].split(',')
                new_x = float(prev_x) - nx
                new_x = update_x(new_x)
                new_y = float(prev_y) + ny

                response = requests.get(
                    "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode="
                    + str(new_x) + "," + str(new_y))
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                s = toponym['metaDataProperty']['GeocoderMetaData']['text']

                params['pt'] = str(new_x) + "," + str(new_y) + ',round'
                search_params['text'] = s
                search_params['ll'] = str(x) + "," + str(y)
                response = requests.get("https://search-maps.yandex.ru/v1/", params=search_params)
                json_response = response.json()
                organization = json_response["features"][0]
                # Название организации.
                org_name = organization["properties"]["CompanyMetaData"]["name"]
                print(json_response)
                address = org_name
                print(search_params)
                draw_map(params)
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.key == pygame.K_PAGEUP:
                if a - 0.2 > 0 and b - 0.2 > 0:
                    a -= 0.2
                    b -= 0.2
                elif a - 0.02 > 0 and b - 0.02 > 0:
                    a -= 0.02
                    b -= 0.02
                elif a - 0.002 > 0 and b - 0.002 > 0:
                    a -= 0.002
                    b -= 0.002

                print(a, b)
                params['spn'] = f'{a},{b}'
                draw_map(params)
            if event.key == pygame.K_PAGEDOWN:
                if a - 0.2 > 0 and a + 0.2 < 90:
                    a += 0.2
                    b += 0.2
                elif a - 0.02 > 0 and a + 0.02 < 90:
                    a += 0.02
                    b += 0.02
                elif a - 0.002 > 0 and a + 0.002 < 90:
                    a += 0.002
                    b += 0.002
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
    txt_ad = map_font.render('Адрес:', True, (0, 0, 0))
    index_txt = map_font.render('Индекс', True, (0, 0, 0))
    map_txt = map_font.render('Схема', True, (0, 0, 0))
    sat_txt = map_font.render('Спутник', True, (0, 0, 0))
    skl_txt = map_font.render('Гибрид', True, (0, 0, 0))
    address_txt = map_font.render(address, True, (0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, (240, 240, 240), address_r)
    pygame.draw.rect(screen, map_col, map_map)
    pygame.draw.rect(screen, sat_col, map_sat)
    pygame.draw.rect(screen, skl_col, map_skl)
    pygame.draw.rect(screen, (200, 200, 200), search)
    pygame.draw.rect(screen, (160, 160, 160), delete)
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.draw.rect(screen, ind_col, index_r)
    screen.blit(txt_search, (search.x + 15, search.y + 15))
    screen.blit(address_txt, (address_r.x + 15, address_r.y + 15))
    screen.blit(txt_delete, (delete.x + 15, delete.y + 15))
    screen.blit(map_txt, (map_map.x + 5, map_map.y + 20))
    screen.blit(sat_txt, (map_sat.x, map_sat.y + 20))
    screen.blit(skl_txt, (map_skl.x + 2, map_skl.y + 20))
    screen.blit(index_txt, (index_r.x + 2, index_r.y + 20))
    screen.blit(txt_ad, (58, 20))
    pygame.display.flip()

pygame.quit()

os.remove(map_file)
