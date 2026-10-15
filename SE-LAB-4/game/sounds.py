"""
sounds.py – Procedural sound effects for Target Aim Trainer.

Generates simple beep-style tones using the built-in `array` module so
no external audio files are required.  If pygame is unavailable the module
silently provides no-op stubs so the rest of the game still works.
"""

import math
import array as _array

try:
    import pygame
    _pygame_ok = True
except ImportError:
    _pygame_ok = False

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _make_tone(frequency: float, duration_ms: int,
               volume: float = 0.4, sample_rate: int = 44100) -> "pygame.mixer.Sound | None":
    """Return a pygame Sound object containing a sine-wave tone.

    The tone is built entirely from a computed sine wave stored in a
    signed-16-bit buffer, so numpy is *not* required.
    """
    if not _pygame_ok:
        return None
    try:
        n_samples = int(sample_rate * duration_ms / 1000)
        buf = _array.array("h")          # signed 16-bit integers
        max_amp = int(32767 * volume)
        for i in range(n_samples):
            t = i / sample_rate
            val = int(max_amp * math.sin(2 * math.pi * frequency * t))
            buf.append(val)              # left channel
            buf.append(val)              # right channel (stereo)
        raw = bytes(buf)
        sound = pygame.mixer.Sound(buffer=raw)
        return sound
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_hit_sound: "pygame.mixer.Sound | None" = None
_miss_sound: "pygame.mixer.Sound | None" = None
_gameover_sound: "pygame.mixer.Sound | None" = None
_initialized = False


def init():
    """Call once after pygame.init() to build all sound effects."""
    global _hit_sound, _miss_sound, _gameover_sound, _initialized
    if _initialized or not _pygame_ok:
        return
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        _hit_sound      = _make_tone(880,  80,  volume=0.35)   # high, short ping
        _miss_sound     = _make_tone(220, 180,  volume=0.30)   # low, longer buzz
        _gameover_sound = _make_tone(330, 600,  volume=0.40)   # mid, long drone
        _initialized = True
    except Exception:
        pass                                                    # fail silently


def play_hit():
    """Play the hit sound effect."""
    if _hit_sound:
        _hit_sound.play()


def play_miss():
    """Play the miss sound effect."""
    if _miss_sound:
        _miss_sound.play()


def play_gameover():
    """Play the game-over sound effect."""
    if _gameover_sound:
        _gameover_sound.play()
