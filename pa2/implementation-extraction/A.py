import regex
import printer


def re_extract(sites):
    for idx, site in enumerate(sites):
        for p_name, p_html in site.items():

            # ---- overstock.com ----
            if idx == 0:
                title = regex.findall(
                    r"(?<=<a.*?<b>).*?\n.*?(?=<\/b><\/a><br>)", p_html
                )
                content = regex.findall(
                    r'(?<="normal">).*?(?=<br>)', p_html, flags=regex.S
                )
                list_price = regex.findall(r"(?<=<s>)\$\d*,?\d*\.?\d*", p_html)
                price = regex.findall(r"(?<=<b>)\$\d*,?\d*\.?\d*", p_html)
                saving = regex.findall(r'(?<="littleorange">)\$\d*,?\d*\.?\d*', p_html)
                saving_percent = regex.findall(r"\(\d*%\)", p_html)

                printer.print_overstock(
                    (
                        title,
                        content,
                        list_price,
                        price,
                        saving,
                        saving_percent,
                    ),
                    name=p_name,
                )

            # ---- rtvslo.si ----
            if idx == 1:
                title = regex.findall(
                    r"(?<=news-container.*?<h1>).*(?=<\/h1>)", p_html, flags=regex.S
                )
                subtitle = regex.findall(r'(?<=subtitle">).*?(?=<\/)', p_html)
                lead = regex.findall(r'(?<=lead">).*?(?=<\/)', p_html, flags=regex.S)
                content = regex.findall(
                    r'(?<=<article.*?<p.*?>).*?(?=<div class="gallery")',
                    p_html,
                    flags=regex.S,
                )
                author = regex.findall(r'(?<=author-name">).*?(?=<\/)', p_html)
                published_time = regex.findall(
                    r'(?<=publish-meta">\n\t*?)\d.*?(?=<br)', p_html
                )

                printer.print_rtvslo(
                    (
                        title,
                        subtitle,
                        lead,
                        content,
                        author,
                        published_time,
                    ),
                    name=p_name,
                )

            # ---- ceneje.si ----
            if idx == 2:
                title = regex.findall(
                    r'(?<=<h1 class="top-offer__name">\n\s).*?(?=\n\s<\/h1>)',
                    p_html,
                    flags=regex.S,
                )
                top_price = regex.findall(
                    r'(?<=top-offer__grid.*?priceB">\n\s).*?(?=\n\s<\/div>)',
                    p_html,
                    regex.S,
                )
                top_disc_price = regex.findall(
                    r'(?<=top-offer__discount">\n\s).*?(?=\n\s<\/div>)',
                    p_html,
                    regex.S,
                )
                item_seller = regex.findall(r'(?<=data-sellername=").*?(?=")', p_html)
                item_price = regex.findall(
                    r"(?<=data-cclass.*)\d*\.?\d{1,3},\d{2}\s.\n",
                    p_html,
                    flags=regex.S,
                )
                item_disc_price = regex.findall(
                    r'(?<=discountPrice">).*?(?=<\/div>)',
                    p_html,
                    flags=regex.S,
                )

                printer.print_ceneje(
                    (
                        title,
                        top_price,
                        top_disc_price,
                        item_seller,
                        item_price,
                        item_disc_price,
                    ),
                    name=p_name,
                )
