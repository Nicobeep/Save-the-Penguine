import pygame
import math
import random

pygame.init()

# ============================================================
# SAVE THE PENGUIN
# ============================================================

WIDTH = 1000
HEIGHT = 750
FPS = 60

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Save the Penguin"
)

clock = pygame.time.Clock()


# ============================================================
# COLORS
# ============================================================

WATER = (35, 135, 210)
WATER_LIGHT = (65, 165, 225)

ICE = (175, 230, 250)
ICE_EDGE = (70, 155, 195)

BLACK = (25, 30, 35)
WHITE = (245, 250, 255)

PENGUIN_BLACK = (25, 30, 35)
PENGUIN_WHITE = (240, 245, 245)

ORANGE = (255, 165, 45)

RED = (225, 60, 60)
YELLOW = (245, 205, 60)
GREEN = (60, 210, 100)


# ============================================================
# PHYSICS
# ============================================================

GRAVITY = 900.0

WATER_LEVEL = 0.0

ICE_THICKNESS = 20.0
ICE_SIZE = 55.0

PENGUIN_RADIUS = 22.0

PLATFORM_HEIGHT = 180.0

SUPPORT_SNAP_SPEED = 15.0

FALL_LIMIT = -250.0


# ============================================================
# CAMERA
# ============================================================

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

CAMERA_SCALE = 1.0


def world_to_screen(x, y):

    return (
        int(CENTER_X + x * CAMERA_SCALE),
        int(CENTER_Y + y * CAMERA_SCALE)
    )


def screen_to_world(x, y):

    return (
        (x - CENTER_X) / CAMERA_SCALE,
        (y - CENTER_Y) / CAMERA_SCALE
    )


# ============================================================
# ICE BLOCK
# ============================================================

class IceBlock:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.size = ICE_SIZE

        # Height above water
        self.z = PLATFORM_HEIGHT

        # Vertical velocity
        self.vz = 0.0

        # Rotation
        self.angle = 0.0
        self.angular_velocity = 0.0

        self.mass = 1.0

        self.alive = True

        # Whether connected to a support pillar
        self.supported = False

        self.connections = []

        self.highlight = False

        # ====================================================
        # COLLATERAL DAMAGE
        #
        # 0 = no hits
        # 1 = hit once
        # 2 = hit twice -> FALL
        #
        # This has NO visual representation.
        # ====================================================

        self.damage = 0

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):

        if not self.alive:
            return

        # ====================================================
        # SUPPORTED ICE
        # ====================================================

        if self.supported:

            self.vz = 0.0

            difference = (
                PLATFORM_HEIGHT -
                self.z
            )

            self.z += (
                difference *
                min(
                    1.0,
                    SUPPORT_SNAP_SPEED * dt
                )
            )

            # Stop spinning when supported
            self.angular_velocity *= 0.90

        # ====================================================
        # FALLING ICE
        # ====================================================

        else:

            # Gravity
            self.vz -= (
                GRAVITY *
                dt
            )

            # Fall downward
            self.z += (
                self.vz *
                dt
            )

            # Air resistance
            self.angular_velocity *= 0.995

            # Continue rotation
            self.angle += (
                self.angular_velocity *
                dt
            )

        # ====================================================
        # ROTATION
        # ====================================================

        if self.supported:

            self.angle += (
                self.angular_velocity *
                dt
            )

        # ====================================================
        # REMOVE AFTER FALLING FAR ENOUGH
        # ====================================================

        if self.z < FALL_LIMIT:

            self.alive = False

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):

        if not self.alive:
            return

        sx, sy = world_to_screen(
            self.x,
            self.y
        )

        # ----------------------------------------------------
        # Height-based visual scaling
        # ----------------------------------------------------

        scale = (
            1.0 +
            self.z * 0.001
        )

        scale = max(
            0.75,
            min(
                1.25,
                scale
            )
        )

        size = int(
            ICE_SIZE *
            scale
        )

        surface = pygame.Surface(
            (
                size + 12,
                size + 12
            ),
            pygame.SRCALPHA
        )

        # ====================================================
        # SHADOW
        # ====================================================

        shadow_offset = int(
            max(
                0,
                -self.z * 0.08
            )
        )

        pygame.draw.rect(
            surface,
            (
                15,
                70,
                110,
                80
            ),
            (
                6 + shadow_offset,
                6 + shadow_offset,
                size,
                size
            ),
            border_radius=8
        )

        # ====================================================
        # ICE
        # ====================================================

        pygame.draw.rect(
            surface,
            ICE,
            (
                6,
                6,
                size,
                size
            ),
            border_radius=8
        )

        pygame.draw.rect(
            surface,
            ICE_EDGE,
            (
                6,
                6,
                size,
                size
            ),
            3,
            border_radius=8
        )

        # ====================================================
        # NO CRACK VISUAL
        #
        # NO RED X
        #
        # Damage is invisible.
        # ====================================================

        # ====================================================
        # HIGHLIGHT
        # ====================================================

        if self.highlight:

            pygame.draw.rect(
                surface,
                YELLOW,
                (
                    4,
                    4,
                    size + 4,
                    size + 4
                ),
                3,
                border_radius=10
            )

        # ====================================================
        # ROTATION
        # ====================================================

        rotated = pygame.transform.rotate(
            surface,
            -math.degrees(
                self.angle
            )
        )

        screen.blit(
            rotated,
            (
                sx -
                rotated.get_width() // 2,

                sy -
                rotated.get_height() // 2
            )
        )


# ============================================================
# CONNECTION
# ============================================================

class Connection:

    def __init__(self, a, b):

        self.a = a
        self.b = b

        self.alive = True

    def draw(self):

        if not self.alive:
            return

        if (
            not self.a.alive
            or
            not self.b.alive
        ):
            return

        ax, ay = world_to_screen(
            self.a.x,
            self.a.y
        )

        bx, by = world_to_screen(
            self.b.x,
            self.b.y
        )

        pygame.draw.line(
            screen,
            ICE_EDGE,
            (ax, ay),
            (bx, by),
            3
        )


# ============================================================
# SUPPORT PILLAR
# ============================================================

class SupportPillar:

    def __init__(self, block):

        self.block = block

        self.x = block.x
        self.y = block.y

        self.height = PLATFORM_HEIGHT

    def supports(self):

        return self.block.alive


# ============================================================
# PENGUIN
# ============================================================

class Penguin:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.z = (
            PLATFORM_HEIGHT +
            ICE_THICKNESS +
            PENGUIN_RADIUS
        )

        self.vz = 0.0

        self.mass = 1.5

        self.alive = True

        self.support = None

    # ========================================================
    # FIND SUPPORT
    # ========================================================

    def find_support(self, blocks):

        best = None

        best_distance = float(
            "inf"
        )

        for block in blocks:

            if not block.alive:
                continue

            dx = (
                self.x -
                block.x
            )

            dy = (
                self.y -
                block.y
            )

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if (
                distance <
                block.size * 0.60
            ):

                if (
                    distance <
                    best_distance
                ):

                    best = block

                    best_distance = (
                        distance
                    )

        return best

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, blocks, dt):

        if not self.alive:
            return

        # Gravity

        self.vz -= (
            GRAVITY *
            dt
        )

        # Find ice below

        support = self.find_support(
            blocks
        )

        if support:

            ice_top = (
                support.z +
                ICE_THICKNESS / 2
            )

            penguin_bottom = (
                self.z -
                PENGUIN_RADIUS
            )

            # Landing

            if (
                penguin_bottom
                <= ice_top
                and
                self.vz < 0
            ):

                self.z = (
                    ice_top +
                    PENGUIN_RADIUS
                )

                self.vz = 0

                self.support = support

        else:

            self.support = None

        # Move

        self.z += (
            self.vz *
            dt
        )

        # Fell into water

        if self.z < -40:

            self.alive = False

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):

        if not self.alive:
            return

        sx, sy = world_to_screen(
            self.x,
            self.y
        )

        scale = (
            1.0 +
            self.z * 0.001
        )

        scale = max(
            0.7,
            min(
                1.25,
                scale
            )
        )

        radius = int(
            PENGUIN_RADIUS *
            scale
        )

        # Shadow

        pygame.draw.ellipse(
            screen,
            (
                15,
                75,
                115
            ),
            (
                sx - radius,
                sy - radius // 2,
                radius * 2,
                radius
            )
        )

        # Body

        pygame.draw.circle(
            screen,
            PENGUIN_BLACK,
            (
                sx,
                sy
            ),
            radius
        )

        # Belly

        pygame.draw.circle(
            screen,
            PENGUIN_WHITE,
            (
                sx,
                sy + int(
                    radius * 0.20
                )
            ),
            int(
                radius * 0.60
            )
        )

        # Eyes

        eye_offset = int(
            radius * 0.35
        )

        eye_radius = int(
            radius * 0.22
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                sx - eye_offset,
                sy - eye_offset
            ),
            eye_radius
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                sx + eye_offset,
                sy - eye_offset
            ),
            eye_radius
        )

        # Pupils

        pupil_radius = max(
            2,
            int(
                radius * 0.10
            )
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                sx - eye_offset,
                sy - eye_offset
            ),
            pupil_radius
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                sx + eye_offset,
                sy - eye_offset
            ),
            pupil_radius
        )

        # Beak

        pygame.draw.polygon(
            screen,
            ORANGE,
            [
                (
                    sx - int(
                        radius * 0.25
                    ),
                    sy
                ),
                (
                    sx + int(
                        radius * 0.25
                    ),
                    sy
                ),
                (
                    sx,
                    sy + int(
                        radius * 0.35
                    )
                )
            ]
        )

        # Feet

        pygame.draw.ellipse(
            screen,
            ORANGE,
            (
                sx - radius,
                sy + radius - 3,
                radius,
                int(
                    radius * 0.30
                )
            )
        )

        pygame.draw.ellipse(
            screen,
            ORANGE,
            (
                sx,
                sy + radius - 3,
                radius,
                int(
                    radius * 0.30
                )
            )
        )


# ============================================================
# CREATE LEVEL
# ============================================================

def create_level():

    blocks = []

    connections = []

    pillars = []

    rows = 7
    cols = 10

    spacing = 60

    start_x = (
        -(
            cols - 1
        ) *
        spacing /
        2
    )

    start_y = (
        -(
            rows - 1
        ) *
        spacing /
        2
    )

    grid = []

    # ========================================================
    # CREATE ICE BLOCKS
    # ========================================================

    for row in range(rows):

        row_blocks = []

        for col in range(cols):

            x = (
                start_x +
                col * spacing
            )

            y = (
                start_y +
                row * spacing
            )

            x += random.uniform(
                -2,
                2
            )

            y += random.uniform(
                -2,
                2
            )

            block = IceBlock(
                x,
                y
            )

            row_blocks.append(
                block
            )

            blocks.append(
                block
            )

        grid.append(
            row_blocks
        )

    # ========================================================
    # FOUR SUPPORT PILLARS
    # ========================================================

    corner_blocks = [

        grid[0][0],

        grid[0][cols - 1],

        grid[rows - 1][0],

        grid[rows - 1][cols - 1]

    ]

    for block in corner_blocks:

        pillars.append(
            SupportPillar(
                block
            )
        )

    # ========================================================
    # CONNECT NEIGHBORS
    # ========================================================

    for row in range(rows):

        for col in range(cols):

            current = grid[row][col]

            # Right

            if col < cols - 1:

                connection = Connection(
                    current,
                    grid[row][col + 1]
                )

                connections.append(
                    connection
                )

                current.connections.append(
                    connection
                )

                grid[row][col + 1].connections.append(
                    connection
                )

            # Down

            if row < rows - 1:

                connection = Connection(
                    current,
                    grid[row + 1][col]
                )

                connections.append(
                    connection
                )

                current.connections.append(
                    connection
                )

                grid[row + 1][col].connections.append(
                    connection
                )

    # ========================================================
    # PENGUIN
    # ========================================================

    center = grid[
        random.randint(
            1,
            rows - 2
        )
    ][
        random.randint(
            1,
            cols - 2
        )
    ]

    penguin = Penguin(
        center.x,
        center.y
    )

    return (
        blocks,
        connections,
        pillars,
        penguin
    )


# ============================================================
# STRUCTURAL SUPPORT
# ============================================================

def update_structural_support(
    blocks,
    connections,
    pillars
):

    # --------------------------------------------------------
    # Initially mark everything unsupported
    # --------------------------------------------------------

    for block in blocks:

        block.supported = False

    # --------------------------------------------------------
    # Start at the four pillars
    # --------------------------------------------------------

    queue = []

    for pillar in pillars:

        block = pillar.block

        if block.alive:

            block.supported = True

            queue.append(
                block
            )

    # --------------------------------------------------------
    # Spread through connections
    # --------------------------------------------------------

    while queue:

        current = queue.pop(0)

        for connection in current.connections:

            if not connection.alive:
                continue

            if (
                not connection.a.alive
                or
                not connection.b.alive
            ):
                continue

            if connection.a == current:

                neighbor = connection.b

            else:

                neighbor = connection.a

            if not neighbor.supported:

                neighbor.supported = True

                queue.append(
                    neighbor
                )


# ============================================================
# FIND ADJACENT BLOCKS
#
# ONLY DIRECTLY ADJACENT:
#
#             [X]
#
#        [X]  [B]  [X]
#
#             [X]
#
# NO DIAGONALS.
# ============================================================

def get_adjacent_blocks(block):

    adjacent_blocks = []

    ADJACENT_DISTANCE = 70

    ALIGNMENT_TOLERANCE = 15

    for other in blocks:

        if other == block:
            continue

        if not other.alive:
            continue

        if is_pillar_block(other):
            continue

        dx = abs(
            other.x -
            block.x
        )

        dy = abs(
            other.y -
            block.y
        )

        # Left / right

        horizontal = (
            dx < ADJACENT_DISTANCE
            and
            dy < ALIGNMENT_TOLERANCE
        )

        # Up / down

        vertical = (
            dy < ADJACENT_DISTANCE
            and
            dx < ALIGNMENT_TOLERANCE
        )

        if (
            horizontal
            or
            vertical
        ):

            adjacent_blocks.append(
                other
            )

    return adjacent_blocks


# ============================================================
# GAME STATE
# ============================================================

(
    blocks,
    connections,
    pillars,
    penguin
) = create_level()

ice_broken = 0

game_over = False

won = False


# ============================================================
# RESET
# ============================================================

def reset_game():

    global blocks
    global connections
    global pillars
    global penguin
    global ice_broken
    global game_over
    global won

    (
        blocks,
        connections,
        pillars,
        penguin
    ) = create_level()

    ice_broken = 0

    game_over = False

    won = False


# ============================================================
# FIND CLICKED BLOCK
# ============================================================

def get_clicked_block(
    mouse_x,
    mouse_y
):

    world_x, world_y = screen_to_world(
        mouse_x,
        mouse_y
    )

    closest = None

    closest_distance = float(
        "inf"
    )

    for block in blocks:

        if not block.alive:
            continue

        dx = (
            world_x -
            block.x
        )

        dy = (
            world_y -
            block.y
        )

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if (
            distance <
            block.size / 2
        ):

            if (
                distance <
                closest_distance
            ):

                closest = block

                closest_distance = (
                    distance
                )

    return closest


# ============================================================
# CHECK PILLAR
# ============================================================

def is_pillar_block(block):

    for pillar in pillars:

        if block == pillar.block:

            return True

    return False


# ============================================================
# START FALLING
#
# This is separated into its own function so both:
#
#   1. structurally unsupported blocks
#   2. blocks hit twice by collateral damage
#
# get exactly the same falling effect.
# ============================================================

def start_falling(block):

    if not block.alive:
        return

    block.supported = False

    # Start downward velocity

    if block.vz >= 0:

        block.vz = -50.0

    # Start rotation

    if abs(
        block.angular_velocity
    ) < 0.2:

        block.angular_velocity = random.uniform(
            -3.0,
            3.0
        )


# ============================================================
# BREAK ICE
#
# DIRECT CLICK:
#     Immediately disappears.
#
# COLLATERAL #1:
#     Remains normal.
#
# COLLATERAL #2:
#     Falls and rotates.
#     Does NOT disappear immediately.
# ============================================================

def break_ice(
    mouse_x,
    mouse_y
):

    global ice_broken

    block = get_clicked_block(
        mouse_x,
        mouse_y
    )

    if block is None:
        return

    # --------------------------------------------------------
    # Pillars cannot be directly destroyed
    # --------------------------------------------------------

    if is_pillar_block(block):
        return

    # --------------------------------------------------------
    # Find neighbors BEFORE removing the clicked block
    # --------------------------------------------------------

    adjacent_blocks = get_adjacent_blocks(
        block
    )

    # ========================================================
    # DIRECT CLICK
    #
    # Immediately destroy clicked block.
    # ========================================================

    block.alive = False

    block.supported = False

    ice_broken += 1

    # --------------------------------------------------------
    # Remove all connections to clicked block
    # --------------------------------------------------------

    for connection in connections:

        if (
            connection.a == block
            or
            connection.b == block
        ):

            connection.alive = False

    # ========================================================
    # COLLATERAL DAMAGE
    # ========================================================

    for neighbor in adjacent_blocks:

        if not neighbor.alive:
            continue

        if is_pillar_block(neighbor):
            continue

        # ----------------------------------------------------
        # Add one collateral hit
        # ----------------------------------------------------

        neighbor.damage += 1

        # ====================================================
        # SECOND HIT
        #
        # DO NOT DESTROY IT.
        #
        # MAKE IT FALL.
        # ====================================================

        if neighbor.damage >= 2:

            start_falling(
                neighbor
            )

            # ------------------------------------------------
            # IMPORTANT:
            #
            # We do NOT set:
            #
            #     neighbor.alive = False
            #
            # The block remains visible while falling.
            # ------------------------------------------------

            # Remove structural connections so it cannot
            # remain supported.

            for connection in connections:

                if (
                    connection.a == neighbor
                    or
                    connection.b == neighbor
                ):

                    connection.alive = False

    # ========================================================
    # RECALCULATE STRUCTURAL SUPPORT
    # ========================================================

    update_structural_support(
        blocks,
        connections,
        pillars
    )

    # ========================================================
    # ANY NEWLY UNSUPPORTED BLOCK FALLS
    # ========================================================

    for ice in blocks:

        if not ice.alive:
            continue

        if not ice.supported:

            start_falling(
                ice
            )


# ============================================================
# WATER
# ============================================================

def draw_water():

    screen.fill(
        WATER
    )

    for y in range(
        10,
        HEIGHT,
        45
    ):

        for x in range(
            10,
            WIDTH,
            70
        ):

            pygame.draw.arc(
                screen,
                WATER_LIGHT,
                (
                    x,
                    y,
                    35,
                    12
                ),
                0,
                math.pi,
                2
            )


# ============================================================
# PILLAR INDICATOR
# ============================================================

def draw_pillar_indicator(
    pillar
):

    sx, sy = world_to_screen(
        pillar.x,
        pillar.y
    )

    pygame.draw.circle(
        screen,
        (
            25,
            100,
            150
        ),
        (
            sx,
            sy
        ),
        5
    )


# ============================================================
# HUD
# ============================================================

font = pygame.font.SysFont(
    "Arial",
    28,
    bold=True
)

small_font = pygame.font.SysFont(
    "Arial",
    18
)


def draw_hud():

    text = font.render(
        f"Ice Broken: {ice_broken}",
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            20,
            20
        )
    )

    instruction = small_font.render(
        "Click ice blocks to break them",
        True,
        WHITE
    )

    screen.blit(
        instruction,
        (
            20,
            58
        )
    )

    controls = small_font.render(
        "R = Restart    ESC = Quit",
        True,
        WHITE
    )

    screen.blit(
        controls,
        (
            20,
            82
        )
    )

    physics = small_font.render(
        "1 hit = normal    2 hits = falls",
        True,
        WHITE
    )

    screen.blit(
        physics,
        (
            20,
            HEIGHT - 30
        )
    )


# ============================================================
# GAME OVER
# ============================================================

def draw_game_over():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            0,
            0,
            0,
            130
        )
    )

    screen.blit(
        overlay,
        (
            0,
            0
        )
    )

    if won:

        message = "PENGUIN SAVED!"

        color = GREEN

    else:

        message = "PENGUIN FELL!"

        color = RED

    text = font.render(
        message,
        True,
        color
    )

    screen.blit(
        text,
        (
            WIDTH // 2 -
            text.get_width() // 2,

            HEIGHT // 2 -
            30
        )
    )

    restart = small_font.render(
        "Press R to restart",
        True,
        WHITE
    )

    screen.blit(
        restart,
        (
            WIDTH // 2 -
            restart.get_width() // 2,

            HEIGHT // 2 +
            20
        )
    )


# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    # --------------------------------------------------------
    # DELTA TIME
    # --------------------------------------------------------

    dt = clock.tick(
        FPS
    ) / 1000.0

    dt = min(
        dt,
        0.02
    )

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        if event.type == pygame.QUIT:

            running = False

        # ====================================================
        # KEYBOARD
        # ====================================================

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            elif event.key == pygame.K_r:

                reset_game()

        # ====================================================
        # MOUSE
        # ====================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if (
                event.button == 1
                and
                not game_over
            ):

                mouse_x, mouse_y = (
                    pygame.mouse.get_pos()
                )

                break_ice(
                    mouse_x,
                    mouse_y
                )

    # ========================================================
    # UPDATE
    # ========================================================

    if not game_over:

        # ----------------------------------------------------
        # Recalculate support
        # ----------------------------------------------------

        update_structural_support(
            blocks,
            connections,
            pillars
        )

        # ----------------------------------------------------
        # Ice physics
        # ----------------------------------------------------

        for block in blocks:

            block.update(
                dt
            )

        # ----------------------------------------------------
        # Penguin physics
        # ----------------------------------------------------

        penguin.update(
            blocks,
            dt
        )

        # ----------------------------------------------------
        # Penguin fell
        # ----------------------------------------------------

        if not penguin.alive:

            game_over = True

            won = False

        # ----------------------------------------------------
        # Win condition
        # ----------------------------------------------------

        alive_count = sum(
            1
            for block in blocks
            if block.alive
        )

        if (
            penguin.alive
            and
            alive_count <= 20
        ):

            game_over = True

            won = True

    # ========================================================
    # DRAW
    # ========================================================

    draw_water()

    # --------------------------------------------------------
    # Pillars
    # --------------------------------------------------------

    for pillar in pillars:

        draw_pillar_indicator(
            pillar
        )

    # --------------------------------------------------------
    # Connections
    # --------------------------------------------------------

    for connection in connections:

        connection.draw()

    # --------------------------------------------------------
    # Ice
    # --------------------------------------------------------

    for block in blocks:

        block.draw()

    # --------------------------------------------------------
    # Penguin
    # --------------------------------------------------------

    penguin.draw()

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    draw_hud()

    # --------------------------------------------------------
    # Game over
    # --------------------------------------------------------

    if game_over:

        draw_game_over()

    # --------------------------------------------------------
    # Update display
    # --------------------------------------------------------

    pygame.display.flip()


pygame.quit()