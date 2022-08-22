import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulation du système solaire - Teyko')

WHITE = (255, 255 ,255)
YELLOW = (253, 184 ,19)
BLUE = (5, 105 ,181)
BROWN = (193, 68, 14)
GREY = (173, 168, 165)
BEIGE = (248, 226, 176)

class Planet:
    #Astronomical Unit (Approximately distance of the Earth to the Sun)
    AU = 149.6e6 * 1000
    #Gravitanional Constant
    G = 6.67428e-11
    #Scale, 1AU = 100px
    SCALE = 250 / AU
    #Time to represent in the simulation (Seconds in one hour * Number of hours)
    TIMESTEP = 3600*24

    def __init__(self, x, y, radius, color, mass):
        #Planet Property
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass  = mass #Mass is in kilograms
        self.orbit = []
        self.distance_to_sun = 0

        # Planet Type
        self.sun = False

        # Velocity
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        #Draw orbit line
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            #Draw planets orbit line on screen
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        #Draw planets on screen
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        #Calculate distance between two object (Planet -> Sun)
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        #Calculate force of attraction
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_postion(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        #f = m / a (force = masse / acceleration)
        #a = f / m (acceleration = force / masse)
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))


def main() :
    run = True
    clock = pygame.time.Clock()

    # Create Sun
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True #Define Sun property
    # Create Earth
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.972 * 10**24)
    earth.y_vel = 29.783 * 1000
    # Create Mars
    mars = Planet(-1.524 * Planet.AU, 0, 13, BROWN, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    #test = Planet(-2 * Planet.AU, 0, 13, YELLOW, 5.972 * 10**24)
    #test.y_vel = 24.077 * 1000

    # Create Mercury
    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, 3.285 * 10**23)
    mercury.y_vel = -47.4 * 1000
    # Create Venus
    venus = Planet(0.723 * Planet.AU, 0, 14, BEIGE, 4.867 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus] #List of planets/stars to simulate

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_postion(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()