from langchain.schema import BaseOutputParser, T

from markdown_slide import SlideWithBulletPoints, SlideWithSubtitle, BulletPoint
from util import get_content_only


HORIZONTAL_RULE = "---"


class MarkdownSlidesOutputParser(BaseOutputParser):
    def get_format_instructions(self) -> str:
        return "投影片格式為markdown格式"

    @staticmethod
    def _insert_title_slide(slides, title_slide):
        assert isinstance(title_slide, SlideWithSubtitle)

        if not title_slide.title:
            title_slide.title = title_slide.subtitle
            title_slide.subtitle = None

        slides.insert(0, title_slide)

    @staticmethod
    def _is_bullet_point(line):
        return line and not line.startswith("#")

    def parse(self, text: str) -> T:
        lines = text.splitlines()
        lines = [line for line in lines if line]  # remove empty lines
        slides = []

        cur_slide = None

        # 預期除了第一張投影片有可能是標題跟副標以外其他投影片一律是標題跟bullet point要點式的投影片
        # Markdown裡面'-'、'*'跟數字開頭的都是bullet point。其餘'#'開頭的都是標題或副標
        # 演算法是從後面往前看。看到bullet point就加到目前的
        while lines:
            cur = lines.pop(-1)
            try:
                if cur == HORIZONTAL_RULE:
                    assert cur_slide
                    if isinstance(cur_slide, SlideWithSubtitle):
                        self._insert_title_slide(slides, cur_slide)
                    else:
                        slides.insert(0, cur_slide)
                    cur_slide = None
                elif self._is_bullet_point(cur):
                    cur_slide = self._handle_bullet_point(cur, cur_slide, lines)
                elif cur.startswith("#"):
                    cur_slide = self._handle_header(cur, cur_slide, slides)
            except Exception as e:
                print(f"Exception handling line '{cur}'. Exception: '{e}'. Skipping")

        if cur_slide:
            self._insert_title_slide(slides, cur_slide)
        return slides

    def _handle_header(self, cur, cur_slide, slides):
        if not cur_slide:
            cur_slide = SlideWithSubtitle()
            cur_slide.subtitle = get_content_only(cur)
        elif isinstance(cur_slide, SlideWithBulletPoints):
            cur_slide.title = get_content_only(cur)
            slides.insert(0, cur_slide)
            cur_slide = None
        elif isinstance(cur_slide, SlideWithSubtitle):
            cur_slide.title = get_content_only(cur)
            self._insert_title_slide(slides, cur_slide)
            cur_slide = None
        return cur_slide

    def _handle_bullet_point(self, cur, cur_slide, lines):
        if not cur_slide:
            cur_slide = SlideWithBulletPoints()
        if not isinstance(cur_slide, SlideWithBulletPoints):
            raise ValueError(f"Error parsing {cur} in {lines}")
        cur_slide.bullet_points.insert(0, BulletPoint.from_bullet_point_line(cur))
        return cur_slide

