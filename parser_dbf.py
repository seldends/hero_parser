import dbf

file = dbf.Table('/mnt/c/projects/parsing/dbf/PAM_Э.dbf', codepage='cp866')
db = file.open()
for rec in db:
    place_of_conscription = rec.NP  # Место призыва Откуда
    surname = rec.FM
    name = rec.IM
    patronymic = rec.OT
    date_of_birth = rec.GODROG
    place_of_conscription2 = rec.MPRIZ  # Место призыва Куда
    military_rank = rec.ZVANIE
    military_unit = rec.VCHAST
    fate = rec.OBGIBEL
    date_of_death = rec.URGIBEL
    location1 = rec.MZAHOR1
    location2 = rec.MZAHOR2

    print(rec.NP)
