import unittest

from markdown_slide import SlideWithSubtitle, SlideWithBulletPoints
from markdown_slides_output_parser import MarkdownSlidesOutputParser


class MarkdownSlidesOutputParserTest(unittest.TestCase):
    def test_title_and_bullet_points(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助

## 發布單位：農業處

### 雲林縣政府新聞參考資料 112.06.07

- 雲林縣落花生產量占全台七成
- 一期作落花生因開花期受低溫影響致結莢不佳，又成熟期受雨害造成腐爛及發芽，致六月份採收期幾乎沒得收成
- 縣長張麗善由農業處長魏勝德陪同，會同農改場及農糧署中區分署至土庫花生田現勘災損情形
- 張麗善指示立即函請農委會公告救助，為花生農爭取救助金每公頃3萬元
""")
        self.assertEquals(2, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithSubtitle))
        self.assertTrue(isinstance(parsed[1], SlideWithBulletPoints))
        self.assertEquals(4, len(parsed[1].bullet_points))

        self.assertEquals("## 發布單位：農業處", parsed[0].subtitle)

        self.assertEquals("### 雲林縣政府新聞參考資料 112.06.07", parsed[1].title)
        self.assertEquals("- 雲林縣落花生產量占全台七成", parsed[1].bullet_points[0])

    def test_single_title_slide(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助

## 發布單位：農業處
""")
        self.assertEquals(1, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithSubtitle))
        self.assertEquals("## 發布單位：農業處", parsed[0].subtitle)

    def test_single_title_only(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助""")
        self.assertEquals(1, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithSubtitle))
        self.assertEquals("# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助", parsed[0].title)

    def test_first_slide_no_subtitle(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助

### 雲林縣政府新聞參考資料 112.06.07

- 雲林縣落花生產量占全台七成
- 一期作落花生因開花期受低溫影響致結莢不佳，又成熟期受雨害造成腐爛及發芽，致六月份採收期幾乎沒得收成
- 縣長張麗善由農業處長魏勝德陪同，會同農改場及農糧署中區分署至土庫花生田現勘災損情形
- 張麗善指示立即函請農委會公告救助，為花生農爭取救助金每公頃3萬元
""")
        self.assertEquals(2, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithSubtitle))
        self.assertTrue(isinstance(parsed[1], SlideWithBulletPoints))
        self.assertEquals(4, len(parsed[1].bullet_points))
        self.assertEquals("# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助", parsed[0].title)
        self.assertIsNone(parsed[0].subtitle)

    def test_bullet_point_with_numbers(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""### 雲林縣政府新聞參考資料 112.06.07

1. 雲林縣落花生產量占全台七成
2. 一期作落花生因開花期受低溫影響致結莢不佳，又成熟期受雨害造成腐爛及發芽，致六月份採收期幾乎沒得收成
3. 縣長張麗善由農業處長魏勝德陪同，會同農改場及農糧署中區分署至土庫花生田現勘災損情形
4. 張麗善指示立即函請農委會公告救助，為花生農爭取救助金每公頃3萬元
""")
        self.assertEquals(1, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithBulletPoints))
        self.assertEquals(4, len(parsed[0].bullet_points))

    def test_bullet_point_with_stars(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""### 雲林縣政府新聞參考資料 112.06.07

* 雲林縣落花生產量占全台七成
* 一期作落花生因開花期受低溫影響致結莢不佳，又成熟期受雨害造成腐爛及發芽，致六月份採收期幾乎沒得收成
* 縣長張麗善由農業處長魏勝德陪同，會同農改場及農糧署中區分署至土庫花生田現勘災損情形
* 張麗善指示立即函請農委會公告救助，為花生農爭取救助金每公頃3萬元
""")
        self.assertEquals(1, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithBulletPoints))
        self.assertEquals(4, len(parsed[0].bullet_points))