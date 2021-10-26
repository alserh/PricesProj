import csv
from datetime import date
import xlrd
needed_keyboards = []
needed_backpacks = []
# we convert the total offers file with competitors to required format
with open("zoomos.csv") as price1:
    price1_dict = csv.DictReader(price1, delimiter=";")
    for row in price1_dict:
        if row["Бренд"] == "Varmilo" \
                or row["Бренд"] == "Durgod" \
                or row["Бренд"] == "Leopold" \
                or row["Бренд"] == "Geekboards":
            needed_keyboards.append(row)

# we seek for items that miss the offer of the supplier and list them for further exclusion
def missing_list():
    bad_list = []
    for items in needed_keyboards:
        if "X-Core" not in list(items.values()):
            bad_list.append(items)
    return bad_list

# # we are checking the price offer with the supplier for further correction
def price_correction():
    text = ""
    for items in needed_keyboards:
        supply = 0
        seller = 0
        for k, v in items.items():
            if v == "X-Core":
                supply = items["Цена{number}".format(number = k[-2:])]
            if v == "4PLAY":
                seller = items["Цена{number}".format(number = k[-2:])]
        if supply != seller:
            text += "{brand} {keyboard} - правильная цена - {price}\n".format(brand = items["Бренд"],
                                                                              price = supply,
                                                                              keyboard = items["Модель"])
    return text

#Exel file section for backpacks
book = xlrd.open_workbook("thule.xls")
print("The number of worksheets is {0}".format(book.nsheets))
print("Worksheet name(s): {0}".format(book.sheet_names()))
sh = book.sheet_by_index(0)
print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))

# for row in range(sh.nrows):
#     print("{}".format(sh.cell_value(rowx=row, colx = 0)))

# defining the range of rows to work with
with open("zoomos.csv") as price1:
    price1_dict = csv.DictReader(price1, delimiter=";")
    for row in price1_dict:
        if row["Бренд"] == "Thule":
            needed_backpacks.append(row)
# print(needed_backpacks)

def thule_row():
    for row in range(sh.nrows):
        if sh.cell_value(rowx = row, colx = 0) == "Thule":
            return row

# print(sorted(needed_backpacks[0]["Модель"][5:].lower())


def count_match(zoomos_backpack, thule_backpack):
    count = 0
    for charachter in zoomos_backpack.lower():
         if charachter in thule_backpack.lower():
            count += 1
    return count / (len(zoomos_backpack) / 100)
a = "Paramount 24L PARABP-2116 (бежевый)"
b = "PARABP2116TW Рюкзак для ноутбука Thule Paramount Backpack 24L, бежевый, 3204488"

print(count_match(a,b))

for backpacks in needed_backpacks:
    for row in range(thule_row(), sh.nrows, 1):
        if count_match(backpacks["Модель"], sh.cell_value(rowx = row, colx = 1)) >= 98:
            print("Found it! {thule} = {memes}".format(thule = sh.cell_value(rowx = row, colx = 1), memes = backpacks["Модель"]))
#

# Output section
with open("Проверка на дату {date}.txt".format(date = date.today()), "w") as output:
    output.write("""
    =============================
    = ВНИМАНИЕ!! НЕТ У X-CORE!! =
    =============================\n\n""")
    for item in missing_list():
        output.write("{brand} {model} - нет у XCore!\n".format(brand = item["Бренд"], model = item["Модель"]))
    output.write("\n==============================================================\n")
    output.write("""
    =================================
    = КОРРЕКТИРОВКА ЦЕН (ЕСЛИ НУЖНО)=
    =================================\n\n""")
    output.write(price_correction())

