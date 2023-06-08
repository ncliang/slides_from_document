# 新聞稿投影片產生器

本專案實作利用`langchain`跟ChatGPT整合，幫文本內容產生ppt投影片。

## 安裝

```
pip install -r requirements.txt
```

## 使用

```
python3 slides_from_document.py -h
usage: slides_from_document.py [-h] --output OUTPUT (--content CONTENT | --url URL | --file FILE)

Generate slides from provided content using ChatGPT

options:
  -h, --help         show this help message and exit
  --output OUTPUT    Location of generated slide
  --content CONTENT  Content to use for slide generation
  --url URL          URL to content to use for slide generation
  --file FILE        A file to use as content for slide generation
```

- `--output`: 輸出的ppt檔存放的路徑
- `--content`: 輸入的文字
- `--url`: 輸入url使用爬蟲爬取網頁內容
- `--file`: 輸入磁碟上的檔案使用檔案內容。檔案格式可以是純文字檔, word, pdf等

`content`, `url`, 跟`file`參數至少要有一個。`output`參數為必要參數。

## 架構

核心使用`langchain`呼叫ChatGPT。在prompt裡面讓ChatGPT產生markdown語法的投影片大綱。再透過`python-pptx`套件把markdown寫成ppt檔。

### 主要物件
- markdown_slide.py: `SlideWithBulletPoints`, `BulletPoint`, `SlideWithSubtitle`, `SlideWithTitle`

用來代表投影片跟投影片內容的物件。只處理標題投影片跟含有標題跟要點清單的投影片。物件裡`add_slide`方法支援把自己加入到`python-pptx` `Presentation`物件裡

- markdown_slides_output_parser.py: `MarkdownSlidesOutputParser`

實現`langchain`的`OutputParser`介面。`get_format_instructions`方法回傳讓ChatGPT產生markdown的prompt。`parse`方法處理ChatGPT回傳的字串變成`markdown_slide.py`裡面的物件方便後續處理

- slides_from_document.py

主程式

