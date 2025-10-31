#importing the necessary libraries
import pygame
import math
pygame.init()

#Window setup
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

#Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
Dark_grey = (80, 78, 81)

# Colors for outer planets
JUPITER_ORANGE = (255, 165, 0)
SATURN_TAN = (210, 180, 140)
URANUS_CYAN = (0, 255, 255)
NEPTUNE_BLUE = (0, 0, 255)

FONT = pygame.font.SysFont("comicsans", 16)

#Planet class
class Planet:
    AU = (149.6e6 * 1000)  # Astronomical Unit in meters
    G = 6.67428e-11  # Gravitational Constant
    LOG_SCALE = 110 
    TIMESTEP = 3600*24  # 1 day in seconds
    
    # 1. ADDED 'name' to the constructor
    def __init__(self, x, y, radius, color, mass, name):
        self.x = x 
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name # Store the name
        self.orbit = [] 
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        # 1. CALCULATE REAL DISTANCE AND ANGLE
        distance_from_sun = math.sqrt(self.x**2 + self.y**2)
        angle = math.atan2(self.y, self.x)
        
        # 2. APPLY LOGARITHMIC SCALING for VISUALS
        if distance_from_sun > 0:
            distance_in_au = distance_from_sun / self.AU
            scaled_distance = math.log1p(distance_in_au) * self.LOG_SCALE
        else:
            scaled_distance = 0

        # 3. CONVERT SCALED POLAR COORDS BACK TO SCREEN X, Y
        x = scaled_distance * math.cos(angle) + WIDTH / 2
        y = scaled_distance * math.sin(angle) + HEIGHT / 2

        # 4. DRAW ORBIT
        if len(self.orbit) > 2:
            updated_orbit = []
            for point in self.orbit:
                point_x, point_y = point
                point_dist = math.sqrt(point_x**2 + point_y**2)
                point_angle = math.atan2(point_y, point_x)
                
                if point_dist > 0:
                    point_dist_au = point_dist / self.AU
                    scaled_point_dist = math.log1p(point_dist_au) * self.LOG_SCALE
                else:
                    scaled_point_dist = 0
                
                orbit_x = scaled_point_dist * math.cos(point_angle) + WIDTH / 2
                orbit_y = scaled_point_dist * math.sin(point_angle) + HEIGHT / 2
                updated_orbit.append((orbit_x, orbit_y))
                
            pygame.draw.lines(win, self.color, False, updated_orbit, 2)

        # 5. DRAW THE PLANET CIRCLE
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)
        
        # 2. UPDATED THIS ENTIRE 'DRAW TEXT' SECTION
        # 6. DRAW THE TEXT
        
        # Render the name first
        name_text = FONT.render(self.name, 1, WHITE)
        
        if not self.sun:
            # --- Draw distance text ---
            distance_au = self.distance_to_sun / self.AU
            distance_text = FONT.render(f"{distance_au:.2f} AU", 1, WHITE)
            
            # Position distance text
            text_x_dist = x - distance_text.get_width() / 2
            text_y_dist = y - self.radius - 8 # Position for bottom text (distance)
            
            # Position name text *above* the distance text
            text_x_name = x - name_text.get_width() / 2
            text_y_name = text_y_dist - name_text.get_height() # Position for top text (name)
            
            # Blit both
            win.blit(name_text, (text_x_name, text_y_name))
            win.blit(distance_text, (text_x_dist, text_y_dist))
        
        else:
            # For the Sun, just draw its name centered
            text_x = x - name_text.get_width() / 2
            text_y = y - name_text.get_height() / 2
            win.blit(name_text, (text_x, text_y))
    
    # --- (attraction and update_position methods are unchanged) ---
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        if distance == 0:
            return 0, 0
            
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        # Update position based on velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y)) # Append current position to orbit


#Main function
def main():
    run = True
    clock = pygame.time.Clock()

    #Creating planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "Sun")
    sun.sun = True
    
    mercury = Planet(0.387 * Planet.AU, 0, 8, Dark_grey, 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000
    
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000
    
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE , 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000
    
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED , 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000
    
    jupiter = Planet(5.203 * Planet.AU, 0, 20, JUPITER_ORANGE, 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = 13.06 * 1000
    
    saturn = Planet(9.539 * Planet.AU, 0, 18, SATURN_TAN, 5.683 * 10**26, "Saturn")
    saturn.y_vel = 9.68 * 1000
    
    uranus = Planet(19.18 * Planet.AU, 0, 16, URANUS_CYAN, 8.681 * 10**25, "Uranus")
    uranus.y_vel = 6.80 * 1000
    
    neptune = Planet(30.06 * Planet.AU, 0, 16, NEPTUNE_BLUE, 1.024 * 10**26, "Neptune")
    neptune.y_vel = 5.43 * 1000
    
    #List of planets
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()