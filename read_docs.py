import csv
import os
import re

import replaces_regexps as rr
from _datetime import datetime

"""
Чтение ЖСТ файла
"""


def read_jst(path):
    list_files = os.listdir(path)

    name_jst = 'table_ЖСТ P1_ЖСТ таблица_'
    jst_files = {}

    jst_dic = {}

    for file_name in list_files:
        if 'ЖСТ P1.csv' in file_name:
            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=';')

                for row in readed_file:
                    if row[11].isdigit():
                        line_number = row[3].strip()

                        for key in row[4]:
                            if not key.isdigit():
                                row[4] = row[4].replace(key, '')
                        zone = row[4]

                        jst_files[zone + "$" + line_number] = path + "\\table_data\\" + name_jst + \
                                                              row[11].strip() + ".csv"

            for line_zone in jst_files:

                with open(jst_files[line_zone], "r") as read_file:
                    readed_file = csv.reader(read_file, delimiter=";")

                    joint_number = 'n/d'
                    serial_number = 0

                    for row in readed_file:

                        row[1] = row[1].upper().replace('В', 'B').replace("3W", "BW").replace(' ', '').replace(':', '')

                        if 'W' in row[1] or 'FW' in row[1] or 'R' in row[1]:
                            serial_number += 1
                            joint_number = row[1].replace('FW', '').replace('BW', '').replace('BR', '')

                            jst_dic[line_zone + "$" + joint_number + "$" + str(serial_number)] = ['', '', '', '', '', '', '', '', '', '', '', '']


            for line_zone in jst_files:

                with open(jst_files[line_zone], "r") as read_file:
                    readed_file = csv.reader(read_file, delimiter=";")

                    joint_number = 'n/d'
                    serial_number = 0
                    for row in readed_file:
                        row[1] = row[1].upper().replace('В', 'B').replace("3W", "BW").replace(' ', '').replace(':', '')


                        if 'W' in row[1] or 'FW' in row[1] or 'R' in row[1]:
                            serial_number += 1
                            joint_number = row[1].replace('FW', '').replace('BW', '').replace('BR', '')

                        try:
                            if len(row[1]) < 30 and not row[1].isdigit():
                                if len(row[2].replace(' ', '')) == 4: # сбор клейм
                                    for temp in rr.template_for_replace:
                                        row[2] = row[2].replace(temp, rr.template_for_replace[temp])
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][0] += row[2].strip() + "$"

                                # Сбор свариваемых материалов
                                jst_dic[line_zone + "$" + joint_number + "$"
                                        + str(serial_number)][1] += row[3].strip() + "$"
                                # размеры элементов
                                if 'X' in row[4].upper().replace('Х', 'X'):
                                    row[4] = row[4].upper().replace('Х', 'X')
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][2] += row[4].replace(" ", "").replace(',', '.') + "$"
                                # дата сварки
                                if len(row[5].strip()) > 5:
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][3] += row[5].strip() + "$"
                                # способ сварки
                                if not row[6].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][4] += row[6].strip() + "$"
                                # сварочные материалы
                                if not row[7].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][5] += row[7].strip() + "$"
                                # темпер подогрева
                                if not row[8].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][6] += row[8].strip() + "$"
                                # контроль корня
                                if not row[9].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][7] += row[9].strip() + "$"
                                # НК PMI
                                if not row[10].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][8] += row[10].strip() + "$"
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][11] += row[10].strip() + "$"
                                # HK Твердость
                                if not row[13].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][9] += row[13].strip() + "$"
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][11] += row[10].strip() + "$"
                                # отметка ВИК
                                if not row[14].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][10] += row[14].strip() + "$"
                                # Заключения НК номера даты
                                if not row[15].isdigit():
                                    jst_dic[line_zone + "$" + joint_number + "$"
                                            + str(serial_number)][11] += row[15].strip() + "$"
                        except:
                            pass
    bad_keys = []
    for key in jst_dic:
        line = key.split("$")[1]
        zone = key.split("$")[0]
        joint = key.split("$")[2]
        serial_number_joint = key.split("$")[3]

        stigmas = [value for value in jst_dic[key][0].split("$") if value]

        welded_mats = [value for value in jst_dic[key][1].split("$") if value]

        sizes_mats = [value for value in jst_dic[key][2].split("$") if value]
        date_weld = ""
        try:
            date_weld = [value for value in jst_dic[key][3].split("$") if value][0]
            for word in date_weld:
                if not word.isdigit():
                    date_weld = date_weld.replace(word, '')
            date_weld = f'{date_weld[0:2]}.{date_weld[2:4]}.{date_weld[4:]}'
        except:
            bad_keys.append(key)

        try:
            way_weld = [value for value in jst_dic[key][4].split("$") if value][0]
            for temp in rr.replace_temlpate_for_way_weld:
                way_weld = way_weld.replace(temp, rr.replace_temlpate_for_way_weld[temp])
        except:
            bad_keys.append(key)

        welder_mats = [value for value in jst_dic[key][5].split("$") if value]

        temp_heating = [value for value in jst_dic[key][6].split("$") if value]
        root_control = [value for value in jst_dic[key][7].split("$") if value]
        vik_control = [value for value in jst_dic[key][10].split("$") if value]

        pmi_nk = [value for value in jst_dic[key][8].split("$") if value]
        ht_nk = [value for value in jst_dic[key][9].split("$") if value]
        nk_conkls = jst_dic[key][11].replace("$", " ")

        jst_dic[key] = [stigmas, welded_mats, sizes_mats, date_weld, way_weld, welder_mats,
                        temp_heating, root_control, pmi_nk, ht_nk, vik_control, nk_conkls]

        # print(key, welder_mats)
    for k in set(bad_keys):
        jst_dic.pop(k)

    return [jst_dic, line_zone]





"""
Чтение заключений НК
"""


def read_nk_cocl(path):
    list_files = os.listdir(path)

    vik_concls = {}
    pvk_concls = {}
    rt_concls = {}
    ut_concls = {}
    pmi_concls = {}


    # Чтение ВИК   vik_concls
    for file_name in list_files:
        if 'ВИК Р1.csv' in file_name:
            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if row[15].isdigit():
                        joint_numbers = row[5].split(" ")
                        zone_number = row[4].replace(' ', '')
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')

                        line_number = row[3]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers:
                            for joint_number in joint_numbers:
                                joint_number = joint_number.replace('Р', 'P')
                                vik_concls[zone_number + "$" + line_number + "$" + joint_number] = ['', '', '', '']

            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")

                for row in readed_file:
                    if row[15].isdigit():
                        number_concl = row[0].strip()
                        number_test = row[10].strip()
                        joint_numbers = row[5].split(" ")
                        stigmas = row[7].strip()

                        date_concl = row[1].strip()

                        zone_number = row[4].replace(' ', '')
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')

                        line_number = row[3]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers and stigmas and date_concl:
                            for joint_number in joint_numbers:
                                joint_number = joint_number.replace('Р', 'P')

                                vik_concls[zone_number + "$" + line_number + "$" + joint_number][0] += date_concl + "$"
                                vik_concls[zone_number + "$" + line_number + "$" + joint_number][1] += stigmas + "$"
                                vik_concls[zone_number + "$" + line_number + "$" + joint_number][2] += number_concl + "$"
                                vik_concls[zone_number + "$" + line_number + "$" + joint_number][3] += number_test + "$"

        # Чтение ПВК   pvk_concls
        if 'ПВК Р1.csv' in file_name:
            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if row[15].isdigit():
                        joint_numbers = row[5].split(" ")
                        zone_number = row[3].replace(' ', '')
                        stigmas = row[7].strip()
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')
                        line_number = row[2]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers:
                            for joint_number in joint_numbers:
                                pvk_concls[zone_number + "$" + line_number + "$" + joint_number] = ['', '', '', '']

            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")

                for row in readed_file:
                    if row[15].isdigit():
                        number_concl = row[0].strip()
                        number_test = row[10].strip()
                        joint_numbers = row[5].split(" ")
                        stigmas = row[7].strip()

                        date_concl = row[1].strip()

                        zone_number = row[3].replace(' ', '')
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')

                        line_number = row[2]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers and date_concl:
                            for joint_number in joint_numbers:
                                pvk_concls[zone_number + "$" + line_number + "$" + joint_number][0] += date_concl + "$"
                                pvk_concls[zone_number + "$" + line_number + "$" + joint_number][1] += stigmas + "$"
                                pvk_concls[zone_number + "$" + line_number + "$" + joint_number][2] += number_concl + "$"
                                pvk_concls[zone_number + "$" + line_number + "$" + joint_number][3] += number_test + "$"

        # Чтение РК
        if 'РТ Р1.csv' in file_name:
            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if row[16].isdigit():
                        joint_numbers = row[4].split(" ")
                        zone_number = row[10].replace(' ', '')
                        stigmas = row[6].strip()
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')
                        line_number = row[2]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers and stigmas:
                            for joint_number in joint_numbers:
                                rt_concls[zone_number + "$" + line_number + "$" + joint_number] = ['', '', '', '']

            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")

                for row in readed_file:
                    if row[16].isdigit():
                        number_concl = row[0].strip()
                        number_test = row[11].strip()
                        joint_numbers = row[4].split(" ")
                        stigmas = row[6].strip()

                        date_concl = row[1].strip()

                        zone_number = row[10].replace(' ', '')
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')

                        line_number = row[2]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers and stigmas and date_concl:
                            for joint_number in joint_numbers:
                                rt_concls[zone_number + "$" + line_number + "$" + joint_number][0] += date_concl + "$"
                                rt_concls[zone_number + "$" + line_number + "$" + joint_number][1] += stigmas + "$"
                                rt_concls[zone_number + "$" + line_number + "$" + joint_number][2] += number_concl + "$"
                                rt_concls[zone_number + "$" + line_number + "$" + joint_number][3] += number_test + "$"

        # Чтение УЗК
        if 'УЗК Р1.csv' in file_name:
            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if row[16].isdigit():
                        joint_numbers = row[5].split(" ")
                        zone_number = row[4].replace(' ', '')
                        stigmas = row[7].strip()
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')
                        line_number = row[2]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers and stigmas:
                            for joint_number in joint_numbers:
                                ut_concls[zone_number + "$" + line_number + "$" + joint_number] = ['', '', '', '']

            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")

                for row in readed_file:
                    if row[16].isdigit():
                        number_concl = row[0].strip()
                        number_test = row[10].strip()
                        joint_numbers = row[5].split(" ")
                        stigmas = row[7].strip()

                        date_concl = row[1].strip()

                        zone_number = row[4].replace(' ', '')
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')

                        line_number = row[2]
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        if zone_number and line_number and joint_numbers and stigmas and date_concl:
                            for joint_number in joint_numbers:
                                ut_concls[zone_number + "$" + line_number + "$" + joint_number][0] += date_concl + "$"
                                ut_concls[zone_number + "$" + line_number + "$" + joint_number][1] += stigmas + "$"
                                ut_concls[zone_number + "$" + line_number + "$" + joint_number][2] += number_concl + "$"
                                ut_concls[zone_number + "$" + line_number + "$" + joint_number][3] += number_test + "$"

        # Чтение PMI
        if 'Химсостав Р1.csv' in file_name:
            name_pmi_concl_data = 'table_Химсостав Р1_Исследование на хим. состав_'

            list_data = []

            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if row[26].isdigit():
                        number_concl = row[0].strip()
                        date_concl = row[1].strip()
                        zone_number = row[4].replace(' ', '')
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')
                        line_number = row[3].replace(' ', '')
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        number_test = row[7].strip()
                        joint_numbers = row[8].strip().split("@")
                        stigmas = row[10].strip()

                        # with open(path + "\\table_data\\" +
                        #           name_pmi_concl_data + row[12].strip() + ".csv") as read_file_data:
                        #     readed_file_data = csv.reader(read_file_data, delimiter=";")
                        #
                        #
                        #
                        #     for row_data in readed_file_data:
                        #         if 'оме' not in row_data[0]:
                        #             try:
                        #                 number_test = row_data[0].strip()
                        #                 joint_numbers = row_data[1].strip()
                        #                 stigmas = row_data[3].strip()
                        #             except:
                        #                 pass
                        #             list_data.append(number_test + "$" + joint_numbers + "$" + stigmas +
                        #                              "$" + date_concl + "$" + number_concl + "$" + line_number +
                        #                              "$" + zone_number)

            # for data in set(list_data):
            #     joint_number = data.split("$")[1]
            #     stigmas = data.split("$")[2]
            #     line_number = data.split("$")[5]
            #     zone_number = data.split("$")[6]

                        if zone_number and line_number and joint_numbers:
                            for joint_number in joint_numbers:
                                pmi_concls[zone_number + "$" + line_number + "$" + joint_number] = ['', '', '', '']

            # for data in set(list_data):
            #     number_test = data.split("$")[0]
            #     number_concl = data.split("$")[4]
            #
            #     joint_number = data.split("$")[1]
            #     stigmas = data.split("$")[2]
            #     date_concl = data.split("$")[3]
            #
            #     line_number = data.split("$")[5]
            #     zone_number = data.split("$")[6]

            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if row[26].isdigit():
                        number_concl = row[0].strip()
                        date_concl = row[1].strip()
                        zone_number = row[4].replace(' ', '')
                        for word in zone_number:
                            if not word.isdigit():
                                zone_number = zone_number.replace(word, '')
                        line_number = row[3].replace(' ', '')
                        for word in line_number:
                            if not word.isdigit():
                                line_number = line_number.replace(word, '')
                        line_number = f'{line_number[:1]}-{line_number[1:3]}-{line_number[3:]}'

                        number_test = row[7].strip()
                        joint_numbers = row[8].strip().split("@")
                        stigmas = row[10].strip()

                        if zone_number and line_number and joint_numbers:
                            for joint_number in joint_numbers:
                                pmi_concls[zone_number + "$" + line_number + "$" + joint_number][0] += date_concl + "$"
                                pmi_concls[zone_number + "$" + line_number + "$" + joint_number][1] += stigmas + "$"
                                pmi_concls[zone_number + "$" + line_number + "$" + joint_number][2] += number_concl + "$"
                                pmi_concls[zone_number + "$" + line_number + "$" + joint_number][3] += number_test + "$"


    # for i in pmi_concls:
    #     print(i, pmi_concls[i])
    return [vik_concls, pvk_concls, rt_concls, ut_concls, pmi_concls]


"""
чтение спецификаций и  актов входноо контроля
"""


def read_spec_akts(path):
    list_files_akts = os.listdir(path)

    name_spec_fason = 'table_Спецификация P1_Сведения о деталях_'
    name_spec_krep = 'table_Спецификация P1_Сведения о крепежных детялях и прокладках_'
    name_spec_pipe = 'table_Спецификация P1_Сведения о трубопроводах_'

    spec_files = {}
    akts_files = {}

    summary_akts_vk_line = {}
    summary_specs_line_list = {}

    # чтение фалов специфиаций и актов входного контроля
    for file_name in list_files_akts:
        if 'Спецификация P1.csv' in file_name:
            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=';')

                for row in readed_file:
                    if row[13].isdigit():
                        line_list = row[1].strip() + "-" + row[3].strip()
                        spec_files[line_list] = [path + "\\table_data\\" + name_spec_pipe + row[13] + ".csv",
                                                 path + "\\table_data\\" + name_spec_fason + row[13] + ".csv",
                                                 path + "\\table_data\\" + name_spec_krep + row[13] + ".csv"]

        if 'Перечень Актов ВК.csv' in file_name:
            with open(path + "\\" + file_name) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if row[8].isdigit():
                        akts_files[row[0]] = path + "\\table_data\\table_Перечень Актов ВК_Таблица 2_" + row[8] + ".csv"

    # сбор информации из актов ВК
    for line in akts_files:
        with open(akts_files[line]) as read_file:
            readed_file = csv.reader(read_file, delimiter=";")

            for row in readed_file:
                for temp in rr.template_for_replace:
                    row[0] = row[0].replace(temp, rr.template_for_replace[temp])
                    row[1] = row[1].replace(temp, rr.template_for_replace[temp])

                row[0] = row[0].replace(' ', '')
                row[1] = row[1].replace(' ', '')

                if 'ID' not in row[0].upper():
                    summary_akts_vk_line[row[0].strip()] = row[1].strip()

    # сбор данных из спецификаций
    for line_list in spec_files:

        summary_specs_line_list[line_list] = ''
        # Сведения о трубопроводах
        try:
            with open(spec_files[line_list][0]) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if 'ID' in row[0].upper():
                        row[0] = row[0].replace("ID", "ID ")
                        items = row[0].split(' ')
                        for item in items:
                            if item == '':
                                items.remove(item)

                        if items[0] == 'ID':
                            summary_specs_line_list[line_list] += items[1].strip() + '$'
        except:
            summary_specs_line_list[line_list] += f'Таблица сведений о трубопроводах не найдена. ' \
                                                  f'Необходима проверка.$'

        # Сведения о деталях
        try:
            with open(spec_files[line_list][1]) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if 'ID' in row[0].upper():
                        row[0] = row[0].replace("ID", "ID ")
                        items = row[0].split(' ')
                        for item in items:
                            if item == '':
                                items.remove(item)

                        if items[0] == 'ID':
                            summary_specs_line_list[line_list] += items[1].strip() + '$'
        except:
            summary_specs_line_list[line_list] += f'Таблица сведений о фасонных деталях не найдена.' \
                                                  f' Необходима проверка.$'

        # Сведения о крепежах
        try:
            with open(spec_files[line_list][2]) as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    if 'ID' in row[0].upper():
                        row[0] = row[0].replace("ID", "ID ")
                        items = row[0].split(' ')
                        for item in items:
                            if item == '':
                                items.remove(item)

                        if items[0] == 'ID':
                            summary_specs_line_list[line_list] += items[1].strip() + '$'
        except:
            summary_specs_line_list[
                line_list] += f'Таблица сведений о крепёжных деталях не найдена.' \
                              f' Необходима проверка.$'

    # возврат список  из словарей 0 -  данные из спецификаций, 1 - данные из актов ВК
    return [summary_specs_line_list, summary_akts_vk_line]


# Собираем информацию с ЖСР
def read_jsr_p1(path: str):
    jurnal_svarki = []
    jurnal_svarki_pvk = []
    quantity_joins = 0
    for filename in os.listdir(path + "\\table_data\\"):
        if "ЖСР" in filename:
            with open(f"{path}\\table_data\\{filename}", "r") as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                for row in readed_file:
                    word = row[11].replace("B", "В").replace("K", "К").replace("N", "И").replace("0", "о")\
                        .replace("З", "В").replace("3", "В")
                    if "ВИК" in word and "ПВК" not in word:
                        quantity_joins += 1
                        # номер линии
                        number_line = str(row[2].split(",")[0].replace(" ", ""))
                        number_line = (re.search(r'\(\d+\)(\d+-\d+-\d+)', number_line).group(1))
                        # Дата сварки
                        date_join = datetime.strptime(row[0].split()[0], "%d.%m.%Y").date()
                        # номер заключения ВИК
                        number_conclusion_vik = re.search(r'№\s*(\S+)', row[11]).group(1)
                        # результат заключения
                        result_support = row[12].replace(" ", "").replace("П", "н").replace("Т", "н")

                    if "ПВК" in word or "Годен" in word:
                        # номер стыка
                        if len(row[2]) > 1:
                            number_join = row[2].replace(" ", "").replace("/", "")
                        # Вся необходимая информация про ПВК
                        if "ПВК" in word:
                            number_conclusion_pvk = re.search(r'№\s*(\S+)', row[11]).group(1)
                            jurnal_svarki_pvk.append(number_conclusion_pvk)
                            number_join_pvk = number_join
                            jurnal_svarki_pvk.append(number_join_pvk)
                            number_line_pvk = number_line
                            jurnal_svarki_pvk.append(number_line_pvk)
                            result_support_pvk = result_support

                            result_support_pvk = result_support_pvk.strip().lower().replace("h", "н").replace("П", "н")

                            if result_support_pvk == "нет":
                                result_support_pvk = "годен"
                            else:
                                result_support_pvk = "не годен"

                            jurnal_svarki_pvk.append(result_support_pvk)
                            date_join_pvk = date_join
                            jurnal_svarki_pvk.append(date_join_pvk)

                        jurnal_svarki.append({"line": number_line,
                                              "joint": number_join, "weld_data": date_join,
                                              "vic_number": number_conclusion_vik,
                                              "result": result_support})

    # удаляем дубликаты словарей
    duplicates_removed = {}
    for dictionary in jurnal_svarki:
        joint = dictionary["joint"]
        if joint in duplicates_removed:
            continue
        else:
            duplicates_removed[joint] = dictionary

    result = list(duplicates_removed.values())

    return quantity_joins, jurnal_svarki_pvk, result


def read_vik_supports_p1(path: str):
    vik_supports_p1 = []
    quantity_joins_vik = 0
    for filename in os.listdir(path):
        if "ВИК на опоры" in filename:
            with open(f"{path}\\{filename}", "r") as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                next(readed_file)
                for row in readed_file:
                    # номер заключения
                    number_supports_vik = row[0]
                    # дата заключения
                    date_supports_vik = datetime.strptime(row[1], "%d.%m.%Y").date()
                    # линия указанная в заключение
                    line_supports_vik = row[3].strip()
                    # print(line_supports_vik)
                    # номер сварного соединения в заключение
                    number_join_vik = row[6].split(" ")
                    quantity_joins_vik = len(number_join_vik)

                    # результат заключения
                    result_supports_vik = row[12].split(" ")
                    for element, result in zip(number_join_vik, result_supports_vik):
                        vik_supports_p1.append({"line_vik": line_supports_vik,
                                                "join_vik": element, "date_conclusion_vik": date_supports_vik,
                                                "number_conclusion_vik":number_supports_vik, "result_vik": result})

    return vik_supports_p1, quantity_joins_vik


def read_pvk_supports_p1(path: str):
    pvk_supports_p1 = []
    quantity_joins_pvk = 0
    for filename in os.listdir(path):
        if "ПВК на опоры" in filename:
            with open(f"{path}\\{filename}", "r") as read_file:
                readed_file = csv.reader(read_file, delimiter=";")
                next(readed_file)
                for row in readed_file:
                    quantity_joins_pvk += 1
                    # номер заключения
                    number_supports_pvk = re.sub(r"[^A-Za-z0-9]", "", row[0])
                    pvk_supports_p1.append(number_supports_pvk)
                    # линия указанная в заключение
                    line_supports_pvk = row[3]
                    pvk_supports_p1.append(line_supports_pvk)
                    # номер сварного соединения в заключение
                    number_join_pvk = row[6].replace(" ", "")
                    pvk_supports_p1.append(number_join_pvk)
                    # результат заключения
                    result_supports_pvk = row[12].strip().lower()
                    pvk_supports_p1.append(result_supports_pvk)
                    # дата заключения
                    date_supports_pvk = datetime.strptime(row[1], "%d.%m.%Y").date()
                    pvk_supports_p1.append(date_supports_pvk)

    return pvk_supports_p1, quantity_joins_pvk


# jst = read_jst(r'C:\Users\IgnatenkoIA\Desktop\WORK\ATOM\P1\for_test_aict_p2\44010_4-40-411317_2.1')
#
#
# for key in jst:
#
#     print(key, jst[key][8])



# a = read_nk_cocl(r'C:\Users\IgnatenkoIA\Desktop\WORK\ATOM\P1\for_test_aict_p2\02.02.23+\test')
# vik = a[0]
# pvk = a[1]
# rt = a[2]
# ut = a[3]
# pmi = a[4]
#
# for i in vik:
#     print(i, vik[i])
# print()
# for i in pvk:
#     print(i, pvk[i])
# print()
# for i in rt:
#     print(i, rt[i])
# print()
# for i in ut:
#     print(i, ut[i])
# print()
# for i in pmi:
#     print(i, pmi[i])
# print()



























