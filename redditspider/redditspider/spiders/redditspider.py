import scrapy

class RedditSpider(scrapy.Spider):
	name = "redditspyder"
	start_urls = ["https://www.reddit.com/r/dogpictures/",
	"https://www.reddit.com/r/catpictures/"]
	# add urls here


	def parse(self, response):
		links = response.xpath("//img/@src")
		# creates new html page
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