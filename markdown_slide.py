import json
from typing import List

from pptx.presentation import Presentation


class SlideWithTitle(object):
    title: str

    def __init__(self):
        self.title = ""

    def add_slide(self, presentation: Presentation):
        raise NotImplementedError()

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)


class SlideWithSubtitle(SlideWithTitle):
    subtitle: str

    def __init__(self):
        super().__init__()
        self.subtitle = ""

    def add_slide(self, presentation: Presentation):
        title_slide_layout = presentation.slide_layouts[0]
        slide = presentation.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]

        title.text = self.title
        subtitle.text = self.subtitle


class SlideWithBulletPoints(SlideWithTitle):
    bullet_points: List

    def __init__(self):
        super().__init__()
        self.bullet_points = []

    def add_slide(self, presentation: Presentation):
        bullet_slide_layout = presentation.slide_layouts[1]

        slide = presentation.slides.add_slide(bullet_slide_layout)
        shapes = slide.shapes

        title_shape = shapes.title
        body_shape = shapes.placeholders[1]

        title_shape.text = self.title

        tf = body_shape.text_frame
        tf.text = self.bullet_points.pop(0)
        for bp in self.bullet_points:
            p = tf.add_paragraph()
            p.text = bp
            p.level = 0
