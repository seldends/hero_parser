import os
import re
import json 
from bs4 import BeautifulSoup

persons = []
persons_not = []


def make_persons(directory):
    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            html_file = open(os.path.join(root, f),'r')
            print(f)
            contents = html_file.read()
            soup = BeautifulSoup(contents, 'html.parser')
            tags = soup.p.text
            data = tags.split("\n")

            persons = []
            persons_not_valid_test = []
            persons_fio_and_bdate = []
            persons_fi_and_bdate = []
            persons_fio = []
            for line in data:
                if line and line != ' ':
                    result = re.split(r',', line)
                    persons.append(result)


            print(data)



            # for line in results:
            #     if line and line != ' ':
            #         line = line.strip()
            #         condition = re.match(r"^[А-ЯЁ]{4,}", line)
            #         #result = re.split(r',', line)
            #         print(condition)
            #         if condition:
            #             persons.append(line)
            #         else:
            #             persons[-1] = persons[-1]+line

            # MyFile = open('test.txt', 'a')
            # for element in persons:
            #     MyFile.write(element)
            #     MyFile.write('\n')
            # MyFile.close()
            # for result in results:
            #     if result and result != ' ':
            #         result = result.strip()
            #         condition = re.search(r"[А-ЯЁ]* \([А-ЯЁ]*\)|[А-ЯЁ]*", result)
            #         c = condition.group(0)
            #         if condition and len(c) >= 2 and c != 'РВК' and c != 'ГВК':
            #             persons.append(result)
            #         else:
            #             persons[-1] = persons[-1]+result
            #output_file = open(dest_file, 'w', encoding='cp1251')
            with open('jfile.json', 'a', encoding='cp1251') as fout:
                json.dump(persons, fout)
            print(len(persons))
    return persons

folder = r'C:\projects\parsing\html2'
make_persons(folder)

print(persons)