import pygame
import random
import time
import imageio
from PIL import Image
import os
from moviepy.editor import ImageSequenceClip


WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
FPS = 120
SWAP_DELAY = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color sort")
clock = pygame.time.Clock()


def insertion_sort(arr, colors):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        key_color = colors[i]
        j = i - 1

        while j >= 0 and colors[j] > key_color:
            arr[j + 1] = arr[j]
            colors[j + 1] = colors[j]
            yield j + 1
            j -= 1

        arr[j + 1] = key
        colors[j + 1] = key_color
        yield j + 1


def get_color(value):
    r = (value * 10) % 256
    g = (value * 20) % 256
    b = (value * 30) % 256
    return (r, g, b)


def draw_bars(arr, colors):
    screen.fill(BACKGROUND_COLOR)
    bar_width = WIDTH // len(arr)
    bar_height = HEIGHT

    for i in range(len(arr)):
        color = colors[i]
        pygame.draw.rect(screen,
                         color,
                         (i * bar_width, HEIGHT - bar_height, bar_width - 1, bar_height))

    pygame.display.flip()

def save_frame(frame_number):
    pygame.image.save(screen, f"frame_{frame_number:04d}.png")


def main():
    array_size = 150
    array = [random.randint(1, 100) for _ in range(array_size)]
    colors = [get_color(value) for value in array]

    sorting_generator = insertion_sort(array, colors)

    start_time = time.time()
    running = True
    frame_number = 0
    frames = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            indices_to_highlight = next(sorting_generator)
            draw_bars(array, colors)

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

        if time.time() - start_time > 125:
            running = False

    clip = ImageSequenceClip(frames, fps=FPS)
    clip.write_videofile('color_sorting.mp4', codec='libx264')

    for frame in frames:
        os.remove(frame)

    pygame.quit()

if __name__ == "__main__":
    main()
