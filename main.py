import pygame
import asyncio
from glob import glob
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('galary', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        self.health = 3
        self.can_take_damage = True
        self.damage_time = 0

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400



        #mask
        self.mask = pygame.mask.from_surface(self.image)


    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def damage_timer(self):
        if not self.can_take_damage:
            if pygame.time.get_ticks() - self.damage_time >= 1200:
                self.can_take_damage = True



    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        

        self.laser_timer()
        self.damage_timer()

        
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf

        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf


        self.original_surf = surf
        self.rotation = 0
        self.rotation_speed = randint(-180, 180)


        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400,500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        
        # Rotate without changing meteor position
        old_center = self.rect.center
        self.rotation += self.rotation_speed * dt

        self.image = pygame.transform.rotate(
            self.original_surf,
            self.rotation
        )

        self.rect = self.image.get_frect(center=old_center)

        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0

        self.image = self.frames[self.frame_index] 
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):

            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()


def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites and player.can_take_damage:
        player.health -= 1
        player.can_take_damage = False
        player.damage_time = pygame.time.get_ticks()
        damage_sound.play()
        
        if player.health <= 0:
            running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def get_background(dt):
    global background_index, background_timer

    background_timer += dt

    if background_timer >= 0.1:
        background_timer = 0
        background_index = (
            background_index + 1
        ) % len(background_frames)

    return pygame.transform.scale(
        background_frames[background_index],
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )


def display_score():
    current_time = (pygame.time.get_ticks() - game_start_time) // 100
    text_surf = font.render(str(current_time), True, (255,255,255))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50 ))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20,30).move(0,-8), 5,10)

def display_health():
    health_text = heart_font.render("♥ "* player.health, True, (255, 80, 100))
    display_surface.blit(health_text, (30, 25))


def display_start_screen():
    #dark
    overlay = pygame.Surface(
        (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill((5, 8, 20, 165))
    display_surface.blit(overlay, (0, 0))

    #titles
    title = title_font.render("SPACE SHOOTER", True, (90, 220, 225))
    title_rect = title.get_rect(center = (WINDOW_WIDTH / 2, 170))
    display_surface.blit(title, title_rect)

    #story
    line1 = story_font.render("Meteor storm are destroying Earth.", True, "white")
    line2 = story_font.render("Guide the last dinosaurs to safety in space.", True, "white")


    display_surface.blit(line1, line1.get_rect(center = (WINDOW_WIDTH / 2, 270)))
    display_surface.blit(line2, line2.get_rect(center = (WINDOW_WIDTH / 2, 315)))

    #spaceship in initial screen
    ship = pygame.transform.scale_by(player.image, 1.5)
    ship_rect = ship.get_rect(center = (WINDOW_WIDTH / 2, 440))
    display_surface.blit(ship, ship_rect)

    #start rules
    start_text = button_font.render("PRESS SPACE TO LAUNCH", True, (255, 220, 70))
    start_rect = start_text.get_rect(center = (WINDOW_WIDTH / 2, 580))
    display_surface.blit(start_text, start_rect)

    controls = story_font.render("Arrow Keys: Move    Space: Fire", True, (210, 210, 210))
    controls_rect = controls.get_rect(center = (WINDOW_WIDTH / 2, 640))

    display_surface.blit(controls, controls_rect)


#genral setup     
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Killer")
running = True
clock = pygame.time.Clock()
game_started = False
game_start_time = 0

background_paths = sorted(
    glob(join("galary", "images", "bg_frames", "*.jpg"))
)

background_frames = [
    pygame.image.load(path).convert()
    for path in background_paths
    ]


background_index = 0
background_timer = 0

# import
star_surf = pygame.image.load(join('galary', 'images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('galary', 'images/meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('galary', 'images', 'laser.png')).convert_alpha()
font = pygame.font.Font(None, 50)
title_font = pygame.font.SysFont("DejaVu Sans", 82, bold = True)
story_font = pygame.font.SysFont("DejaVu Sans", 32)
button_font = pygame.font.SysFont("DejaVu Sans", 38, bold = True)
heart_font = pygame.font.SysFont("DejaVu Sans", 50)
explosion_frames = [pygame.image.load(join('galary', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('galary', 'audio', 'laser.mp3'))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(join('galary', 'audio', 'explosion.mp3'))
explosion_sound.set_volume(0.5)
game_music = pygame.mixer.Sound(join('galary', 'audio', 'game_music.mp3'))
game_music.set_volume(0.4)
game_music.play(loops = -1)
damage_sound = pygame.mixer.Sound(join("galary", "audio", "damage.ogg"))
damage_sound.set_volume(0.5)


# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# for i in range(20):
#     Star(all_sprites, star_surf)

player = Player(all_sprites)

#custom event -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

async def main():
    global running, game_started, game_start_time

    while running:
        dt = clock.tick(60) / 1000

        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started:
                    game_started = True
                    game_start_time = pygame.time.get_ticks()

            if event.type == meteor_event and game_started:
                x ,y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

        #update
        
        
        




        # Draw the game
        background_surf = get_background(dt)
        display_surface.blit(background_surf, (0, 0))
        if game_started:
            all_sprites.update(dt)
            collisions()

            display_score()
            display_health()
            all_sprites.draw(display_surface)

        else:
            display_start_screen()


        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
pygame.quit()
