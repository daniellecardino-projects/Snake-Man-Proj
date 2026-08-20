from PIL import Image, ImageDraw, ImageFilter
import math


SIZE = 512


base = Image.new(
    "RGBA",
    (SIZE, SIZE),
    (3, 3, 10, 255)
)


# ---------------------------------------------------------
# GLOW LAYER
# ---------------------------------------------------------

glow = Image.new(
    "RGBA",
    (SIZE, SIZE),
    (0, 0, 0, 0)
)

g = ImageDraw.Draw(glow)


# Purple/cyan atmospheric glow

g.ellipse(
    (40, 40, 472, 472),
    fill=(0, 246, 255, 35)
)

g.ellipse(
    (90, 90, 422, 422),
    fill=(155, 53, 255, 35)
)


glow = glow.filter(
    ImageFilter.GaussianBlur(45)
)


base = Image.alpha_composite(
    base,
    glow
)


# ---------------------------------------------------------
# NEON RING
# ---------------------------------------------------------

ring = Image.new(
    "RGBA",
    (SIZE, SIZE),
    (0, 0, 0, 0)
)

r = ImageDraw.Draw(ring)


for width, alpha in [
    (34, 25),
    (20, 50),
    (10, 100),
    (5, 220)
]:

    r.ellipse(
        (75, 75, 437, 437),
        outline=(0, 246, 255, alpha),
        width=width
    )


ring = ring.filter(
    ImageFilter.GaussianBlur(3)
)


base = Image.alpha_composite(
    base,
    ring
)


# ---------------------------------------------------------
# PAC-MAN STYLE BOMB
# ---------------------------------------------------------

bomb = Image.new(
    "RGBA",
    (SIZE, SIZE),
    (0, 0, 0, 0)
)

b = ImageDraw.Draw(bomb)


# bomb glow

for width, alpha in [
    (55, 20),
    (35, 40),
    (18, 80)
]:

    b.ellipse(
        (135, 135, 377, 377),
        outline=(255, 22, 143, alpha),
        width=width
    )


# bomb body

b.ellipse(
    (145, 145, 367, 367),
    fill=(9, 10, 24, 255),
    outline=(255, 22, 143, 255),
    width=8
)


# Pac-Man wedge

cx = 256
cy = 256
radius = 110

gap = math.radians(38)

start = gap
end = 360 - gap

points = [
    (cx, cy),
]

for i in range(80):

    angle = math.radians(
        start +
        (end - start) *
        i /
        79
    )

    points.append(
        (
            cx +
            radius *
            math.cos(angle),

            cy +
            radius *
            math.sin(angle)
        )
    )


b.polygon(
    points,
    fill=(3, 4, 12, 255)
)


# bomb highlight

b.arc(
    (165, 165, 340, 340),
    205,
    300,
    fill=(0, 246, 255, 255),
    width=7
)


# ---------------------------------------------------------
# FUSE
# ---------------------------------------------------------

b.line(
    [
        (337, 158),
        (375, 125),
        (365, 95)
    ],
    fill=(255, 230, 0, 255),
    width=10,
    joint="curve"
)


b.ellipse(
    (350, 78, 382, 110),
    fill=(255, 255, 255, 255)
)


# ---------------------------------------------------------
# CYBERPUNK SNAKE
# ---------------------------------------------------------

snake_points = []

for i in range(230):

    t = i / 229

    angle = (
        t *
        math.pi *
        3.7
    )

    radius = (
        185 -
        t * 30
    )

    x = (
        256 +
        radius *
        math.cos(angle)
    )

    y = (
        256 +
        radius *
        math.sin(angle)
    )

    snake_points.append(
        (int(x), int(y))
    )


# glow snake

snake_glow = Image.new(
    "RGBA",
    (SIZE, SIZE),
    (0, 0, 0, 0)
)

sg = ImageDraw.Draw(
    snake_glow
)


sg.line(
    snake_points,
    fill=(0, 246, 255, 210),
    width=32,
    joint="curve"
)


snake_glow = snake_glow.filter(
    ImageFilter.GaussianBlur(18)
)


bomb = Image.alpha_composite(
    bomb,
    snake_glow
)


b = ImageDraw.Draw(bomb)


# snake base

b.line(
    snake_points,
    fill=(8, 18, 35, 255),
    width=27,
    joint="curve"
)


# cyan edge

b.line(
    snake_points,
    fill=(0, 246, 255, 255),
    width=8,
    joint="curve"
)


# pink secondary edge

for i in range(
    0,
    len(snake_points) - 1,
    18
):

    b.line(
        snake_points[i:i+12],
        fill=(255, 22, 143, 255),
        width=5,
        joint="curve"
    )


# ---------------------------------------------------------
# SNAKE HEAD
# ---------------------------------------------------------

hx, hy = snake_points[-1]

b.ellipse(
    (
        hx - 28,
        hy - 28,
        hx + 28,
        hy + 28
    ),
    fill=(5, 12, 25, 255),
    outline=(0, 246, 255, 255),
    width=7
)


# visor

b.arc(
    (
        hx - 19,
        hy - 11,
        hx + 19,
        hy + 11
    ),
    200,
    340,
    fill=(255, 22, 143, 255),
    width=5
)


# ---------------------------------------------------------
# COMPOSITE
# ---------------------------------------------------------

base = Image.alpha_composite(
    base,
    bomb
)


# ---------------------------------------------------------
# FINAL BLOOM
# ---------------------------------------------------------

final_glow = base.filter(
    ImageFilter.GaussianBlur(1.2)
)

base = Image.blend(
    base,
    final_glow,
    .18
)


base.resize(
    (512, 512),
    Image.Resampling.LANCZOS
).save(
    "icon.png",
    "PNG"
)


print(
    "Created icon.png"
)
