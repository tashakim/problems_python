import scrapy

class RedditSpider(scrapy.Spider):
	name = "reddit"
	start_urls = ["https://www.reddit.com/r/gardening/",
	"https://www.reddit.com/r/gardening/?count=25&after=t3_4vja10"
	]


	def parse(self, response):
		links = response.xpath("//img/@src")
		html = ""

		for link in links:
			url = link.get()

			if any(extension in url for extension in [".jpg"]):
				html += """<a href = "{url}" 
				target = "_blank">
				<img src="{url}" height = "33%"
				width = "33%"/>
				<a/>""".format(url = url)

				with open("frontpage.html", "a") as page:
					page.write(html)
					page.close()