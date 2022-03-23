class Site:
    def __init__(self, domain, robots_content, sitemap_content):
        self.domain = domain
        self.robots_content = robots_content
        self.sitemap_content = sitemap_content
        self.pages = []

    def __str__(self):
        p1 = f"Domain: {self.domain} \n"
        p2 = f"Robots: {self.robots_content[:20] if self.robots_content else 'None'} \n"
        p3 = f"Sitemap: {self.sitemap_content[:20] if self.sitemap_content else 'None'} \n"
        p4 = f"pages: {len(self.pages)} \n"
        return p1 + p2 + p3 + p4

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

    def __str__(self):
        p1 = f"Type: {self.type_code} \n"
        p2 = f"URL: {self.url} \n"
        p3 = f"Status: {self.status_code} \n"
        p4 = f"Time: {self.accessed_time} \n"
        p5 = f"Images: {len(self.images)} \n"
        p6 = f"Links: {len(self.from_page)}"
        return p1 + p2 + p3 + p4 + p5 + p6


class Image:
    def __init__(self, filename, content_type, data, accessed_time):
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.accessed_time = accessed_time