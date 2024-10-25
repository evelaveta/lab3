import pygame
import random

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
FPS = 120
SWAP_DELAY = 100  # задержка в миллисекундах после каждого обмена

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сортировка выбором")
clock = pygame.time.Clock()


def selection_sort(arr, colors):
    n = len(arr)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if colors[j] > colors[max_idx]:
                max_idx = j

        # обмен значений и цветов
        if max_idx != i:
            arr[i], arr[max_idx] = arr[max_idx], arr[i]
            colors[i], colors[max_idx] = colors[max_idx], colors[i]
            yield i, max_idx  # возврат индексов

def get_color(value):
    # функция для получения черно-белого цвета в зависимости от значения
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


def main():
    global max_value
    # генерация массива с случайными значениями и соответствующими цветами
    array_size = 100
    array = [random.randint(1, 100) for _ in range(array_size)]  # случайные значения от 1 до 100
    max_value = max(array)
    colors = [get_color(value) for value in array]  # цвета соответствуют значениям

    sorting_generator = selection_sort(array, colors)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            indices_to_highlight = next(sorting_generator)  # индексы
            draw_bars(array, colors)  # отрисовка массива

            pygame.time.delay(SWAP_DELAY)

            clock.tick(FPS)
        except StopIteration:
            draw_bars(array, colors)  # отрисовка окончательного состояния
            #running = False

    #pygame.quit()


if __name__ == "__main__":
    main()