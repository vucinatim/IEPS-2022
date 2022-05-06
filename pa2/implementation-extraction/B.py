from lxml import html, etree
import printer


def xpath_extract(sites):
    for idx, site in enumerate(sites):
        for p_name, p_html in site.items():
            tree = html.fromstring(p_html)

            # ---- overstock.com ----
            if idx == 0:
                title = tree.xpath("//tr[@bgcolor]//a/b/text()")
                content = tree.xpath('//tr[@bgcolor]//span[@class="normal"]/text()')
                list_price = tree.xpath("//tr[@bgcolor]//s/text()")
                price = tree.xpath('//tr[@bgcolor]//span[@class="bigred"]/b/text()')
                saving_str = tree.xpath(
                    '//tr[@bgcolor]//span[@class="littleorange"]/text()'
                )
                saving, saving_percent = [], []
                for s in saving_str:
                    a, b = s.split(" ")
                    saving.append(a)
                    saving_percent.append(b)

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
                title = tree.xpath("//header//h1/text()")
                subtitle = tree.xpath('//header//*[@class="subtitle"]/text()')
                lead = tree.xpath('//header//*[@class="lead"]/text()')
                content = [" ".join(tree.xpath("//article//p/text()"))]
                author = tree.xpath('//*[@class="author-name"]/text()')
                published_time = tree.xpath('//*[@class="publish-meta"]/text()')

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

            # //*[@class="price"]/a/text()
            # ---- ceneje.si ----
            if idx == 2:
                title = tree.xpath('//h1[@class="top-offer__name"]/text()')
                top_price = tree.xpath('//*[contains(@class, "priceB")]/text()')
                top_disc_price = [
                    " ".join(tree.xpath('//*[@class="top-offer__discount"]/*/text()'))
                ]
                item_seller = tree.xpath("//@data-sellername")
                item_price = tree.xpath('//*[@class="price-value"]/text()[2]')
                item_price.extend(
                    tree.xpath('//*[contains(@class, "greyPrice")]/a/text()')
                )
                discounts = tree.xpath('//*[@class="discountPrice"]')
                item_disc_price = [" ".join(d.xpath("*/text()")) for d in discounts]
                item_disc_price.extend(
                    ["" for _ in range(len(item_seller) - len(item_disc_price))]
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
