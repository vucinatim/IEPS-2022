class Site:
    def __init__(self, domain, robots_content, sitemap_content):
        self.domain = domain
        self.robots_content = robots_content
        self.sitemap_content = sitemap_content

    def __str__(self):
        p1 = f"domain: {self.domain} \n"
        p2 = f"robots_content: {len(self.robots_content) if self.robots_content else 'None'} \n"
        p3 = f"sitemap_content: {len(self.sitemap_content) if self.sitemap_content else 'None'}"
        return p1 + p2 + p3

    def to_tuple(self):
        return (self.domain, self.robots_content, self.sitemap_content)


class Page:
    def __init__(
        self,
        site,
        type_code,
        url,
        html_content,
        status_code,
        accessed_time,
        images,
        page_data,
        links,
    ):
        self.site = site
        self.type_code = type_code
        self.url = url
        self.html_content = html_content
        self.status_code = status_code
        self.accessed_time = accessed_time
        self.images = images
        self.page_data = page_data
        self.links = links

    def __str__(self):
        p1 = f"site: {self.site} \n"
        p2 = f"type_code: {self.type_code} \n"
        p3 = f"url: {self.url} \n"
        p4 = f"html_content: {len(self.html_content) if self.html_content else 'None'} \n"
        p5 = f"status_code: {self.status_code} \n"
        p6 = f"accessed_time: {self.accessed_time} \n"
        p7 = f"images: {len(self.images) if self.images else 'None'} \n"
        p8 = f"page_data: {self.page_data} \n"
        p9 = f"links: {len(self.links) if self.links else 0}"
        return p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9

    def to_tuple(self):
        return (
            self.type_code,
            self.url,
            self.html_content,
            self.status_code,
            self.accessed_time,
        )


class Image:
    def __init__(self, page, filename, content_type, data, accessed_time):
        self.page = page
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.accessed_time = accessed_time

    def __str__(self):
        p1 = f"page: {self.page} \n"
        p2 = f"filename: {self.filename} \n"
        p3 = f"content_type: {self.content_type} \n"
        p4 = f"accessed_time: {self.accessed_time}"
        return p1 + p2 + p3 + p4

    def to_tuple(self):
        return (
            self.filename,
            self.content_type,
            self.data,
            self.accessed_time,
        )


class PageData:
    def __init__(self, page, data_type_code, data):
        self.page = page
        self.data_type_code = data_type_code
        self.data = data

    def __str__(self):
        p1 = f"page: {self.page} \n"
        p2 = f"data_type_code: {self.data_type_code}"
        return p1 + p2

    def to_tuple(self):
        return (self.data_type_code, self.data)


class Link:
    def __init__(self, from_page, to_page):
        self.from_page = from_page
        self.to_page = to_page

    def __str__(self):
        p1 = f"from_page: {self.from_page} \n"
        p2 = f"to_page: {self.to_page}"
        return p1 + p2

    def to_tuple(self):
        return (self.from_page, self.to_page)


class FrontierEntry:
    def __init__(
        self, src_url, dest_url, crawled=False, fetched=False, processed=False
    ):
        self.src_url = src_url
        self.dest_url = dest_url
        self.crawled = crawled
        self.fetched = fetched
        self.processed = processed

    def __str__(self):
        p1 = f"src_url: {self.src_url} \n"
        p2 = f"dest_url: {self.dest_url} \n"
        p3 = f"crawled: {self.crawled} \n"
        p4 = f"fetched: {self.fetched} \n"
        p5 = f"fetched: {self.processed}"
        return p1 + p2 + p3 + p4 + p5

    def to_tuple(self):
        return (self.src_url, self.dest_url, self.crawled, self.fetched, self.processed)


class Error:
    def __init__(self, url, message, accessed_time):
        self.url = url
        self.message = message
        self.accessed_time = accessed_time

    def __str__(self):
        p1 = f"url: {self.url} \n"
        p2 = f"message: {self.message} \n"
        p3 = f"accessed_time: {self.accessed_time}"
        return p1 + p2 + p3

    def to_tuple(self):
        return (self.url, self.message, self.accessed_time)