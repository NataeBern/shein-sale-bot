from bs4 import BeautifulSoup
import requests
import json


def get_first_inf():
    for page in range(1, 511):
        URL = f'https://ru.shein.com/sale/RU-New-In-Sale-sc-00509637.html?ici=ru_tab01navbar02menu04dir01&src_module=topcat&src_tab_page_id=page_select_class1691954790958&src_identifier=fc%3DWomen%60sc%3DРАСПРОДАЖА%60tc%3DСПЕЦИАЛЬНЫЕ%20ПРЕДЛОЖЕНИЯ%60oc%3DНовые%20Скидки%60ps%3Dtab01navbar02menu04dir01%60jc%3DitemPicking_00509637&srctype=category&userpath=category-РАСПРОДАЖА-Новые-Скидки&page={page}'
        req = requests.get(url=URL)

        soup = BeautifulSoup(req.text, 'lxml')
        links_to_products = soup.find_all('a', class_='S-product-item__img-container j-expose__product-item-img')

        inf_dict = {}

        for links in links_to_products:
            link = f'https://ru.shein.com/{links.get("href")}'
            req_in_link = requests.get(url=link)
            soup_in_link = BeautifulSoup(req_in_link.text, 'lxml')
            product_information = soup_in_link.find_all('div', class_='product-intro__info')

            for information in product_information:
                name_inf = information.find('h1').text.strip().replace('"', '')
                dis_prices_inf = information.find('div', class_='discount from')
                prices_inf = information.find('del', class_='del-price').text.strip()
                discounts_inf = information.find('span', class_='discount-label').text.strip()
                img_inf = f'https:{links.find("img").get("data-src")}'

                article_id = img_inf.split('/')[-1]
                article_id = article_id[:-22]

                inf_dict[article_id] = {
                        'name_inf': name_inf,
                        'dis_prices_inf': dis_prices_inf['aria-label'],
                        'prices_inf': prices_inf,
                        'discounts_inf': discounts_inf,
                        'img_inf': img_inf,
                        'link': link
                    }


        with open('inf_dict.json', 'w') as file:
            json.dump(inf_dict, file, indent=6, ensure_ascii=False)


def check_inf_update():
    with open('inf_dict.json') as file:
        inf_dict = json.load(file)

    for page in range(1, 51):
            URL = f'https://ru.shein.com/sale/RU-New-In-Sale-sc-00509637.html?ici=ru_tab01navbar02menu04dir01&src_module=topcat&src_tab_page_id=page_select_class1691954790958&src_identifier=fc%3DWomen%60sc%3DРАСПРОДАЖА%60tc%3DСПЕЦИАЛЬНЫЕ%20ПРЕДЛОЖЕНИЯ%60oc%3DНовые%20Скидки%60ps%3Dtab01navbar02menu04dir01%60jc%3DitemPicking_00509637&srctype=category&userpath=category-РАСПРОДАЖА-Новые-Скидки&page={page}'
            req = requests.get(url=URL)

            soup = BeautifulSoup(req.text, 'lxml')
            links_to_products = soup.find_all('a', class_='S-product-item__img-container j-expose__product-item-img')

            fresh_inf_dict = {}

            for links in links_to_products:
                link = f'https://ru.shein.com/{links.get("href")}'
                req_in_link = requests.get(url=link)
                soup_in_link = BeautifulSoup(req_in_link.text, 'lxml')
                product_information = soup_in_link.find_all('div', class_='product-intro__info')

                for information in product_information:
                    img_inf = f'https:{links.find("img").get("data-src")}'
                    article_id = img_inf.split('/')[-1]
                    article_id = article_id[:-22]

                    if article_id in inf_dict:
                        continue
                    else:
                        link = f'https://ru.shein.com/{links.get("href")}'
                        name_inf = information.find('h1').text.strip().replace('"', '')
                        dis_prices_inf = information.find('div', class_='discount from')
                        prices_inf = information.find('del', class_='del-price').text.strip()
                        discounts_inf = information.find('span', class_='discount-label').text.strip()

                        inf_dict[article_id] = {
                            'name_inf': name_inf,
                            'dis_prices_inf': dis_prices_inf['aria-label'],
                            'prices_inf': prices_inf,
                            'discounts_inf': discounts_inf,
                            'img_inf': img_inf,
                            'link': link
                        }

                        fresh_inf_dict[article_id] = {
                            'name_inf': name_inf,
                            'dis_prices_inf': dis_prices_inf['aria-label'],
                            'prices_inf': prices_inf,
                            'discounts_inf': discounts_inf,
                            'img_inf': img_inf,
                            'link': link
                        }

                with open('inf_dict.json', 'w') as file:
                    json.dump(inf_dict, file, indent=6, ensure_ascii=False)

                return fresh_inf_dict

def main():
    get_first_inf()
    check_inf_update()


if __name__ == '__main__':
    main()