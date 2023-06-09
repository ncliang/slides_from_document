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

        self.assertEquals("發布單位：農業處", parsed[0].subtitle)

        self.assertEquals("雲林縣政府新聞參考資料 112.06.07", parsed[1].title)
        self.assertEquals("雲林縣落花生產量占全台七成", parsed[1].bullet_points[0].text)

    def test_single_title_slide(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助

## 發布單位：農業處
""")
        self.assertEquals(1, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithSubtitle))
        self.assertEquals("發布單位：農業處", parsed[0].subtitle)

    def test_single_title_only(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""# 落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助""")
        self.assertEquals(1, len(parsed))
        self.assertTrue(isinstance(parsed[0], SlideWithSubtitle))
        self.assertEquals("落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助", parsed[0].title)

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
        self.assertEquals("落花生不敵低溫及雨害　張麗善:建請農委會儘速公告天然災害救助", parsed[0].title)
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

    def test_nested_bullet_points(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""### 招生及開班訊息

- 招生時間：112年3月21日起
- 開班時間：112年5月4日起
- 招生及開班訊息公佈於以下管道：
  - 勞動暨青年事務發展處-公務公告
  - 勞動部勞動力發展署臺灣就業通網站
  - 勞動部勞動力發展署雲嘉南分署
  - 斗六就業中心、虎尾就業中心、各鄉、鎮、市公所就業服務台
""")
        self.assertEquals(1, len(parsed))
        self.assertEquals("招生時間：112年3月21日起", parsed[0].bullet_points[0].text)
        self.assertEquals(0, parsed[0].bullet_points[0].level)
        self.assertEquals("斗六就業中心、虎尾就業中心、各鄉、鎮、市公所就業服務台", parsed[0].bullet_points[-1].text)
        self.assertEquals(1, parsed[0].bullet_points[-1].level)

    def test_slide_with_content(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""## 張縣長的話

張縣長表示，雲林子弟在各領域努力精益求精，在全國藝文與體育競賽獲得傑出表現為雲林爭光，這股持之以恆的精神與努力不懈的毅力，正是雲林人世代傳承的勤奮精神，足為所有雲林子弟的學習標竿。

張縣長指出，孝行模範在當前現代社會彰顯難能可貴的人文典範，其親力親為陪伴、侍奉至親的精神，不僅實踐「百善孝為先」的傳統美德，也是形塑溫馨友善社會的最佳榜樣，值得傳頌與推崇。

社教有功惠風獎得獎人，身體力行推動社會教育，以在地為起點投入心力，為終身學習教育做出重大貢獻。全國藝文競賽優勝人員長期於音樂、舞蹈、戲劇及歌謠等領域努力，在全國性賽事掄元、大放光芒，並在雲林縣文化觀光處演藝廳公開展演，獲得民眾高度肯定與讚賞，蔚為雲林藝文新風華。

張縣長再說，雲林縣雖然是農業大縣，也是個宗教大縣，但這幾年來我們非常重視教育，尤其是教育優先的部分，從領先全國2年全面裝設縣內國中小校園冷氣、全面提高學生營養午餐費至全國標準、國中一年級的女學生，提前施打九價HPV疫苗、邀請縣內優秀教育夥伴研發出全國第一套縣訂版的品德教育教材等。

此外，為了孩子的多元學習，增聘17名專任運動教練，來訓練我們的學生；聘用將近百位外師，來營造沉浸式英語學習環境，提升孩子的國際移動力及競爭力；成立智慧教育中心及科技實驗學校，帶領我們的孩子乘著世界潮流，發展自己的資訊專長。用心規劃教育的成果，就是希望每位雲林子弟都能獲得最好的教育照顧，培養實力，找到未來的方向，創造出屬於自己的成功。

勤奮努力是雲林人的DNA，張縣長讚賞每位獲獎者的努力，並期許秉持「沒有最好，只有更好」的精神繼續追求卓越，從自身做起影響身邊每個人，成為社會正向發展的動能。""")
        self.assertEquals(1, len(parsed))
        self.assertEquals("張縣長的話", parsed[0].title)
        self.assertTrue(isinstance(parsed[0], SlideWithBulletPoints))
        self.assertEquals("張縣長表示，雲林子弟在各領域努力精益求精，在全國藝文與體育競賽獲得傑出表現為雲林爭光，這股持之以恆的精神與努力不懈的毅力，正是雲林人世代傳承的勤奮精神，足為所有雲林子弟的學習標竿。", parsed[0].bullet_points[0].text)

    def test_ignore_unknown_markdown(self):
        parser = MarkdownSlidesOutputParser()
        parsed = parser.parse("""# 2023雲林之光、孝行模範、社教有功惠風獎暨全國藝文優勝人員 張麗善表揚恭賀

發布單位：教育處

日期：112.6.8

---""")
        self.assertEquals(1, len(parsed))
        self.assertEquals("2023雲林之光、孝行模範、社教有功惠風獎暨全國藝文優勝人員 張麗善表揚恭賀", parsed[0].title)
        self.assertTrue(isinstance(parsed[0], SlideWithBulletPoints))
        self.assertEquals(
            "發布單位：教育處",
            parsed[0].bullet_points[0].text)

