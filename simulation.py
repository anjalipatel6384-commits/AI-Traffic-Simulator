import pygame

import random


from config import *

from traffic_signal import TrafficSignal

from vehicles import Vehicle



class Simulation:


    def __init__(self):


        pygame.init()


        # =====================================

        # Window

        # =====================================


        self.screen = pygame.display.set_mode(

            (WIDTH, HEIGHT)

        )


        pygame.display.set_caption(TITLE)


        self.clock = pygame.time.Clock()


        self.running = True


        # =====================================

        # Modes

        # =====================================


        self.ai_mode = ENABLE_AI


        self.night_mode = False


        self.rain_mode = False


        # =====================================

        # Vehicle List

        # =====================================


        self.vehicles = []


        self.spawn_timer = 0


        self.spawn_delay = SPAWN_DELAY


        # =====================================

        # Statistics

        # =====================================


        self.total_spawned = 0


        self.total_passed = 0


        self.total_waiting = 0


        # =====================================

        # Traffic Queue

        # =====================================


        self.north_queue = 0


        self.south_queue = 0


        self.east_queue = 0


        self.west_queue = 0


        self.traffic_status = "LOW"


        self.ai_reason = "Waiting..."


        # =====================================

        # Signal Controller

        # =====================================


        self.current_phase = "NS"


        self.signal_state = "GREEN"


        self.green_time = DEFAULT_GREEN


        self.signal_timer = 0


        self.yellow_timer = 0

                # =====================================

        # Traffic Signals

        # =====================================


        self.north_signal = TrafficSignal(

            CENTER_X - 40,

            CENTER_Y - 130

        )


        self.south_signal = TrafficSignal(

            CENTER_X + 40,

            CENTER_Y + 130

        )


        self.east_signal = TrafficSignal(

            CENTER_X + 130,

            CENTER_Y - 40

        )


        self.west_signal = TrafficSignal(

            CENTER_X - 130,

            CENTER_Y + 40

        )


        # =====================================

        # Emergency Vehicle

        # =====================================


        self.emergency_mode = False


        self.emergency_direction = None


        # =====================================

        # AI History

        # =====================================


        self.history = []


        self.max_history = 50


        # =====================================

        # Rain Effect

        # =====================================


        self.raindrops = []


        for _ in range(150):


            self.raindrops.append([


                random.randint(0, WIDTH),


                random.randint(0, HEIGHT),


                random.randint(10, 20)


            ])


        # =====================================

        # FPS Counter

        # =====================================


        self.show_fps = SHOW_FPS


        # =====================================

        # AI Decision

        # =====================================


        self.ai_phase = "NS"


        self.ai_green_time = DEFAULT_GREEN


        # =====================================

        # Finish Initialization

        # =====================================


        print("===================================")

        print(" AI Smart Traffic Simulator Started ")

        print("===================================")

    # =====================================

    # Draw Background

    # =====================================


    def draw_background(self):


        # Background


        if self.night_mode:

            self.screen.fill(NIGHT_BACKGROUND)

        else:

            self.screen.fill(GRASS)


        # =====================================

        # Horizontal Road

        # =====================================


        pygame.draw.rect(

            self.screen,

            ROAD_COLOR,

            (

                0,

                CENTER_Y - ROAD_WIDTH // 2,

                WIDTH,

                ROAD_WIDTH

            )

        )


        # =====================================

        # Vertical Road

        # =====================================


        pygame.draw.rect(

            self.screen,

            ROAD_COLOR,

            (

                CENTER_X - ROAD_WIDTH // 2,

                0,

                ROAD_WIDTH,

                HEIGHT

            )

        )


        # =====================================

        # Center Junction

        # =====================================


        pygame.draw.rect(

            self.screen,

            DARK_GRAY,

            (

                CENTER_X - ROAD_WIDTH // 2,

                CENTER_Y - ROAD_WIDTH // 2,

                ROAD_WIDTH,

                ROAD_WIDTH

            )

        )


        # =====================================

        # Lane Markings

        # =====================================


        for x in range(0, WIDTH, 40):


            pygame.draw.rect(

                self.screen,

                WHITE,

                (

                    x,

                    CENTER_Y - 2,

                    20,

                    4

                )

            )


        for y in range(0, HEIGHT, 40):


            pygame.draw.rect(

                self.screen,

                WHITE,

                (

                    CENTER_X - 2,

                    y,

                    4,

                    20

                )

            )


        # =====================================

        # Zebra Crossing

        # =====================================


        for x in range(CENTER_X - 70, CENTER_X + 70, 18):


            pygame.draw.rect(

                self.screen,

                WHITE,

                (

                    x,

                    CENTER_Y - 100,

                    10,

                    30

                )

            )


            pygame.draw.rect(

                self.screen,

                WHITE,

                (

                    x,

                    CENTER_Y + 70,

                    10,

                    30

                )

            )


        for y in range(CENTER_Y - 70, CENTER_Y + 70, 18):


            pygame.draw.rect(

                self.screen,

                WHITE,

                (

                    CENTER_X - 100,

                    y,

                    30,

                    10

                )

            )


            pygame.draw.rect(

                self.screen,

                WHITE,

                (

                    CENTER_X + 70,

                    y,

                    30,

                    10

                )

            )


        # =====================================

        # Road Labels

        # =====================================


        labels = [


            ("NORTH", CENTER_X - 30, 20),


            ("SOUTH", CENTER_X - 30, HEIGHT - 40),


            ("WEST", 20, CENTER_Y - 30),


            ("EAST", WIDTH - 80, CENTER_Y - 30)


        ]


        for text, x, y in labels:


            img = FONT_SMALL.render(

                text,

                True,

                WHITE

            )


            self.screen.blit(img, (x, y))


        # =====================================

        # Rain Animation

        # =====================================


        if self.rain_mode:


            for drop in self.raindrops:


                pygame.draw.line(

                    self.screen,

                    (170, 220, 255),

                    (drop[0], drop[1]),

                    (drop[0] + 3, drop[1] + 10),

                    1

                )


                drop[1] += drop[2]


                if drop[1] > HEIGHT:


                    drop[0] = random.randint(0, WIDTH)

                    drop[1] = -20

                        # =====================================

    # Update Traffic Signals (AI Brain)

    # =====================================


    def update_signals(self):


        # -----------------------------

        # Count Vehicles

        # -----------------------------


        self.north_queue = 0

        self.south_queue = 0

        self.east_queue = 0

        self.west_queue = 0


        for vehicle in self.vehicles:


            if vehicle.direction == "DOWN":

                self.north_queue += 1


            elif vehicle.direction == "UP":

                self.south_queue += 1


            elif vehicle.direction == "RIGHT":

                self.west_queue += 1


            elif vehicle.direction == "LEFT":

                self.east_queue += 1


        # -----------------------------

        # Emergency Vehicle Priority

        # -----------------------------


        self.emergency_mode = False


        for vehicle in self.vehicles:


            if vehicle.emergency and vehicle.near_signal():


                self.emergency_mode = True

                self.emergency_direction = vehicle.direction

                break


        if self.emergency_mode:


            if self.emergency_direction in ["UP", "DOWN"]:

                self.current_phase = "NS"

            else:

                self.current_phase = "EW"


        # -----------------------------

        # AI Decision

        # -----------------------------


        elif self.ai_mode:


            ns = self.north_queue + self.south_queue

            ew = self.east_queue + self.west_queue


            if ns >= ew:


                self.ai_phase = "NS"


            else:


                self.ai_phase = "EW"


            total = ns + ew


            if total >= HIGH_TRAFFIC:


                self.green_time = MAX_GREEN

                self.traffic_status = "HIGH"


            elif total >= MEDIUM_TRAFFIC:


                self.green_time = 30

                self.traffic_status = "MEDIUM"


            else:


                self.green_time = DEFAULT_GREEN

                self.traffic_status = "LOW"


        # -----------------------------

        # Timer

        # -----------------------------


        self.signal_timer += 1


        # GREEN → YELLOW


        if self.signal_state == "GREEN":


            if self.signal_timer >= self.green_time * FPS:


                self.signal_state = "YELLOW"

                self.signal_timer = 0


        # YELLOW → NEXT PHASE


        else:


            if self.signal_timer >= YELLOW_TIME * FPS:


                self.signal_state = "GREEN"

                self.signal_timer = 0


                if self.emergency_mode:


                    pass


                else:


                    self.current_phase = self.ai_phase


        # -----------------------------

        # Countdown

        # -----------------------------


        remaining = max(

            0,

            self.green_time -

            (self.signal_timer // FPS)

        )


        self.north_signal.timer = remaining

        self.south_signal.timer = remaining

        self.east_signal.timer = remaining

        self.west_signal.timer = remaining


        # -----------------------------

        # Apply Signal States

        # -----------------------------


        if self.signal_state == "GREEN":


            if self.current_phase == "NS":


                self.north_signal.set_state("GREEN")

                self.south_signal.set_state("GREEN")


                self.east_signal.set_state("RED")

                self.west_signal.set_state("RED")


            else:


                self.east_signal.set_state("GREEN")

                self.west_signal.set_state("GREEN")


                self.north_signal.set_state("RED")

                self.south_signal.set_state("RED")


        else:


            if self.current_phase == "NS":


                self.north_signal.set_state("YELLOW")

                self.south_signal.set_state("YELLOW")


                self.east_signal.set_state("RED")

                self.west_signal.set_state("RED")


            else:


                self.east_signal.set_state("YELLOW")

                self.west_signal.set_state("YELLOW")


                self.north_signal.set_state("RED")

                self.south_signal.set_state("RED")

                    # =====================================

    # Spawn Vehicles

    # =====================================


    def spawn_vehicle(self):


        self.spawn_timer += 1


        if self.spawn_timer < self.spawn_delay:

            return


        self.spawn_timer = 0


        direction = random.choice([

            "DOWN",

            "UP",

            "RIGHT",

            "LEFT"

        ])


        vehicle = Vehicle(direction)


        # Apply current modes

        vehicle.night_mode = self.night_mode

        vehicle.rain_mode = self.rain_mode


        # Don't spawn if another vehicle is too close

        for other in self.vehicles:


            if other.direction != direction:

                continue


            if direction == "DOWN":


                if abs(other.y - vehicle.y) < SAFE_DISTANCE + 50:

                    return


            elif direction == "UP":


                if abs(other.y - vehicle.y) < SAFE_DISTANCE + 50:

                    return


            elif direction == "RIGHT":


                if abs(other.x - vehicle.x) < SAFE_DISTANCE + 50:

                    return


            elif direction == "LEFT":


                if abs(other.x - vehicle.x) < SAFE_DISTANCE + 50:

                    return


        self.vehicles.append(vehicle)

        self.total_spawned += 1

    # =====================================
    # Update Vehicles
    # =====================================

    def update_vehicles(self):

        for vehicle in self.vehicles[:]:

            # Select signal
            if vehicle.direction == "DOWN":

                signal = self.north_signal

            elif vehicle.direction == "UP":

                signal = self.south_signal

            elif vehicle.direction == "RIGHT":

                signal = self.west_signal

            else:

                signal = self.east_signal

            # Apply current modes
            vehicle.night_mode = self.night_mode
            vehicle.rain_mode = self.rain_mode

            # Move vehicle
            vehicle.move(
                signal,
                self.vehicles
            )

            # Mark vehicle as passed after it crosses
            # the intersection center
            if vehicle.direction == "DOWN":

                if vehicle.y > CENTER_Y + STOP_DISTANCE:
                    vehicle.passed = True

            elif vehicle.direction == "UP":

                if vehicle.y < CENTER_Y - STOP_DISTANCE:
                    vehicle.passed = True

            elif vehicle.direction == "RIGHT":

                if vehicle.x > CENTER_X + STOP_DISTANCE:
                    vehicle.passed = True

            elif vehicle.direction == "LEFT":

                if vehicle.x < CENTER_X - STOP_DISTANCE:
                    vehicle.passed = True

            # Remove vehicle after it leaves the screen
            if vehicle.is_off_screen():

                self.total_passed += 1

                self.vehicles.remove(vehicle)


    # =====================================

    # Draw Vehicles

    # =====================================


    def draw_vehicles(self):


        for vehicle in self.vehicles:


            vehicle.draw(self.screen)


    # =====================================

    # Draw Signals

    # =====================================


    def draw_signals(self):


        self.north_signal.draw(self.screen)

        self.south_signal.draw(self.screen)

        self.east_signal.draw(self.screen)

        self.west_signal.draw(self.screen)

    # =====================================

    # Draw Dashboard

    # =====================================


    def draw_dashboard(self):


        panel = pygame.Rect(

            15,

            15,

            360,

            430

        )


        pygame.draw.rect(

            self.screen,

            PANEL_COLOR,

            panel,

            border_radius=12

        )


        pygame.draw.rect(

            self.screen,

            PANEL_BORDER,

            panel,

            2,

            border_radius=12

        )


        remaining = max(

            0,

            self.green_time -

            (self.signal_timer // FPS)

        )


        data = [


            "AI SMART TRAFFIC",


            "",


            f"Signal : {self.signal_state}",


            f"Phase : {self.current_phase}",


            f"Next Phase : {self.ai_phase}",


            f"Countdown : {remaining}s",


            "",


            f"North : {self.north_queue}",


            f"South : {self.south_queue}",


            f"East : {self.east_queue}",


            f"West : {self.west_queue}",


            "",


            f"Traffic : {self.traffic_status}",


            f"Green Time : {self.green_time}s",


            "",


            f"Spawned : {self.total_spawned}",


            f"Passed : {self.total_passed}",


            f"Vehicles : {len(self.vehicles)}",


            "",


            f"Night : {'ON' if self.night_mode else 'OFF'}",


            f"Rain : {'ON' if self.rain_mode else 'OFF'}",


            f"Emergency : {'YES' if self.emergency_mode else 'NO'}",


            "",


            "N = Night",


            "R = Rain",


            "A = AI Mode",


            "1 = NS Green",


            "2 = EW Green"


        ]


        y = 30


        for index, text in enumerate(data):


            if index == 0:


                image = FONT_BIG.render(

                    text,

                    True,

                    (0, 255, 255)

                )


            else:


                image = FONT_SMALL.render(

                    text,

                    True,

                    WHITE

                )


            self.screen.blit(

                image,

                (30, y)

            )


            y += 20


    # =====================================

    # Keyboard Events

    # =====================================


    def handle_events(self):


        for event in pygame.event.get():


            if event.type == pygame.QUIT:


                self.running = False


            elif event.type == pygame.KEYDOWN:


                if event.key == pygame.K_n:


                    self.night_mode = not self.night_mode


                elif event.key == pygame.K_r:


                    self.rain_mode = not self.rain_mode


                elif event.key == pygame.K_a:


                    self.ai_mode = not self.ai_mode


                elif event.key == pygame.K_1:


                    self.current_phase = "NS"


                elif event.key == pygame.K_2:


                    self.current_phase = "EW"


                elif event.key in (

                    pygame.K_EQUALS,

                    pygame.K_PLUS

                ):


                    self.spawn_delay = max(

                        5,

                        self.spawn_delay - 5

                    )


                elif event.key == pygame.K_MINUS:


                    self.spawn_delay += 5

                        # =====================================

    # Main Game Loop

    # =====================================


    def run(self):


        while self.running:


            # -----------------------------

            # FPS

            # -----------------------------


            self.clock.tick(FPS)


            # -----------------------------

            # Events

            # -----------------------------


            self.handle_events()


            # -----------------------------

            # Spawn Vehicles

            # -----------------------------


            self.spawn_vehicle()


            # -----------------------------

            # AI Signal Controller

            # -----------------------------


            self.update_signals()


            # -----------------------------

            # Vehicle Update

            # -----------------------------

            self.update_vehicles()


            # -----------------------------

            # Draw Scene

            # -----------------------------


            self.draw_background()


            self.draw_vehicles()


            self.draw_signals()


            self.draw_dashboard()


            # -----------------------------

            # FPS Counter

            # -----------------------------


            if self.show_fps:


                fps = int(self.clock.get_fps())


                fps_text = FONT_SMALL.render(

                    f"FPS : {fps}",

                    True,

                    GREEN

                )


                self.screen.blit(

                    fps_text,

                    (WIDTH - 100, 10)

                )


            # -----------------------------

            # Update Display

            # -----------------------------


            pygame.display.flip()


        pygame.quit()