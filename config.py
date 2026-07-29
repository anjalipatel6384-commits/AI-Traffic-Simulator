import pygame

pygame.init()

# ==========================================================
# SCREEN SETTINGS
# ==========================================================

WIDTH = 1200
HEIGHT = 800

FPS = 60

TITLE = "AI Smart Traffic Signal Simulator"

# ==========================================================
# ROAD SETTINGS
# ==========================================================

ROAD_WIDTH = 180
LANE_WIDTH = ROAD_WIDTH // 2

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

STOP_DISTANCE = 120
SAFE_DISTANCE = 70

# ==========================================================
# VEHICLE SPEEDS
# ==========================================================

CAR_SPEED = 3.0
BUS_SPEED = 2.3
TRUCK_SPEED = 2.0
BIKE_SPEED = 3.8
AMBULANCE_SPEED = 4.5

ACCELERATION = 0.08
BRAKE_FORCE = 0.18

# ==========================================================
# SIGNAL SETTINGS
# ==========================================================

DEFAULT_GREEN = 15
MIN_GREEN = 10
MAX_GREEN = 45

YELLOW_TIME = 3

# ==========================================================
# TRAFFIC SETTINGS
# ==========================================================

SPAWN_DELAY = 35

LOW_TRAFFIC = 5
MEDIUM_TRAFFIC = 10
HIGH_TRAFFIC = 15

AI_MODE = True

# ==========================================================
# COLORS
# ==========================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (220, 40, 40)
GREEN = (40, 220, 40)
YELLOW = (255, 210, 0)

BLUE = (50, 140, 255)

GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
LIGHT_GRAY = (180, 180, 180)

ROAD_COLOR = (55, 55, 55)
GRASS = (35, 140, 60)

SKY = (170, 220, 255)

ORANGE = (255, 150, 0)

# ==========================================================
# DASHBOARD
# ==========================================================

PANEL_COLOR = (35, 35, 35)
PANEL_BORDER = (0, 200, 255)

TEXT_COLOR = WHITE

# ==========================================================
# RAIN
# ==========================================================

RAIN_SPEED_FACTOR = 0.70

# ==========================================================
# NIGHT
# ==========================================================

NIGHT_BACKGROUND = (20, 25, 40)

# ==========================================================
# FONTS
# ==========================================================

pygame.font.init()

FONT_SMALL = pygame.font.SysFont("Arial", 18)

FONT = pygame.font.SysFont("Arial", 22)

FONT_BIG = pygame.font.SysFont(
    "Arial",
    30,
    bold=True
)

# ==========================================================
# GAME SETTINGS
# ==========================================================

SHOW_FPS = True

ENABLE_SHADOWS = True

ENABLE_HEADLIGHTS = True

ENABLE_AI = True