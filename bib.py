import re
import urllib.request
import time
from random import random
import json


class Bib:
    def __init__(self):
        self.dic = {}
        self.res = {}

    def update(self):
        self.get_all_layers()
        self.build_all_layers()
        self.compress_dic()
        with open('./bib.json', 'w') as f:
            print(self.dic)
            json.dump(self.dic, f)

    def get_all_layers(self):
        self.res = {}
        locations = [
            'eg', 'og_1', 'og_2_ost', 'og_2_mitte', 'og_2_west', 'og_3_ost',
            'og_3_mitte', 'og_3_west', 'og_4'
        ]

        for loc in locations:
            fp = urllib.request.urlopen(
                "https://arbeitsplatz.ub.uni-marburg.de/?location=" + loc)
            byte_str = fp.read()

            self.res[loc] = byte_str.decode("utf8")
            fp.close()
            time.sleep(1 + random() * 4)

    def add_entry_to_dic(self, layer, entry):
        temp = entry.split(" ")
        date = temp[0][8:16]
        try:
            if len(temp) == 5:
                status = 'booked'
                place_num = temp[2][6:12]
                time = [int(temp[3][:2]), int(temp[3][:2]) + int(temp[1][8])]
            else:
                status = 'free'
                place_num = temp[1][6:12]
                time = [int(temp[2][:2]), int(temp[2][6:8])]
        except:
            print(entry, temp)

        if layer not in self.dic:
            self.dic[layer] = {}
        if date not in self.dic[layer]:
            self.dic[layer][date] = {}
        if place_num not in self.dic[layer][date]:
            self.dic[layer][date][place_num] = {'booked': [], 'free': []}

        self.dic[layer][date][place_num][status].append(time)

    def compress_range(self, array):
        if len(array) < 2:
            return array
        res = [[array[0][0]]]
        for i in range(1, len(array)):
            if array[i][0] == array[i - 1][1]:
                continue
            else:
                res[len(res) - 1].append(array[i - 1][1])
                res.append([array[i][0]])
        res[len(res) - 1].append(array[len(array) - 1][1])
        if res[len(res) - 1][1] == 0:
            res[len(res) - 1][1] = 24
        return res

    def compress_dic(self):
        for layer in self.dic:
            for day in self.dic[layer]:
                for place in self.dic[layer][day]:
                    self.dic[layer][day][place][
                        'booked'] = self.compress_range(
                            self.dic[layer][day][place]['booked'])
                    self.dic[layer][day][place]['free'] = self.compress_range(
                        self.dic[layer][day][place]['free'])

    def build_all_layers(self):
        self.dic = {}
        for layer in self.res:
            layer_string = self.res[layer]
            t = layer_string[layer_string.index("<tr>"):layer_string.
                             rindex("</tr>")].split("</tr>")[3:]
            for i in t:
                i = i[i.index("</th>") + 5:]
                i = re.sub("[\r\n\t;,\"]", "", i).replace("<td ", "").replace(
                    "</td>", "").replace(" onclick=gLA()", "")
                i = re.sub("style=background-color: #\S+", "",
                           i).replace("  ", " ")
                i_arr = i.split("&nbsp")
                for entry in i_arr:
                    if "style=width: 1px" not in entry:
                        self.add_entry_to_dic(layer, entry)