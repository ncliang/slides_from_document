import json
from typing import List


class SlideWithTitle(object):
    title: str

    def __init__(self):
        self.title = ""

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)


class SlideWithSubtitle(SlideWithTitle):
    subtitle: str

    def __init__(self):
        super().__init__()
        self.subtitle = ""


class SlideWithBulletPoints(SlideWithTitle):
    bullet_points: List

    def __init__(self):
        super().__init__()
        self.bullet_points = []

