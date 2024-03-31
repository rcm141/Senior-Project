import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main():
    #css_parser(str(soup_init("https://www.fussball.de/static/por/8.78.73.484/css/style.css")), "", {})
    css_parser("a{b{c:1;d:2}}", "", {})
    #print(soup.find(".fbde .table>tbody>tr.row-promotion>td"))
#tr.row-promotion>td.column-icon,tr.row-promotion>td.column-rank

def soup_init(webpage):
    response = requests.get(webpage)
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup 

def css_parser(soup_str, key, css_dict):
    closed_bracket_index = 0
    open_bracket_index = 0
    bracketed_length = 0
    lists_found = {None:None}
    recurse_dict = {}
    return_dict = {}
    nesting = False
    i = 0

    for _ in range(len(soup_str)):
        print("i: " + str(i) + "; len(soup_str): " + str(len(soup_str)))
        char = soup_str[i]
        if(char == '{'):
            for j in range(i + 1,len(soup_str)):
                if(soup_str[j] == '{'):
                    nesting = True
                    break
                if(soup_str[j] == '}'):
                    break
            open_bracket_index = i
        if(char == '}'):
            closed_bracket_index = i
        if(open_bracket_index > closed_bracket_index):
            print("open_bracket_index: " + str(open_bracket_index) + "; closed_bracket_index: " + str(closed_bracket_index))
            print("key: " + str(key))
            
            if(len(list(css_dict.values())) == 0):
                bracketed_length = 0
            else:
                 for j in range(open_bracket_index, closed_bracket_index, -1):
                     print(soup_str[j])
                     if(soup_str[j] == '}'):
                         bracketed_length = j + 1
                         break
                         
            print("bracketed_length : open_bracket_index")
            print(str(bracketed_length) + " : " + str(open_bracket_index))           
            print("css_dict before:")
            print(css_dict)
            return_dict = css_parser(soup_str[open_bracket_index + 1 : ], soup_str[bracketed_length : open_bracket_index], recurse_dict)
            print("css_dict after:")
            print(css_dict)
            print("return_dict: ")
            print(return_dict)
            open_bracket_index = 0
            lists_found_now = {None:None}
            for j in range(len(list(css_dict.values()))):
                if(type(list(css_dict.values())[j]) == list):
                    lists_found_now[j] = (list(css_dict.values())[j])
            if(list(lists_found_now.values()) != list(lists_found.values())):
                if(len(list(lists_found_now.values())) == len(list(lists_found.values()))):
                    found_now_values = list(lists_found_now.values())
                    found_now_values.remove(None)
                    for j in range(len(list(css_dict.values()))):
                        if(found_now_values[0] == list(css_dict.values())[j]):
                            print("deep 1: i += " + str(len(list(css_dict.values())[j][len(found_now_values[0]) - 1]) + 1) )
                            i += len(list(css_dict.values())[j][len(found_now_values[0]) - 1]) + 1
                else:
                    list_index_to_use = list(lists_found_now.keys())
                    for keyyed in list(lists_found_now.keys()):
                        for prev_key in list(lists_found.keys()):
                            if(keyyed == prev_key):
                                list_index_to_use.remove(keyyed)
                    print("deep 2: i += " + str(len(list(css_dict.values())[list_index_to_use[0]][len(css_dict.get(list(css_dict.keys())[list_index_to_use[0]])) - 1]) + 1))
                    i += len(list(css_dict.values())[list_index_to_use[0]][len(css_dict.get(list(css_dict.keys())[list_index_to_use[0]])) - 1]) + 1
            if(len(list(css_dict.values())) > 0):
                print("shallow 1: i += " + str(len(list(css_dict.values())[len(list(css_dict.values())) - 1]) + 1))
                i += len(list(css_dict.values())[len(list(css_dict.values())) - 1]) + 1
            lists_found = lists_found_now
            if((return_dict != css_dict) & (len(list(return_dict.values())) > 0)):
                for j in range(len(list(return_dict.keys()))):
                    css_dict[list(return_dict.keys())[j]] = return_dict.get(list(return_dict.keys())[j])
                return css_dict
        if(closed_bracket_index > open_bracket_index):
            print("we're returning")
            print("open_bracket_index: " + str(open_bracket_index) + "; closed_bracket_index: " + str(closed_bracket_index))
            key_found = False
            for j in range(len(list(css_dict.keys()))):
                if(list(css_dict.keys())[j] == key):
                    key_found = True
            print("key_found: " + str(key_found) + " with value " + str(key))
            print("css_dict: ")
            print(css_dict)
            print("checking for nest")
            print("closed_bracket_index: " + str(closed_bracket_index))
            """
            for j in range(closed_bracket_index + 1,len(soup_str)):
                print(soup_str[j-5:j+5])
                if(soup_str[j] == '{'):
                    break
                if(soup_str[j] == '}'):
                    nesting = True
                    break
            """
            print("return_dict: ")
            print(return_dict)
            if(nesting):
                recurse_dict[key] = soup_str[open_bracket_index : closed_bracket_index - 1]
                return recurse_dict
            if(key_found):
                value_list = []
                if(type(css_dict.get(key)) == list):
                    for elem in css_dict.get(key):
                        value_list.append(elem)
                else:
                    value_list.append(css_dict.get(key))
                value_list.append(soup_str[open_bracket_index : closed_bracket_index])
                css_dict[key] = value_list
            else:
                print("key: " + key)
                css_dict[key] = soup_str[open_bracket_index : closed_bracket_index]
            return css_dict
        i += 1
        if(i > 2100):
            print(css_dict)
            #print("i: " + str(i))
    return css_dict

if __name__ == '__main__':
    main()