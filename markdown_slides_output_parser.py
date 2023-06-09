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
    def _handle_header(cur, cur_slide, slides):
        if not cur_slide:
            cur_slide = SlideWithSubtitle()
            cur_slide.subtitle = get_content_only(cur)
        elif isinstance(cur_slide, SlideWithBulletPoints):
            cur_slide.title = get_content_only(cur)
            slides.insert(0, cur_slide)
            cur_slide = None
        elif isinstance(cur_slide, SlideWithSubtitle):
            cur_slide.title = get_content_only(cur)
            MarkdownSlidesOutputParser._insert_title_slide(slides, cur_slide)
            cur_slide = None
        return cur_slide

    @staticmethod
    def _handle_bullet_point(cur, cur_slide, lines):
        if not cur_slide:
            cur_slide = SlideWithBulletPoints()
        if not isinstance(cur_slide, SlideWithBulletPoints):
            raise ValueError(f"Error parsing {cur} in {lines}")
        cur_slide.bullet_points.insert(0, BulletPoint.from_bullet_point_line(cur))
        return cur_slide

    @staticmethod
    def _is_bullet_point(line):
        return line and not line.startswith("#")

    def parse(self, text: str) -> T:
        lines = text.splitlines()
        lines = [line for line in lines if line]  # remove empty lines
        slides = []

        cur_slide = None

        # 處理回傳的markdown字串。把markdown轉成`markdown_slide.py`裡的物件
        # 演算法是從最後一行往前看。任何'#'開頭的都當成投影片標頭處理。其他所有內容都當bullet point要點處理
        # 所有文字格式都會被忽略。內嵌的圖片會忽略。超連結會忽略。
        # 只支援產生含有標題副標題跟含有標題跟bullet point要點的投影片
        # bullet point可以有階層。含有數字的列表會被轉成無數字的列表
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


