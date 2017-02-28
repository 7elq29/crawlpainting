import scrapy

from urllib.parse import urljoin

class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = ["http://www.9610.com/xianqin/index.htm",
                  "http://www.9610.com/qinhan/1.htm",
                  "http://www.9610.com/weijin/1.htm",
                  "http://www.9610.com/suitang/1.htm",
                  "http://www.9610.com/song/index.htm",
                  "http://www.9610.com/yuan/index.htm",
                  "http://www.9610.com/ming/index.htm",
                  "http://www.9610.com/qing/1.htm",
                  "http://www.9610.com/jindai/index.htm",
                  "http://www.9610.com/dangdai/index.htm"]
    allowed_domains = ['www.9610.com']
    custom_settings = {
        'DEPTH_LIMIT': '5',
    }
    folder = "/Users/Ken/Downloads/image/"

    peoples = []

    def parse(self, response):
        if response.status == 404:
            return;
        content = response.xpath("//table")[0]
        for link in content.xpath("//a"):
            title = link.xpath('text()').extract_first()
            next_page = link.xpath('@href').extract_first()
            if next_page:
                request = scrapy.Request(response.urljoin(next_page), callback=self.parse_img)
                request.meta["name"] = title
                yield request

    def parse_img(self, response):
        if response.status == 404:
            return
        name = response.meta["name"]
        title = response.meta["title"] if "title" in response.meta else ""
        count = 0
        for link in response.xpath("//p/a"):
            href = link.xpath("@href").extract_first()
            content = link.xpath("text()").extract_first()
            if href and href.split(".")[-1] in ["jpg", "JPG", "gif"]:
                filename = ""
                if not content or content == "" or content.isdigit():
                    count += 1
                    filename = name + title + str(count)
                else:
                    filename = name + title + content.strip(' \t\n\r').replace('\n', "")
                href = urljoin(response.url, href)
                with open(self.folder + "image.txt", 'a') as f:
                    f.write(filename + "," + href + "\n")

            elif href and (content not in ["返回上一级"]):
                print(urljoin(response.url, href))
                if len(href .split(".")) == 0 or href.split(".")[-1] not in ["doc"]:
                    request = scrapy.Request(response.urljoin(href), callback=self.parse_img)
                    request.meta["title"] = content
                    request.meta["name"] = name
                    yield request




