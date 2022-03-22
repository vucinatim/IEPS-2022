class Site:
    def __init__(self, domain, robots_content, sitemap_content):
        self.domain = domain
        self.robots_content = robots_content
        self.sitemap_content = sitemap_content
        self.pages = []

    def add_page(self, page):
        self.pages.append(page)


class Page:
    def __init__(
        self,
        type_code,
        url,
        html_content,
        status_code,
        accessed_time,
        images,
        from_page,
    ):
        self.type_code = type_code
        self.url = url
        self.html_content = html_content
        self.status_code = status_code
        self.accessed_time = accessed_time
        self.images = images
        self.from_page = from_page


class Image:
    def __init__(self, filename, content_type, data, accessed_time):
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.accessed_time = accessed_time