import pygame
import random
from .target import Target
from . import sounds

# Game Engine

# --- Colors ---
WHITE = (255, 255, 255)
RED = (220, 60, 60)
YELLOW = (255, 220, 50)
GREEN = (100, 220, 100)
LIGHT_GRAY = (180, 180, 190)
DARK_OVERLAY = (20, 20, 25)

# --- Game states ---
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

# --- Difficulty presets ---
# Each preset controls the target's base size, minimum size, and how
# many frames it stays on-screen before expiring.
DIFFICULTIES = {
    "easy":   {"base_radius": 50, "min_radius": 18, "lifespan": 150,
               "label": "Easy"},
    "medium": {"base_radius": 40, "min_radius": 12, "lifespan": 90,
               "label": "Medium"},
    "hard":   {"base_radius": 28, "min_radius": 8,  "lifespan": 55,
               "label": "Hard"},
}


class GameEngine:
    """Central controller that manages game state, rendering and input."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.margin = 60
        self.hud_height = 60

        # Fonts
        self.font = pygame.font.SysFont("Arial", 26)
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_small = pygame.font.SysFont("Arial", 22)

        # Initialize sound effects (Task 4)
        sounds.init()

        # Begin at the difficulty-selection menu
        self.state = STATE_MENU
        self.difficulty = "medium"
        self._init_game_vars()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_game_vars(self):
        """Reset all gameplay variables for a new round."""
        diff = DIFFICULTIES[self.difficulty]
        self.base_radius = diff["base_radius"]
        self.min_radius = diff["min_radius"]
        self.lifespan = diff["lifespan"]

        self.target = self._spawn_target()
        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60
        self.hits = 0
        self.misses = 0
        self.score = 0
        self._gameover_sound_played = False

    def _spawn_target(self):
        """Create a new target at a random position within the play area."""
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(self.margin + self.hud_height,
                           self.height - self.margin)
        return Target(x, y, self.base_radius, self.min_radius, self.lifespan)

    def _start_game(self, difficulty):
        """Transition from menu / game-over into a new round."""
        self.difficulty = difficulty
        self._init_game_vars()
        self.state = STATE_PLAYING

    # ------------------------------------------------------------------
    # Event / input handling
    # ------------------------------------------------------------------

    def handle_event(self, event):
        """Dispatch a single pygame event to the appropriate handler."""
        if self.state == STATE_PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)

        elif self.state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                self._handle_menu_key(event.key)

        elif self.state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                self._handle_menu_key(event.key)

    def _handle_menu_key(self, key):
        """Process a key press on the menu or game-over screen."""
        if key == pygame.K_1:
            self._start_game("easy")
        elif key == pygame.K_2:
            self._start_game("medium")
        elif key == pygame.K_3:
            self._start_game("hard")
        elif key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _handle_click(self, pos):
        """Score a hit or miss depending on whether the click is inside
        the target's *visual* radius (Task 1 fix lives in Target class)."""
        x, y = pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            sounds.play_hit()                       # Task 4
            self.target = self._spawn_target()
        else:
            self.misses += 1
            sounds.play_miss()                      # Task 4

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self):
        """Advance the game by one frame."""
        if self.state != STATE_PLAYING:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.state = STATE_GAME_OVER
            if not self._gameover_sound_played:
                sounds.play_gameover()              # Task 4
                self._gameover_sound_played = True
            return

        self.target.update()
        if self.target.expired():
            self.misses += 1                        # timeout counts as miss
            sounds.play_miss()                      # Task 4
            self.target = self._spawn_target()

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    def accuracy(self):
        """Return the accuracy as a percentage, rounded to one decimal."""
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, screen):
        """Draw the current frame depending on the game state."""
        if self.state == STATE_MENU:
            self._render_menu(screen)
        elif self.state == STATE_PLAYING:
            self._render_playing(screen)
        elif self.state == STATE_GAME_OVER:
            self._render_game_over(screen)

    # --- Menu screen ---------------------------------------------------

    def _render_menu(self, screen):
        cx = self.width // 2

        title = self.font_large.render("TARGET AIM TRAINER", True, WHITE)
        screen.blit(title, (cx - title.get_width() // 2, 80))

        sub = self.font_medium.render("Choose Difficulty", True, LIGHT_GRAY)
        screen.blit(sub, (cx - sub.get_width() // 2, 160))

        options = [
            ("1  -  Easy", GREEN,  "(Large targets, slow shrink)"),
            ("2  -  Medium", YELLOW, "(Default targets, normal shrink)"),
            ("3  -  Hard", RED,    "(Small targets, fast shrink)"),
        ]
        y_start = 230
        for i, (label, color, desc) in enumerate(options):
            text = self.font_medium.render(label, True, color)
            screen.blit(text, (cx - 160, y_start + i * 60))
            desc_text = self.font_small.render(desc, True, LIGHT_GRAY)
            screen.blit(desc_text, (cx + 60, y_start + i * 60 + 6))

        hint = self.font_small.render("Press ESC to quit", True, LIGHT_GRAY)
        screen.blit(hint, (cx - hint.get_width() // 2, self.height - 50))

    # --- In-game HUD ---------------------------------------------------

    def _render_playing(self, screen):
        # Draw the target
        r = int(self.target.visual_radius())
        pygame.draw.circle(screen, RED, (self.target.x, self.target.y), r)
        pygame.draw.circle(screen, WHITE, (self.target.x, self.target.y), r, 2)

        # HUD bar
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_text, (self.width // 2 - 90, 10))

    # --- Game-over screen (Task 2) + replay menu (Task 3) --------------

    def _render_game_over(self, screen):
        cx = self.width // 2

        # Semi-transparent dark overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill(DARK_OVERLAY)
        screen.blit(overlay, (0, 0))

        # "GAME OVER" title
        title = self.font_large.render("GAME OVER", True, RED)
        screen.blit(title, (cx - title.get_width() // 2, 50))

        # Final statistics
        score_surf = self.font_medium.render(
            f"Final Score: {self.score}", True, WHITE)
        screen.blit(score_surf, (cx - score_surf.get_width() // 2, 130))

        acc_surf = self.font_medium.render(
            f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_surf, (cx - acc_surf.get_width() // 2, 175))

        detail = self.font.render(
            f"Hits: {self.hits}   Misses: {self.misses}", True, LIGHT_GRAY)
        screen.blit(detail, (cx - detail.get_width() // 2, 225))

        diff_label = DIFFICULTIES[self.difficulty]["label"]
        diff_surf = self.font.render(
            f"Difficulty: {diff_label}", True, LIGHT_GRAY)
        screen.blit(diff_surf, (cx - diff_surf.get_width() // 2, 260))

        # Replay options (Task 3)
        replay_title = self.font_medium.render("Play Again?", True, YELLOW)
        screen.blit(replay_title,
                    (cx - replay_title.get_width() // 2, 310))

        labels = [("1 - Easy", GREEN),
                  ("2 - Medium", YELLOW),
                  ("3 - Hard", RED)]
        total_w = len(labels) * 140
        start_x = cx - total_w // 2
        for i, (label, color) in enumerate(labels):
            surf = self.font.render(label, True, color)
            screen.blit(surf, (start_x + i * 140, 360))

        quit_hint = self.font_small.render(
            "Press ESC or Q to quit", True, LIGHT_GRAY)
        screen.blit(quit_hint,
                    (cx - quit_hint.get_width() // 2, self.height - 45))
