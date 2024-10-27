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
pygame.display.set_caption("Timsort")
clock = pygame.time.Clock()


def insertion_sort(arr, colors, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        key_color = colors[i]
        j = i - 1

        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            colors[j + 1] = colors[j]
            yield j + 1

            j -= 1

        arr[j + 1] = key
        colors[j + 1] = key_color
        yield j + 1


def merge(arr, colors, left, mid, right):
    left_size = mid - left + 1
    right_size = right - mid

    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < left_size and j < right_size:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            colors[k] = get_color(left_arr[i])
            i += 1
        else:
            arr[k] = right_arr[j]
            colors[k] = get_color(right_arr[j])
            j += 1
        yield k
        k += 1

    while i < left_size:
        arr[k] = left_arr[i]
        colors[k] = get_color(left_arr[i])
        yield k
        i += 1
        k += 1

    while j < right_size:
        arr[k] = right_arr[j]
        colors[k] = get_color(right_arr[j])
        yield k
        j += 1
        k += 1


def timsort(arr, colors):
    min_run_size = 32
    n = len(arr)

    for start in range(0, n, min_run_size):
        end = min(start + min_run_size - 1, n - 1)
        yield from insertion_sort(arr, colors, start, end)

    size = min_run_size
    while size < n:
        for left in range(0, n, size * 2):
            mid = min(n - 1, left + size - 1)
            right = min((left + size * 2 - 1), (n - 1))
            if mid < right:
                yield from merge(arr, colors, left, mid, right)

        size *= 2


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
    array_size = 150
    array = [random.randint(1, 100) for _ in range(array_size)]

    max_value = max(array)
    colors = [get_color(value) for value in array]

    sorting_generator = timsort(array, colors)

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

        if time.time() - start_time > 45:
            running = False

    clip = ImageSequenceClip(frames, fps=FPS)
    clip.write_videofile('insertion_sorting.mp4', codec='libx264')

    for frame in frames:
        if os.path.exists(frame):
            os.remove(frame)

    pygame.quit()


if __name__ == "__main__":
    main()
