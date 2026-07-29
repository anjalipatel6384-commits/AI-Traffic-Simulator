import pygame
import random

from config import *


class Vehicle:

    def __init__(self, direction):

        self.direction = direction

        # =====================================
        # Vehicle Type
        # =====================================

        self.vehicle_type = random.choices(
            ["CAR", "BUS", "TRUCK", "BIKE", "AMBULANCE"],
            weights=[60, 15, 10, 13, 2]
        )[0]

        # =====================================
        # Vehicle Properties
        # =====================================

        if self.vehicle_type == "CAR":

            self.width = 24
            self.height = 42
            self.max_speed = CAR_SPEED

            self.color = random.choice([
                (255, 0, 0),
                (0, 120, 255),
                (255, 200, 0),
                (40, 220, 40),
                (255, 120, 180),
                (170, 170, 170)
            ])

        elif self.vehicle_type == "BUS":

            self.width = 30
            self.height = 72
            self.max_speed = BUS_SPEED
            self.color = (255, 160, 0)

        elif self.vehicle_type == "TRUCK":

            self.width = 32
            self.height = 78
            self.max_speed = TRUCK_SPEED
            self.color = (120, 120, 120)

        elif self.vehicle_type == "BIKE":

            self.width = 16
            self.height = 30
            self.max_speed = BIKE_SPEED
            self.color = (40, 40, 40)

        else:

            self.width = 26
            self.height = 46
            self.max_speed = AMBULANCE_SPEED
            self.color = WHITE

        self.emergency = (
            self.vehicle_type == "AMBULANCE"
        )

        # =====================================
        # Movement
        # =====================================

        self.current_speed = 0.0
        self.target_speed = self.max_speed

        self.acceleration = ACCELERATION
        self.brake_force = BRAKE_FORCE

        # Vehicle has crossed the intersection
        self.passed = False

        # Vehicle has entered the intersection
        self.in_intersection = False

        self.night_mode = False
        self.rain_mode = False

        # =====================================
        # Spawn Position
        # =====================================

        if direction == "DOWN":

            self.x = CENTER_X - 45
            self.y = -120

        elif direction == "UP":

            self.x = CENTER_X + 20
            self.y = HEIGHT + 120

        elif direction == "RIGHT":

            self.x = -120
            self.y = CENTER_Y + 20

        else:

            self.x = WIDTH + 120
            self.y = CENTER_Y - 45

        # =====================================
        # Collision Rectangle
        # =====================================

        self.update_rect()

    # =====================================
    # Update Collision Rectangle
    # =====================================

    def update_rect(self):

        if self.direction in ("LEFT", "RIGHT"):

            self.rect = pygame.Rect(
                round(self.x),
                round(self.y),
                self.height,
                self.width
            )

        else:

            self.rect = pygame.Rect(
                round(self.x),
                round(self.y),
                self.width,
                self.height
            )

    # =====================================
    # Intersection Area
    # =====================================

    def is_in_intersection(self):

        intersection_left = (
            CENTER_X - ROAD_WIDTH // 2
        )

        intersection_right = (
            CENTER_X + ROAD_WIDTH // 2
        )

        intersection_top = (
            CENTER_Y - ROAD_WIDTH // 2
        )

        intersection_bottom = (
            CENTER_Y + ROAD_WIDTH // 2
        )

        return (
            self.rect.right > intersection_left
            and self.rect.left < intersection_right
            and self.rect.bottom > intersection_top
            and self.rect.top < intersection_bottom
        )

    # =====================================
    # Distance From Stop Line
    # =====================================

    def distance_to_stop_line(self):

        half_road = ROAD_WIDTH // 2

        if self.direction == "DOWN":

            stop_line = (
                CENTER_Y - half_road - 8
            )

            return stop_line - self.rect.bottom

        elif self.direction == "UP":

            stop_line = (
                CENTER_Y + half_road + 8
            )

            return self.rect.top - stop_line

        elif self.direction == "RIGHT":

            stop_line = (
                CENTER_X - half_road - 8
            )

            return stop_line - self.rect.right

        else:

            stop_line = (
                CENTER_X + half_road + 8
            )

            return self.rect.left - stop_line

    # =====================================
    # Near Signal
    # =====================================

    def near_signal(self):

        distance = self.distance_to_stop_line()

        return distance <= 90

    # =====================================
    # Find Front Vehicle Gap
    # =====================================

    def front_vehicle_gap(self, vehicles):

        closest_gap = None

        for other in vehicles:

            if other is self:
                continue

            # Only same lane
            if other.direction != self.direction:
                continue

            if self.direction == "DOWN":

                if other.rect.top >= self.rect.bottom:

                    gap = (
                        other.rect.top
                        - self.rect.bottom
                    )

                else:
                    continue

            elif self.direction == "UP":

                if other.rect.bottom <= self.rect.top:

                    gap = (
                        self.rect.top
                        - other.rect.bottom
                    )

                else:
                    continue

            elif self.direction == "RIGHT":

                if other.rect.left >= self.rect.right:

                    gap = (
                        other.rect.left
                        - self.rect.right
                    )

                else:
                    continue

            else:

                if other.rect.right <= self.rect.left:

                    gap = (
                        self.rect.left
                        - other.rect.right
                    )

                else:
                    continue

            if closest_gap is None or gap < closest_gap:

                closest_gap = gap

        return closest_gap

    # =====================================
    # Safe Distance Check
    # =====================================

    def check_distance(self, vehicles):

        gap = self.front_vehicle_gap(vehicles)

        if gap is None:

            return True

        safe_gap = SAFE_DISTANCE

        # Larger vehicles need more room
        if self.vehicle_type == "BUS":

            safe_gap += 25

        elif self.vehicle_type == "TRUCK":

            safe_gap += 30

        elif self.vehicle_type == "AMBULANCE":

            safe_gap += 10

        return gap >= safe_gap

    # =====================================
    # Traffic Signal Handling
    # =====================================

    def handle_signal(self, signal):

        # Normal speed by default
        self.target_speed = self.max_speed

        # =================================
        # RED
        # =================================

        if signal.is_red():

            # IMPORTANT:
            # Once inside intersection,
            # vehicle must finish crossing.
            if not self.in_intersection:

                distance = self.distance_to_stop_line()

                if distance <= 100:

                    self.target_speed = 0

        # =================================
        # YELLOW
        # =================================

        elif signal.is_yellow():

            # Yellow = slow down,
            # NOT complete stop.
            self.target_speed = (
                self.max_speed * 0.45
            )

        # =================================
        # GREEN
        # =================================

        elif signal.is_green():

            self.target_speed = self.max_speed

        # =================================
        # Rain
        # =================================

        if self.rain_mode:

            self.target_speed *= RAIN_SPEED_FACTOR

    # =====================================
    # Smooth Speed Control
    # =====================================

    def update_speed(self):

        if self.current_speed < self.target_speed:

            self.current_speed += self.acceleration

            if self.current_speed > self.target_speed:

                self.current_speed = self.target_speed

        elif self.current_speed > self.target_speed:

            self.current_speed -= self.brake_force

            if self.current_speed < self.target_speed:

                self.current_speed = self.target_speed

    # =====================================
    # Calculate Maximum Safe Movement
    # =====================================

    def safe_movement(self, vehicles):

        movement = self.current_speed

        gap = self.front_vehicle_gap(vehicles)

        if gap is None:

            return movement

        safe_gap = SAFE_DISTANCE

        if self.vehicle_type == "BUS":

            safe_gap += 25

        elif self.vehicle_type == "TRUCK":

            safe_gap += 30

        elif self.vehicle_type == "AMBULANCE":

            safe_gap += 10

        available = gap - safe_gap

        if available <= 0:

            return 0

        return min(
            movement,
            available
        )

    # =====================================
    # Prevent Crossing Red Stop Line
    # =====================================

    def safe_signal_movement(self, movement, signal):

        # Green / yellow can continue
        if not signal.is_red():

            return movement

        # Already inside intersection:
        # allow vehicle to clear it.
        if self.in_intersection:

            return movement

        distance = self.distance_to_stop_line()

        # Already safely before stop line
        if distance > 0:

            return min(
                movement,
                distance
            )

        # Do not move further into red
        return 0

    # =====================================
    # Move Vehicle
    # =====================================

    def move(self, signal, vehicles):

        # ---------------------------------
        # Signal
        # ---------------------------------

        self.handle_signal(signal)

        # ---------------------------------
        # Vehicle ahead
        # ---------------------------------

        if not self.check_distance(vehicles):

            self.target_speed = 0

        # ---------------------------------
        # Smooth speed
        # ---------------------------------

        self.update_speed()

        # ---------------------------------
        # Safe movement
        # ---------------------------------

        move_speed = self.safe_movement(
            vehicles
        )

        # ---------------------------------
        # Red stop-line protection
        # ---------------------------------

        move_speed = self.safe_signal_movement(
            move_speed,
            signal
        )

        # =================================
        # Move
        # =================================

        if self.direction == "DOWN":

            self.y += move_speed

        elif self.direction == "UP":

            self.y -= move_speed

        elif self.direction == "RIGHT":

            self.x += move_speed

        elif self.direction == "LEFT":

            self.x -= move_speed

        # Update collision rectangle
        self.update_rect()

        # =================================
        # Intersection Status
        # =================================

        if self.is_in_intersection():

            self.in_intersection = True

        # =================================
        # Passed Intersection
        # =================================

        half_road = ROAD_WIDTH // 2

        if self.direction == "DOWN":

            if self.rect.top > CENTER_Y + half_road:

                self.passed = True

        elif self.direction == "UP":

            if self.rect.bottom < CENTER_Y - half_road:

                self.passed = True

        elif self.direction == "RIGHT":

            if self.rect.left > CENTER_X + half_road:

                self.passed = True

        elif self.direction == "LEFT":

            if self.rect.right < CENTER_X - half_road:

                self.passed = True

    # =====================================
    # Off Screen
    # =====================================

    def is_off_screen(self):

        if self.direction == "DOWN":

            return self.y > HEIGHT + 150

        elif self.direction == "UP":

            return self.y < -150

        elif self.direction == "RIGHT":

            return self.x > WIDTH + 150

        elif self.direction == "LEFT":

            return self.x < -150

        return False

    # =====================================
    # Draw Vehicle
    # =====================================

    def draw(self, screen):

        # ---------------------------------
        # Shadow
        # ---------------------------------

        if ENABLE_SHADOWS:

            if self.direction in ("LEFT", "RIGHT"):

                shadow = pygame.Rect(
                    round(self.x + 3),
                    round(self.y + 3),
                    self.height,
                    self.width
                )

            else:

                shadow = pygame.Rect(
                    round(self.x + 3),
                    round(self.y + 3),
                    self.width,
                    self.height
                )

            pygame.draw.rect(
                screen,
                (30, 30, 30),
                shadow,
                border_radius=6
            )

        # ---------------------------------
        # Body
        # ---------------------------------

        if self.direction in ("LEFT", "RIGHT"):

            body = pygame.Rect(
                round(self.x),
                round(self.y),
                self.height,
                self.width
            )

        else:

            body = pygame.Rect(
                round(self.x),
                round(self.y),
                self.width,
                self.height
            )

        pygame.draw.rect(
            screen,
            self.color,
            body,
            border_radius=6
        )

        # ---------------------------------
        # Windows
        # ---------------------------------

        if self.direction in ("UP", "DOWN"):

            window = pygame.Rect(
                body.x + 4,
                body.y + 6,
                max(4, body.width - 8),
                max(4, body.height // 3)
            )

        else:

            window = pygame.Rect(
                body.x + 6,
                body.y + 4,
                max(4, body.width // 3),
                max(4, body.height - 8)
            )

        pygame.draw.rect(
            screen,
            SKY,
            window,
            border_radius=3
        )

        # ---------------------------------
        # Wheels
        # ---------------------------------

        if self.direction in ("UP", "DOWN"):

            wheels = [
                (
                    body.left + 4,
                    body.top + 8
                ),
                (
                    body.right - 4,
                    body.top + 8
                ),
                (
                    body.left + 4,
                    body.bottom - 8
                ),
                (
                    body.right - 4,
                    body.bottom - 8
                )
            ]

        else:

            wheels = [
                (
                    body.left + 8,
                    body.top + 4
                ),
                (
                    body.left + 8,
                    body.bottom - 4
                ),
                (
                    body.right - 8,
                    body.top + 4
                ),
                (
                    body.right - 8,
                    body.bottom - 4
                )
            ]

        for wheel in wheels:

            pygame.draw.circle(
                screen,
                BLACK,
                wheel,
                3
            )

        # ---------------------------------
        # Ambulance Cross
        # ---------------------------------

        if self.emergency:

            pygame.draw.line(
                screen,
                RED,
                (
                    body.centerx,
                    body.top + 6
                ),
                (
                    body.centerx,
                    body.bottom - 6
                ),
                3
            )

            pygame.draw.line(
                screen,
                RED,
                (
                    body.left + 6,
                    body.centery
                ),
                (
                    body.right - 6,
                    body.centery
                ),
                3
            )

        # ---------------------------------
        # Headlights
        # ---------------------------------

        if ENABLE_HEADLIGHTS and self.night_mode:

            light_color = (
                255,
                255,
                180
            )

            if self.direction == "DOWN":

                pygame.draw.circle(
                    screen,
                    light_color,
                    (
                        body.centerx,
                        body.bottom
                    ),
                    5
                )

            elif self.direction == "UP":

                pygame.draw.circle(
                    screen,
                    light_color,
                    (
                        body.centerx,
                        body.top
                    ),
                    5
                )

            elif self.direction == "RIGHT":

                pygame.draw.circle(
                    screen,
                    light_color,
                    (
                        body.right,
                        body.centery
                    ),
                    5
                )

            elif self.direction == "LEFT":

                pygame.draw.circle(
                    screen,
                    light_color,
                    (
                        body.left,
                        body.centery
                    ),
                    5
                )