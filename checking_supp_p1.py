import os
import csv
import xlsxwriter
from pprint import pprint
from _datetime import datetime
import read_docs as rd

def checking_jsr_vik(path: str):
    quantity_joints, jurnal_svarki_pvk, result = rd.read_jsr_p1(path)
    vik, quantity_joins_vik = rd.read_vik_supports_p1(path)
    result_chk = ["Проверка ЖСР опоры с заключениеми НК"]
    temporary = []
    # Считаем % контроля ВИК
    if quantity_joints == quantity_joins_vik:
        result_chk.append("% контроля ВИК набран")
    else:
        result_chk.append(f'Всего {quantity_joints} стыков по ЖСР, предоставлено ВИК на {quantity_joins_vik}')
    for element, row in zip(result, vik):
        if element.get("line") in row.get("line_vik"):
            temporary.append(f"{element.get('line')} ok")
            if element.get("joint") == row.get("join_vik"):
                temporary.append(f'{element.get("joint")} ok')
                if element.get("weld_data") <= row.get("date_conclusion_vik"):
                    temporary.append(f'{element.get("weld_data")} ok')
                    if element.get("vic_number") == row.get("number_conclusion_vik"):
                        temporary.append(f'ВИК№{element.get("vic_number")} ок')
                        if element.get("result") and row.get("result_vik") == "годен" or "нет":
                            temporary.append(f'Результат заключения ВИК № {element.get("vic_number")} - годен')

                        else:
                            temporary.append(f'Необохимо проверить результат заключения ВИК{element.get("vic_number")}')
                    else:
                        temporary.append(f'Необходимо проверить заключения ВИК №{element.get("vic_number")}')
                else:
                    temporary.append(f'Необохимо проверить дату заключения и сварки на стыке№ {element.get("joint")}')
            else:
                temporary.append(f'Необходимо проверить номер стыка {element.get("joint")}')
        else:
            temporary.append("Необходимо проверить номер линии в ручную")

        if f"{element.get('line')} ok" in temporary and f'{element.get("joint")} ok' in temporary and f'{element.get("weld_data")} ok' in temporary:
            result_chk.append(f'Стык {element.get("joint")} ok')

        else:
            result_chk.append(f'Стык {element.get("joint")} необходимо провериить!')

    return result_chk


def checking_jsr_pvk(path: str):
    quantity_joints, jurnal_svarki_pvk, result = rd.read_jsr_p1(path)
    pvk, quantity_joins_pvk = rd.read_pvk_supports_p1(path)
    result_chk_pvk = ["ПВК: "]
    library = []

    joints_inf = {}

    for items in pvk[0:4]:
        if items in jurnal_svarki_pvk:
            library.append(f"{items} ок")
        else:
            library.append(f"! {items} не совпадает с ЖСР")
    if pvk[4] <= jurnal_svarki_pvk[4]:
        library.append(f"{pvk[4]} ок")
    else:
        library.append(f"! {pvk[2]} необходимо проверить дату")




    joints_inf[pvk[2]] = "OK"
    for string in library:
        if "ок" not in string:
            joints_inf[pvk[2]] = f' Необходимо проверить!'
            break
        else:
            pass

    for joint in joints_inf:
        result_chk_pvk.append(f"Стык - {joint} - {joints_inf[joint]}")

    return result_chk_pvk

def summary_result(path):
    vik_res = checking_jsr_vik(path)
    pvk_res = checking_jsr_pvk(path)

    summary_result = []

    for inf in vik_res:
        summary_result.append(inf)

    summary_result.append("****")

    for inf in pvk_res:
        summary_result.append(inf)


    return summary_result
