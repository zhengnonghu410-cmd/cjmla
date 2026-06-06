from pygame import mixer
from classes.Config import asset_path


class Sound:
    def __init__(self):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(0.2)

        self.allowSFX = True

        self.soundtrack = mixer.Sound(asset_path("./sfx/main_theme.ogg"))
        self.coin = mixer.Sound(asset_path("./sfx/coin.ogg"))
        self.bump = mixer.Sound(asset_path("./sfx/bump.ogg"))
        self.stomp = mixer.Sound(asset_path("./sfx/stomp.ogg"))
        self.jump = mixer.Sound(asset_path("./sfx/small_jump.ogg"))
        self.death = mixer.Sound(asset_path("./sfx/death.wav"))
        self.kick = mixer.Sound(asset_path("./sfx/kick.ogg"))
        self.brick_bump = mixer.Sound(asset_path("./sfx/brick-bump.ogg"))
        self.powerup = mixer.Sound(asset_path("./sfx/powerup.ogg"))
        self.powerup_appear = mixer.Sound(asset_path("./sfx/powerup_appears.ogg"))
        self.pipe = mixer.Sound(asset_path("./sfx/pipe.ogg"))

    def play_sfx(self, sfx):
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music):
        self.music_channel.play(music)
