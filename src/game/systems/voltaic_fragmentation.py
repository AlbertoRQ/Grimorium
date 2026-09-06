import pygame
from game.entities.bullets.bullet import create_fragment


class VoltaicFragmentation:
    def __init__(
        self,
        bullet,
        original_damage,
        can_refragment=False,
        is_refragmentation=False,
    ):
        combo_data = bullet.effect_data["combos"]["fire_electric"]

        impact_push = 10

        self.x = bullet.impact_x if bullet.impact_x is not None else bullet.x
        self.y = bullet.impact_y if bullet.impact_y is not None else bullet.y

        direction = pygame.Vector2(bullet.vel_x, bullet.vel_y)

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.x += direction.x * impact_push
            self.y += direction.y * impact_push

        self.original_bullet_damage = original_damage
        self.bullet_color = bullet.color
        self.bullet_radius = bullet.radius

        self.combo_data = combo_data
        self.can_refragment = can_refragment
        self.is_refragmentation = is_refragmentation

        self.timer = 0
        self.duration = combo_data["embed_duration"]
        self.finished = False

        if bullet.fragment_direction is not None:
            direction = bullet.fragment_direction
        else:
            direction = pygame.Vector2(-bullet.vel_x, -bullet.vel_y)

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.inward_direction = direction

        

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.duration:
            self.finished = True
            return self.create_fragments()

        return []

    def draw(self, surface):
        if self.finished:
            return

        progress = min(self.timer / self.duration, 1)
        pulse = int(self.timer * 30) % 2

        position = (int(self.x), int(self.y))

        #halo_radius = self.bullet_radius + 2 + int(progress * 4)
        halo_radius = self.bullet_radius + 2 + int(progress * 3) + pulse

        # Halo amarillo de sobrecarga
        pygame.draw.circle(
            surface,
            (255, 220, 40),
            position,
            halo_radius,
        )

        # Interior oscuro para que el halo sea solo un borde
        pygame.draw.circle(
            surface,
            (45, 40, 20),
            position,
            max(1, halo_radius - 1),
        )

        # Bala original incrustada
        pygame.draw.circle(
            surface,
            self.bullet_color,
            position,
            self.bullet_radius,
        )

    def create_fragments(self):
        fragment_count = self.combo_data["fragment_count"]
        refragment_divisor = self.combo_data["refragment_divisor"]

        if self.is_refragmentation:
            fragment_count = max(
                1,
                fragment_count // refragment_divisor,
            )

        spread_angle = self.combo_data["spread_angle"]
        fragment_range = self.combo_data["fragment_range"]
        damage_multiplier = self.combo_data["damage_multiplier"]

        fragment_damage = (
            self.original_bullet_damage * damage_multiplier
        )

        fragment_speed = 220

        fragments = []

        if fragment_count == 1:
            angles = [0]
        else:
            angle_step = spread_angle / (fragment_count - 1)
            angles = [
                -spread_angle / 2 + index * angle_step
                for index in range(fragment_count)
            ]

        for angle in angles:
            direction = self.inward_direction.rotate(angle)

            spawn_distance = 18

            spawn_x = self.x + direction.x * spawn_distance
            spawn_y = self.y + direction.y * spawn_distance

            fragment = create_fragment(
                x=spawn_x,
                y=spawn_y,
                vel_x=direction.x * fragment_speed,
                vel_y=direction.y * fragment_speed,
                max_distance=fragment_range,
                damage=fragment_damage,
                effect_data={"combos": {"fire_electric": self.combo_data}},
            )
            fragment.can_refragment = self.can_refragment

            fragments.append(fragment)

        return fragments
