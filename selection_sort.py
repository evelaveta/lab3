import pygame
import random
import time
import imageio
from PIL import Image
import os

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
FPS = 120
SWAP_DELAY = 100 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Selection sort")
clock = pygame.time.Clock()


def selection_sort(arr, colors):
    n = len(arr)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if colors[j] > colors[max_idx]:
                max_idx = j

        if max_idx != i:
            arr[i], arr[max_idx] = arr[max_idx], arr[i]
            colors[i], colors[max_idx] = colors[max_idx], colors[i]
            yield i, max_idx 


def get_color(value):
    gray_value = int((value / max_value) * 255)
    return (gray_value, gray_value, gray_value)


def draw_bars(arr, colors):
    screen.fill(BACKGROUND_COLOR)
    bar_width = WIDTH // len(arr)

    for i in range(len(arr)):
        color = colors[i]
        bar_height = HEIGHT

        pygame.draw.rect(screen,
                         color,
                         (i * bar_width, HEIGHT - bar_height - 10, bar_width - 1, bar_height))

    pygame.display.flip()

def save_frame(frame_number):
    pygame.image.save(screen, f"frame_{frame_number:04d}.png")


def main():
    global max_value
    # РіРµРЅРµСЂР°С†РёСЏ РјР°СЃСЃРёРІР° СЃ СЃР»СѓС‡Р°Р№РЅС‹РјРё Р·РЅР°С‡РµРЅРёСЏРјРё Рё СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёРјРё С†РІРµС‚Р°РјРё
    array_size = 100
    array = [random.randint(1, 100) for _ in range(array_size)]  # СЃР»СѓС‡Р°Р№РЅС‹Рµ Р·РЅР°С‡РµРЅРёСЏ РѕС‚ 1 РґРѕ 100
    max_value = max(array)
    colors = [get_color(value) for value in array]  # С†РІРµС‚Р° СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‚ Р·РЅР°С‡РµРЅРёСЏРј

    sorting_generator = selection_sort(array, colors)

    start_time = time.time()
    running = True
    frame_number = 0
    frames = []
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            indices_to_highlight = next(sorting_generator)  # РёРЅРґРµРєСЃС‹
            draw_bars(array, colors)  # РѕС‚СЂРёСЃРѕРІРєР° РјР°СЃСЃРёРІР°

            save_frame(frame_number)
            frames.append(f"frame_{frame_number:04d}.png")
            frame_number += 1

            pygame.time.delay(SWAP_DELAY)

            clock.tick(FPS)
        except StopIteration:
            draw_bars(array, colors)
            save_frame(frame_number)
            frames.append(f"frame_{frame_number:04d}.png")
            frame_number += 1

        if time.time() - start_time > 12:
            running = False

    images = [Image.open(frame) for frame in frames]
    imageio.mimsave('selection_sort.gif', images, duration=SWAP_DELAY/1000)

    for frame in frames:
        os.remove(frame)
    
    pygame.quit()


if __name__ == "__main__":
    main()
