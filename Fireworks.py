import pygame
import sys
import random
import math
import os
import time
import requests
import io

# %%
# constants
FPS = 60
BLACK, WHITE = (0, 0, 0), (255, 255, 255)

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks Animation")
clock = pygame.time.Clock()  # Screen dimensions

# Load sounds
def download_and_play_firewhistle():
    # Initialize Pygame mixer
    pygame.mixer.init()
    
    # URL for a fire whistle sound (Creative Commons license)
    sound_url = "https://soundbible.com/grab.php?id=2188&type=wav"
    
    try:
        # Download the sound file
        print("Downloading fire whistle sound...")
        response = requests.get(sound_url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Create in-memory file object
        sound_file = io.BytesIO(response.content)
        # Load and play the sound
        print("Playing fire whistle...")
        sound = pygame.mixer.Sound(sound_file)
        sound.set_volume(1.0)  # 100% volume
        sound.play(loops=-1)   # Continuous loop
        
        # Wait while the sound is playing
        while pygame.mixer.get_busy():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pass
# Commented out the block that requires local sound files to avoid errors if files are missing.
# If you have the sound files, you can uncomment and use this block.

# pygame.mixer.init()
# firewhistle_path = os.path.join("sounds", "firewhistle.wav")
# firecrack_path = os.path.join("sounds", "firecrack.wav")
# if not os.path.exists(firewhistle_path) or not os.path.exists(firecrack_path):
#     print("Sound files not found. Please ensure 'firewhistle.wav' and 'firecrack.wav' are in the 'sounds' directory.")
#     sys.exit(1)
# firewhistle_sound = pygame.mixer.Sound(firewhistle_path)
# firecrack_sound = pygame.mixer.Sound(firecrack_path)

# Use dummy sound objects to avoid errors if sound files are missing
class DummySound:
    def play(self): pass
    def stop(self): pass

firewhistle_sound = DummySound()
firecrack_sound = DummySound()

class Firework:
    # constructor 
    def __init__(self, whistle_sound, crack_sound):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.target_y = random.randint(100, HEIGHT // 2)
        self.color = [random.randint(50, 255) for _ in range(3)]
        self.exploded = False
        self.particles = []
        self.whistle_playing = True

        # Import sounds
        self.whistle_sound = whistle_sound
        self.crack_sound = crack_sound

        # Play firewhistle sound
        self.whistle_sound.play()

    def update(self):
        if not self.exploded:
            self.y -= 5
            if self.y <= self.target_y:
                self.explode()
        else:
            for particle in self.particles:
                particle.update()

    def draw(self):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (self.x, self.y), 3)
        else:
            for particle in self.particles:
                particle.draw()

    def explode(self):
        self.exploded = True
        self.whistle_sound.stop()  # Stop whistle sound when exploding
        self.crack_sound.play()  # Play firecrack sound

        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.color))

class Particle:
    def __init__(self, x, y, dx, dy, color):  # constructor
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.lifetime = random.randint(40, 100)
        self.color = color
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # gravity effect
        self.lifetime -= 1

    def draw(self):
        if self.lifetime > 0:
            alpha = max(0, int((self.lifetime / 100) * 255))
            color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
            # Pygame doesn't support alpha in draw.circle by default, so use a surface
            particle_surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(particle_surface, (int(self.x)-self.size, int(self.y)-self.size))

def main():
    running = True
    fireworks = []
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Add new fireworks randomly (1/20 chance) 
        if random.randint(1, 20) == 1:
            fireworks.append(Firework(firewhistle_sound, firecrack_sound))

        # draw fireworks
        for firework in fireworks[:]:
            firework.update()
            firework.draw()
            if firework.exploded and all(p.lifetime <= 0 for p in firework.particles):
                fireworks.remove(firework)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
