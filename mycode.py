import csv
from datetime import date

# import xlrd
needed_items = []


# needed_backpacks = []

# Here we create a class for each pricelist, so that we can address its logic with further variables input
class Zoomos:
    # initialize by writing a list of relevant items passed by brand.
    # i've implemented a feature to check if the brand is in list and it assumes it was misspelled.
    def __init__(self, *brands):
        for brand in brands:
            temp_brand_list = []
            with open("zoomos.csv") as zoomos_price:
                zoomos_dict = csv.DictReader(zoomos_price, delimiter=";")
                for row in zoomos_dict:
                    temp_brand_list.append(row["Бренд"])
                    if row["Бренд"] == brand:
                        needed_items.append(row)
            if brand not in temp_brand_list:
                print(f"------>> ВНИМАНИЕ!!! Бренд {brand} не в списке! Проверяем написание!")
            else:
                print(f"Бренд {brand} добавлен в обработку успешно")
        print("""
        ===================================================\n
        Генерация списка завершена. Ищите .txt файл в папке\n
        ===================================================\n
        """)

    # in case we want to read the dictionary w/o any missing fields and garbage
    def clear_list(self):
        temp_list = []
        for item in needed_items:
            temp_needed_items = {}
            for k, v in item.items():
                if item[k] is None or item[k] == "":
                    continue
                else:
                    temp_needed_items.update({k: v})
            temp_list.append(temp_needed_items)
        return temp_list

    # here we seek for items that miss the supplier's offer and advise us to correct that
    # i would also like to add the feature of multiple sellers input, but currently i'm afraid
    # it is going to loop, so temporary input supposes just one str(Name)
    def missing_offer(self, *suppliers):
        missing_offer = []
        result = ""
        for item in needed_items:
            for supplier in suppliers:
                if supplier not in list(item.values()):
                    missing_offer.append(item)
        for position in missing_offer:
            result += "Товар {категория} {бренд} {модель} отсутствует у поставщика!\n".format(
                категория=position["Категория"], бренд=position["Бренд"], модель=position["Модель"])
        return result

    # The method below compares the supplier and seller price and outputs an advice.
    # due to the practical purpose of this script - I am going to format the output in a way useful for dayjob
    # Meanwhile any outcome can be predicted and returned as strings
    # There was a huge issue here with building the correspondence between supplier's name and price
    # due to how zoomos.csv is built
    # I invented somewhat logic based on previous decision and it now works correctly (Up until offers < 100)
    # But I suspect that it has to be done much easier and more universally
    # Eventually it turned out that price correction kinda does all the tricks. Gotta develop it or break into methods.

    def price_correction(self, supplier, seller):
        better_price = ""
        worse_price = ""
        same_price = ""
        superior_price = ""
        error_price = ""
        for item in needed_items:
            price_supplier = 0
            price_seller = 0
            for k, v in item.items():
                if v == supplier:
                    if len(k) % 2 == 0:
                        price_supplier = item["Цена {number}".format(number=k[-2:])]
                    else:
                        price_supplier = item["Цена{number}".format(number=k[-2:])]
                if v == seller:
                    if len(k) % 2 == 0:
                        price_seller = item["Цена {number}".format(number=k[-2:])]
                    else:
                        price_seller = item["Цена{number}".format(number=k[-2:])]
            if price_supplier != 0 and price_seller != 0:
                if str(price_supplier) < str(price_seller):
                    worse_price += "{supplier} -- {brand} {item} - БОЛЕЕ НИЗКАЯ ЦЕНА КОНКУРЕНТА - {price} // наша цена {price_seller}\n".format(
                        supplier=supplier,
                        price_seller=price_seller,
                        brand=item["Бренд"],
                        price=price_supplier,
                        item=item["Модель"])
                if str(price_supplier) > str(price_seller):
                    better_price += "{supplier} -- {brand} {item} - НАША ЦЕНА ЛУЧШЕ - {price} // наша цена {price_seller}\n".format(
                        supplier=supplier,
                        price_seller=price_seller,
                        brand=item["Бренд"],
                        price=price_supplier,
                        item=item["Модель"])
                if str(price_supplier) == str(price_seller):
                    same_price += "{supplier} -- {brand} {item} - !ОДИНАКОВАЯ ЦЕНА! - {price} // наша цена {price_seller}\n".format(
                        supplier=supplier,
                        price_seller=price_seller,
                        brand=item["Бренд"],
                        price=price_supplier,
                        item=item["Модель"])
            elif price_supplier == 0:
                superior_price += "{supplier} -- {brand} {item} - НЕТ ПРЕДЛОЖЕНИЯ! - {price} // наша цена {price_seller}\n".format(
                    supplier=supplier,
                    price_seller=price_seller,
                    brand=item["Бренд"],
                    price=price_supplier,
                    item=item["Модель"])
            elif price_seller == 0:
                error_price += "Где-то критическая ошибочка, друг!"
        result = worse_price + "\n" + better_price + "\n" + same_price + "\n" + superior_price + "\n" + error_price
        return result


# if this is called it creates a big result and writes a txt "Полный отчет {date}"
def full_report(competitor, *brands):
    zoomos = Zoomos(*brands)
    with open("Полная проверка на дату {date}.txt".format(date=date.today()), "w") as output:
        output.write(zoomos.price_correction(competitor, "4PLAY"))


# if this is called it creates a small result and writes a txt "Отчет {date}"
def report(competitor, *brands):
    zoomos = Zoomos(*brands)
    with open("Проверка на дату {date}.txt".format(date=date.today()), "w") as output:
        output.write(zoomos.missing_offer(competitor, "4PLAY"))

# TESTING SECTION BELOW:

# compare_brands = Zoomos("Razer", "Logitech", "Memilo", "Red Square")
# print(compare_brands.price_correction("5 элемент", "4PLAY"))
# print(compare_brands.missing_offer("X-Core"))
# print(compare_brands.clear_list())
# print(needed_items)
# full_report("4PLAY", "Razer")
# report("X-Core", "Razer")


###############################################################################
# the section below is still work in progress in search for comparison logic
# between given csv and xls
###############################################################################


# #Exel file section for backpacks
# book = xlrd.open_workbook("thule.xls")
# print("The number of worksheets is {0}".format(book.nsheets))
# print("Worksheet name(s): {0}".format(book.sheet_names()))
# sh = book.sheet_by_index(0)
# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
# print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
#
# # for row in range(sh.nrows):
# #     print("{}".format(sh.cell_value(rowx=row, colx = 0)))
#
# # defining the range of rows to work with
# with open("zoomos.csv") as price1:
#     price1_dict = csv.DictReader(price1, delimiter=";")
#     for row in price1_dict:
#         if row["Бренд"] == "Thule":
#             needed_backpacks.append(row)
#
# # defining the rows range to make the .xls usable
# def thule_row():
#     for row in range(sh.nrows):
#         if sh.cell_value(rowx = row, colx = 0) == "Thule":
#             return row
#
# # this was supposed to count the matching % of the name, but did not really work out.
# # need to develop another comparison logic or move to another idea
# def count_match(zoomos_backpack, thule_backpack):
#     count = 0
#     for charachter in zoomos_backpack.lower():
#          if charachter in thule_backpack.lower():
#             count += 1
#     return count / (len(zoomos_backpack) / 100)
# a = "Paramount 24L PARABP-2116 (бежевый)"
# b = "PARABP2116TW Рюкзак для ноутбука Thule Paramount Backpack 24L, бежевый, 3204488"
# # even 98% match does not really match with the appropriate position in price :(
# for backpacks in needed_backpacks:
#     for row in range(thule_row(), sh.nrows, 1):
#         if count_match(backpacks["Модель"], sh.cell_value(rowx = row, colx = 1)) >= 98:
#             print("Found it! {thule} = {memes}".format(thule = sh.cell_value(rowx = row, colx = 1), memes = backpacks["Модель"]))
#