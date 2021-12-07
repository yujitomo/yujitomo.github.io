
import re
import pprint


the_file_name = input()
the_file_path = "./assets/Python/" + the_file_name + ".tex"
the_html = "./assets/Python/" + the_file_name + ".html"
the_file_data = open(the_file_path, 'r', encoding='UTF-8')

tex_data = the_file_data.read()
preamble = tex_data.split('\\begin{document}')[0]


special_characters = ["\\","_","{","}","[","]","*"," "]


def func_this_command(var_str):
    num = 0
    var_str += "*"
    this_command = "" ### このバックスラッシュから始まるコマンドを所得
    while ( var_str[num] not in special_characters ):
        this_command += var_str[num]
        num += 1
    return this_command


def func_my_use_packages(var_str,i):
    package_name_str = "" ### パッケージ名を格納するstr
    option_name_str = "" ### オプション名を格納するstr
    for j in range(0, len(var_str)):
        if ( var_str[j] == "{"):
            j += 1
            while ( var_str[j] != "}" ):
                package_name_str += var_str[j]
                j += 1
        ### パッケージ名を所得した
        elif ( var_str[j] == "["):
            j += 1
            while ( var_str[j] != "]" ):
                option_name_str += var_str[j]
                j += 1
        ### オプション名を所得した
        else:
            j += 1
    ### パッケージ名とオプション名のペアを返す
    return [package_name_str,option_name_str]


my_usepackages_all = [] ### 使っているパッケージとオプションを格納するリスト
myOriginalPackages_text = "" ### myOriginalPackagesの中身をテキストとして所得
myMacros_text = "" ### myMacrosの中身をテキストとして所得


for i in range(0,len(preamble)):
    if ( preamble[i] == "\\" ):
        this_line = ""
        this_num = 1
        while ( preamble[i+this_num] != "\n" ):
            this_line += preamble[i+this_num]
            this_num += 1
        this_command = func_this_command(this_line)
        ### もしusepackageなら、その名前とオプションを格納
        if ( this_command == "usepackage" ):
            the_pair = func_my_use_packages(this_line, i)
            my_usepackages_all.append(the_pair)
        elif ( this_command == "myOriginalPackages" ): ### もしmyOriginalPackagesなら、}まで抜き出す
            j = len("myOriginalPackages") + 1
            count_middle_bracket = 1
            if ( preamble[i+j] != "}" ):
                j += 1
                while ( count_middle_bracket != 0 ):
                    myOriginalPackages_text += preamble[i+j]
                    if ( preamble[i+j] == "{" ):
                        count_middle_bracket += 1
                    elif ( preamble[i+j] == "}" ):
                        count_middle_bracket -= 1
                    j += 1
        elif ( this_command == "myMacros" ): ### もしmyMacrosなら、}まで抜き出す
            j = len("myMacros") + 1
            count_middle_bracket = 1
            if ( preamble[i+j] != "}" ):
                j += 1
                while ( count_middle_bracket != 0 ):
                    myMacros_text += preamble[i+j]
                    if ( preamble[i+j] == "{" ):
                        count_middle_bracket += 1
                    elif ( preamble[i+j] == "}" ):
                        count_middle_bracket -= 1
                    j += 1



myOriginalPackages_list = []

for i in range(0, len(myOriginalPackages_text)):
    if ( myOriginalPackages_text[i] == "\\" ):
        this_line = ""
        this_num = 1
        while ( myOriginalPackages_text[i+this_num] != "\n" ):
            this_line += myOriginalPackages_text[i+this_num]
            this_num += 1
        this_command = func_this_command(this_line)
        ### もしusepackageなら、その名前とオプションを格納
        if ( this_command == "usepackage" ):
            the_pair = func_my_use_packages(this_line, i)
            myOriginalPackages_list.append(the_pair)


print(myOriginalPackages_list)

my_usepackages = []
for i in range(0, len(my_usepackages_all)):
    if ( my_usepackages_all[i] not in myOriginalPackages_list ) and ( my_usepackages_all[i] not in my_usepackages):
        my_usepackages.append(my_usepackages_all[i])

print(my_usepackages)


myMacros_list = myMacros_text.splitlines()
myMacros_list.pop(-1)
#print(myMacros_list)
myMacro_name_dict = {}

for i in range(0, len(myMacros_list)):
    if ( myMacros_list[i] != "" ) :
        num = 1
        while ( myMacros_list[i][num] != "\\" ):
            num += 1
        newcommand_data = [] ### newcommandの名前・引数の数・第一引数の初期値・展開後を格納するデータリスト
        newcommand_name = "" ### newcommandの名前
        newcommand_name_variant_number = "" ### newcommandの引数の数
        newcommand_name_first_var = "" ### newcommandの第一引数の初期値
        newcommand_name_str = "" ### newcommandの展開後
        while ( myMacros_list[i][num] != "}" ):
            newcommand_name += myMacros_list[i][num]
            num += 1
        ### newcommandの名前を格納終了
        ### newcommandの引数の数を格納
        num += 1
        if ( myMacros_list[i][num] == "["):
            num += 1
            newcommand_name_variant_number += myMacros_list[i][num]
            num += 2
        else:
            newcommand_name_variant_number += "0"
        newcommand_data.append(newcommand_name_variant_number)
        ### newcommandの引数の数を格納終了
        ### newcommandの第一引数の初期値格納
        if ( myMacros_list[i][num] == "["):
            num += 1
            bracket_number = 1
            while ( bracket_number != 0 ):
                newcommand_name_first_var += myMacros_list[i][num]
                if ( myMacros_list[i][num] == "[" ):
                    bracket_number += 1
                elif ( myMacros_list[i][num] == "]" ):
                    bracket_number += -1
                num += 1
        newcommand_data.append(newcommand_name_first_var[:-1])
        ### newcommandの第一引数の初期値格納終了
        ### newcommandの展開後を格納
        num += 1
        mid_bracket_number = 1
        while ( mid_bracket_number != 0 ):
            newcommand_name_str += myMacros_list[i][num]
            if ( myMacros_list[i][num] == "{" ):
                mid_bracket_number += 1
            elif ( myMacros_list[i][num] == "}" ):
                mid_bracket_number += -1
            num += 1
        newcommand_data.append(newcommand_name_str[:-1])
        ### newcommandの展開後を格納終了
        myMacro_name_dict[newcommand_name] = newcommand_data

pprint.pprint(myMacro_name_dict)







my_new_theorems_list = []
### my_new_theorems_listはnewtheoremのリスト。
### 1つ目がthmとかremとか。二つ目が「定理」とか「注意」とか。三つ目はtheorem style。

preamble_theorem_styles = preamble.split('\\theoremstyle{')
length_of_theoremstyles = len(preamble_theorem_styles)
print(length_of_theoremstyles)
for i in range(1,length_of_theoremstyles):
    this_theorem_style = preamble_theorem_styles[i].split('}')[0]
    print(this_theorem_style)
    for line in preamble_theorem_styles[i].splitlines():
        test_len = line.split('newtheorem')
        if len(test_len) > 1:
            line_text = re.split(r'[{}]', test_len[1])
            line_text.pop(0)
            this_line_text = []
            for thm in line_text:
                if (thm != '' and thm[0] !='['):
                    this_line_text.append(thm)
            this_line_text.append(this_theorem_style)
            my_new_theorems_list.append(this_line_text)
print(my_new_theorems_list)



### 使用パッケージを格納




my_latexsyms = preamble.split('\\usepackage{latexsym}')
