import pygame
import os

pygame.mixer.init()


class MusicPlayer:
    def __init__(self, music_folder="music_player/music"):
        self.music_folder = music_folder

        self.playlist = [
            f for f in os.listdir(music_folder)
            if f.endswith(".mp3") or f.endswith(".wav")
        ]

        self.current_index = 0
        self.paused = False

        if self.playlist:
            self.load_track()

    def load_track(self):
        path = os.path.join(self.music_folder, self.playlist[self.current_index])
        pygame.mixer.music.load(path)

    def play(self):
        pygame.mixer.music.play()
        self.paused = False

    def stop(self):
        pygame.mixer.music.stop()

    def pause_resume(self):
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.load_track()
        self.play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.load_track()
        self.play()

    def get_track_name(self):
        return self.playlist[self.current_index]

    def get_total_tracks(self):
        return len(self.playlist)

    def get_status(self):
        return "Paused" if self.paused else "Playing"

    def get_position_seconds(self):
        return pygame.mixer.music.get_pos() // 1000

    def update(self):
        # автопереход на следующий трек
        if not pygame.mixer.music.get_busy() and not self.paused:
            if self.playlist:
                self.next_track()