from typing import List


class SlideWithTitle(object):
    title: str

    def __init__(self):
        self.title = ""

    def has_title(self):
        return self.title

    def has_subtitle(self):
        return False

    def has_bullet_points(self):
        return False


class SlideWithSubtitle(SlideWithTitle):
    subtitle: str

    def __init__(self):
        super().__init__()
        self.subtitle = ""

    def has_subtitle(self):
        return self.subtitle


class SlideWithBulletPoints(SlideWithTitle):
    bullet_points: List

    def __init__(self):
        super().__init__()
        self.bullet_points = []

    def has_bullet_points(self):
        return self.bullet_points
