import re


persons = [
['АЦИН АЛЕКСАНДР АЛЕКСЕЕВИЧ 1864 г.р.', ' Амурская обл. Архаринский РВК', ' с-т 577 гап', ' умер 14.10.73', ' Еткульский р-н с.Коелга.'], 
['АЦИН АЛЕКСАНДР (ИВАН) АЛЕКСЕЕВИЧ (ИВАНОВИЧ) ', ' Амурская обл. Архаринский РВК', ' с-т 577 гап', ' проживал после войны Еткульский р-н с.Коелга.', ' Еткульский р-н с.Коелга.'],
['АЦИН АЛЕКСАНДР П. 1895 г.р.', ' Амурская обл. Архаринский РВК', ' с-т 577 гап', ' погиб 23.04,45', ' Чехословакия Остраво-Моравский р-н с. Хобичево*.']
]


fio_pattern = r"[А-ЯЁ]* \([А-ЯЁ]*\)|[А-ЯЁ]*"
date_of_birth_pattern = r"\d{4}(?= г.р|)"
date_of_death_pattern = r"(?<=погиб )\d\d.\d\d.\d\d"
date_of_pass_away_pattern = r"(?<=умер )\d\d.\d\d.\d\d"
date_died_of_wounds_pattern = r"(?<=умер от ран )\d\d.\d\d.\d\d"
date_of_loss_pattern = r"(?<=пропал без вести )\d\d.\d\d.\d\d"
place_of_residence_pattern = r"проживал после войны"
place_of_conscription_pattern = r"РВК" 
military_rank_pattern = r"ст-на|с-т|ряд.|ст. л-т|гв. с-т|с-т|мл. л-т"



def check_fio(pattern, test):
    result = re.findall(pattern, test)  
    if result:
        result = list(filter(None, result))
        return result
    return None

def check_list(pattern, test):
    for t in test:
        result = re.findall(pattern, t)
        if result:
            return result
    return None

def check_one(pattern, test):
    result = re.findall(pattern, test)
    if result:
        return result[0]
    return None


def check_data(pattern, test):
    for t in test:
        result = re.findall(pattern, t)
        if result:
            return t
    return None

def check_data_next(pattern, test):
    for t in test:
        result = re.findall(pattern, t)
        if result:
            return test[test.index(t)+1]
    return None


for person in persons:

    fio = check_fio(fio_pattern, person[0])

    surname = fio[0].capitalize()
    name = fio[1].capitalize()
    patronymic = fio[2].capitalize()
    
    date_of_birth = check_one(date_of_birth_pattern, person[0])
    print(type(date_of_birth))
    place_of_conscription = check_data(place_of_conscription_pattern, person[1:])

    military_rank = check_data(military_rank_pattern, person[1:])

    date_of_death = check_list(date_of_death_pattern, person[1:])
    date_of_loss = check_list(date_of_loss_pattern, person[1:])
    date_of_pass_away = check_list(date_of_pass_away_pattern, person[1:])
    date_died_of_wounds = check_list(date_died_of_wounds_pattern, person[1:])

    place_of_residence = check_data(place_of_residence_pattern, person[1:])
    place_of_death = check_data_next(date_of_death_pattern, person[1:])
    place_of_pass_away = check_data_next(date_of_pass_away_pattern, person[1:])
    place_died_of_wounds = check_data_next(date_died_of_wounds_pattern, person[1:])


    
    # print("fio", fio)
    # print("surname", surname)
    # print("name", name)
    # print("patronymic", patronymic)
    # print("date_of_birth ",date_of_birth)
    # print("date_of_death ",date_of_death)
    # print("date_of_loss ",date_of_loss)
    # print("date_of_pass_away ",date_of_pass_away)
    # print("date_died_of_wounds ",date_died_of_wounds)
    # print("place_of_residence ",place_of_residence)
    # print("military_rank", military_rank)
    # print("place_of_death", place_of_death)
    # print("place_of_conscription", place_of_conscription)
    
    


