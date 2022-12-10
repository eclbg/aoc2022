CYCLES_TO_MONITOR = (20, 60, 100, 140, 180, 220)


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


def part1():
    with open("input.txt") as f:
        cycle = 1
        x = 1
        signal_strength = 0
        for row in f:
            row = row.strip()
            if row.startswith("noop"):
                if cycle in CYCLES_TO_MONITOR:
                    signal_strength += cycle * x
                cycle += 1
            else:
                inc = int(row.split()[1])
                if cycle in CYCLES_TO_MONITOR:
                    signal_strength += cycle * x
                cycle += 1
                if cycle in CYCLES_TO_MONITOR:
                    signal_strength += cycle * x
                x += inc
                cycle += 1
        return signal_strength


def draw_pixel(pixel: int, sprite_center: int) -> list[int]:
    sprite_pixels = (sprite_center - 1, sprite_center, sprite_center + 1)
    if pixel in sprite_pixels:
        return True
    return False


def draw_result(pixels_drawn: list[int]):
    result = ""
    for row in pixels_drawn:
        for i in range(40):
            result += "#" if i in row else "."
        result += "\n"
    return result


def part2():
    with open("input.txt") as f:
        cycle = 1
        x = 1
        pixels_drawn = [[], [], [], [], [], []]
        for row in f:
            row = row.strip()
            if row.startswith("noop"):
                pixel = (cycle - 1) % 40
                if draw_pixel(pixel=pixel, sprite_center=x):
                    pixels_drawn[(cycle - 1) // 40].append(pixel)
                cycle += 1
            else:
                pixel = (cycle - 1) % 40
                if draw_pixel(pixel=pixel, sprite_center=x):
                    pixels_drawn[(cycle - 1) // 40].append(pixel)
                inc = int(row.split()[1])
                cycle += 1
                pixel = (cycle - 1) % 40
                if draw_pixel(pixel=pixel, sprite_center=x):
                    pixels_drawn[(cycle - 1) // 40].append(pixel)
                x += inc
                cycle += 1
    return draw_result(pixels_drawn)


if __name__ == "__main__":
    print(part1())
    print(part2())
