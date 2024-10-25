import pygame
import random

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
FPS = 120
SWAP_DELAY = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сортировка слиянием")
clock = pygame.time.Clock()


def merge(arr, colors, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]

    L_colors = colors[left:mid + 1]
    R_colors = colors[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            colors[k] = get_color(L[i])
            i += 1
        else:
            arr[k] = R[j]
            colors[k] = get_color(R[j])
            j += 1
        yield k
        k += 1

    while i < n1:
        arr[k] = L[i]
        colors[k] = get_color(L[i])
        yield k
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        colors[k] = get_color(R[j])
        yield k
        j += 1
        k += 1


def merge_sort(arr, colors, left, right):
    if left < right:
        mid = (left + right) // 2

        yield from merge_sort(arr, colors, left, mid)
        yield from merge_sort(arr, colors, mid + 1, right)

        yield from merge(arr, colors, left, mid, right)


def get_color(value):
    gray_value = int((value / max_value) * 255)
    return (gray_value, gray_value, gray_value)


def draw_bars(arr, colors):
    screen.fill(BACKGROUND_COLOR)
    bar_width = WIDTH // len(arr)

    for i in range(len(arr)):
        color = colors[i]
        bar_height = int((arr[i] / max_value) * (HEIGHT - 20))

        pygame.draw.rect(screen,
                         color,
                         (i * bar_width, HEIGHT - bar_height - 10, bar_width - 1, bar_height))

    pygame.display.flip()


def main():
    global max_value
    array_size = 100
    array = [random.randint(1, 100) for _ in range(array_size)]

    max_value = max(array)
    colors = [get_color(value) for value in array]

    sorting_generator = merge_sort(array, colors, 0, len(array) - 1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            indices_to_highlight = next(sorting_generator)
            draw_bars(array, colors)

            pygame.time.delay(SWAP_DELAY)

            clock.tick(FPS)
        except StopIteration:
            draw_bars(array, colors)
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()