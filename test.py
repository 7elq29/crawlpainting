import scrapy
import urllib.request
from urllib.parse import urljoin

class TestSpider(scrapy.Spider):
    name = 'testspider'
    start_urls = ["http://www.9610.com/suitang/lilongji.htm"]
    allowed_domains = ['www.9610.com']
    custom_settings = {
        'DEPTH_LIMIT': '1',
    }
    folder = "/Users/Ken/Downloads/image/"

    peoples = []

    def get_name(self, in_body_name, link_name, content, count, author):
        result = author + (link_name if link_name else "")
        if content and not content.isdigit():
            result += content
        elif in_body_name:
            result += in_body_name
        if content and content.isdigit():
            return result + str(content)
        else:
            count += 1
            return result + str(count)

    def filter_text(self, text):
        if not text:
            return None
        for s in ["点击右键逐页下载", "\n", "]["]:
            text.replace(s, "")
        #print(text)
        return str if str != "" else None

    def isTrash(self,node):
        for s in ["script","html"]:
            if node.startswith("<"+s):
                return True
        return False

    def parse(self, response):
        #test code
        response.meta["name"]="塘玄宗"

        if response.status == 404:
            return

        name = response.meta["name"]
        title = response.meta["title"] if "title" in response.meta else ""
        count = 0
        in_body_desc = ""
        for p in response.xpath("//p"):
            for l in p.xpath("following::*"):

                if self.isTrash(l.extract()):
                    continue
                print(l.extract())
                buffer = l.xpath("text()").extract_first()
                buffer = self.filter_text(buffer)
                in_body_desc = buffer if buffer else in_body_desc

                """
                for link in p.xpath("a"):
                    href = link.xpath("@href").extract_first()
                    content = link.xpath("text()").extract_first()
                    if href and href.split(".")[-1] in ["jpg", "JPG", "gif"]:
                        filename = self.get_name(in_body_desc, title, content, count, name)
                        href = urljoin(response.url, href)
                        # urllib.request.urlretrieve(href, self.folder + filename+".jpg")
                        with open(self.folder + "image.txt", 'a') as f:
                            f.write(filename + "," + href + "\n")
                            # yield {"name": filename, "href": href}


                    elif href and (content not in ["返回上一级"]):
                        if len(href.split(".")) == 0 or href.split(".")[-1] not in ["doc"]:
                            request = scrapy.Request(response.urljoin(href), callback=self.parse)
                            request.meta["title"] = content
                            request.meta["name"] = name
                            yield request
                            """





