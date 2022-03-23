# TODO: Add methods for a DB interface
# These classes can also be modified for DB use


class Site:
    def __init__(self, domain, robots_content, sitemap_content):
        self.domain = domain
        self.robots_content = robots_content
        self.sitemap_content = sitemap_content

    def __str__(self):
        p1 = f"Domain: {self.domain} \n"
        p2 = f"Robots: {self.robots_content[:20] if self.robots_content else 'None'} \n"
        p3 = f"Sitemap: {self.sitemap_content[:20] if self.sitemap_content else 'None'}"
        return p1 + p2 + p3

    def db_create_site(self):
        raise NotImplementedError


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
    ):
        self.site = site
        self.type_code = type_code
        self.url = url
        self.html_content = html_content
        self.status_code = status_code
        self.accessed_time = accessed_time
        self.images = images
        self.page_data = page_data

    def __str__(self):
        p1 = f"Site: {self.site} \n"
        p2 = f"Type: {self.type_code} \n"
        p3 = f"URL: {self.url} \n"
        p4 = f"HTML: {len(self.html_content) if self.html_content else 'None'} \n"
        p5 = f"Status: {self.status_code} \n"
        p6 = f"Time: {self.accessed_time} \n"
        p7 = f"Images: {len(self.images) if self.images else 'None'} \n"
        p8 = f"PageData: {self.page_data}"
        return p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8

    def db_create_page(self):
        raise NotImplementedError

    def db_create_link_to(self, url):
        raise NotImplementedError

    def db_compare_page_content(self):
        raise NotImplementedError


class Image:
    def __init__(self, filename, content_type, data, accessed_time):
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.accessed_time = accessed_time

    def db_create_image(self):
        raise NotImplementedError


class PageData:
    def __init__(self, data_type_code, data):
        self.data_type_code = data_type_code
        self.data = data

    def db_create_page_data(self):
        raise NotImplementedError