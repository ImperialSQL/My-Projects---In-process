def draw_triangle():
    for i in range(1, 16, 2):
        spaces = (15 - i) // 2
        print(' ' * spaces + '*' * i)

draw_triangle()