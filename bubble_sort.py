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
pygame.display.set_caption("Bubble sort")
clock = pygame.time.Clock()

def bubble_sort(arr, colors):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if colors[j] > colors[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                colors[j], colors[j + 1] = colors[j + 1], colors[j]
                yield j, j + 1

def get_color(value):
    gray_value = int((value / max_value) * 255)
    return (gray_value, gray_value, gray_value)

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
    global max_value
    array_size = 100
    array = [random.randint(1, 100) for _ in range(array_size)]
    max_value = max(array)
    colors = [get_color(value) for value in array]

    sorting_generator = bubble_sort(array, colors)

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

        if time.time() - start_time > 60:
            running = False
            
    clip = ImageSequenceClip(frames, fps=FPS)
    clip.write_videofile('bubble_sorting.mp4', codec='libx264')

    for frame in frames:
        if os.path.exists(frame):
            os.remove(frame)

    pygame.quit()

if __name__ == "__main__":
    main()
