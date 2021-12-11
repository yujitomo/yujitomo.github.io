
import os
import re
import pprint


the_file_name = input()
the_file_path = "./assets/Python/" + the_file_name + ".tex"
the_aux_file_path = "./assets/Python/" + the_file_name + ".aux"
the_html = "./assets/Python/" + the_file_name + ".html"
the_file_data = open(the_file_path, 'r', encoding='UTF-8')
the_aux_file_data = open(the_aux_file_path, 'r', encoding='UTF-8')

tex_data = the_file_data.read()
preamble = tex_data.split('\\begin{document}')[0]

special_characters = ["\\", "_", "{", "}", "[", "]", "*", " ", "\n", "^", "(", ")"]

### 通常のコマンド
default_command_names = ["item", "label", "ref", "autoref", "cite", "href"]
reference_command_list = ["\\ref", "\\autoref", "\\cite"] ### \\hrefはこれらのoptionに入りうるのでちょっと別感ある
default_math_modes = ["\\(", "\\)", "\\[", "\\]"]
default_accent_functions = {"\\\'":"accute", "\\\"":"uml", "\\`":"grave", "\\~":"tilde", "\\r":"ring", "\\^":"circ", "\\textit":"i", "\\textbf":"b"}




documentclass_text = ""
japanese_document_bool = True

for line in preamble.splitlines():
    if ( "\\documentclass" in line ):
        documentclass_text = line

if ( "j" not in documentclass_text ):
    japanese_document_bool = False




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
myTheoremEnvironments_text = "" ### myTheoremEnvironmentsの中身をテキストとして所得


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
        elif ( this_command == "myTheoremEnvironments" ): ### もしmyMacrosなら、}まで抜き出す
            j = len("myTheoremEnvironments") + 1
            count_middle_bracket = 1
            if ( preamble[i+j] != "}" ):
                j += 1
                while ( count_middle_bracket != 0 ):
                    myTheoremEnvironments_text += preamble[i+j]
                    if ( preamble[i+j] == "{" ):
                        count_middle_bracket += 1
                    elif ( preamble[i+j] == "}" ):
                        count_middle_bracket -= 1
                    j += 1


### 使っている自作パッケージの一覧を所得

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


### 自作パッケージ以外で使っているパッケージを所得

my_usepackages = []
for i in range(0, len(my_usepackages_all)):
    if ( my_usepackages_all[i] not in myOriginalPackages_list ) and ( my_usepackages_all[i] not in my_usepackages):
        my_usepackages.append(my_usepackages_all[i])

print(my_usepackages)





### マクロを格納する辞書

myMacros_list = myMacros_text.splitlines()
myMacros_list.pop(-1)
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


### マクロを可能な限り展開しておく

### givenなテキストvar_strの中のマクロを一回展開する関数

def func_expand_commands(var_str):
    return_str = ""
    var_str += " "
    num_v = 0
    for i in range(0, len(var_str)):
        if ( i >= num_v ):
            if ( var_str[i] != "\\" ): ### i番目が\\でない場合はそのまま突っ込む
                return_str += var_str[i]
            else: ### i番目が\\の場合
                this_command = ""
                j = 1 ### 0だとi+jは\\だからspecial_characterになる
                while ( var_str[i+j] not in special_characters ):
                    this_command += var_str[i+j]
                    j += 1
                this_command = "\\" + this_command
                ### 今のコマンドを格納し終えた
                ### この時点でi+jはコマンド終了のところまで行ってる
                ### ここから展開開始
                ### もしmyMacroに含まれてないならそのまま放置してnum_vを更新
                if ( this_command not in myMacro_name_dict ):
                    return_str += this_command
                    num_v = i+j
                ### もし含まれていたら一回展開する
                else:
                    arg_number = int(myMacro_name_dict[this_command][0]) ### 引数の数
                    arg_list = [] ### 引数自体を格納するリスト
                    outer_bracket_number = 0 ### 一番大きい外側の{}の数をカウント
                    bracket_number = 0 ### {}をカウント
                    arg_str = "" ### 今の番目の引数を格納するstr
                    while ( outer_bracket_number < arg_number ):
                        arg_str += var_str[i+j]
                        if ( var_str[i+j] == "{"):
                            bracket_number += 1
                        elif ( var_str[i+j] == "}"):
                            bracket_number -= 1
                        if ( bracket_number == 0):
                            arg_list.append(arg_str[1:-1])
                            outer_bracket_number += 1
                            arg_str = "" ### 引数初期化
                        j += 1
                    ### 引数格納終了
                    ### この時点でi+jはarg_number番目の最後の}まできている
                    ### 一回展開する
                    result_developed = myMacro_name_dict[this_command][2] ### 展開後のやつ、ここの中の#1とかをargで置き換える
                    for a in range(0, arg_number):
                        this_replace = "#" + str(a+1)
                        result_developed = result_developed.replace(this_replace, arg_list[a])
                    ### 一回展開終了
                    ### return_strに加えて、num_vを更新
                    return_str += result_developed
                    num_v = i+j
    return return_str[:-1]


### givenなvar_strに対して、そこで使われているコマンドのリストを返す関数

def func_use_commands(var_str):
    return_list = []
    var_str += " "
    for i in range(0, len(var_str)):
        if ( var_str[i] == "\\" ):
            this_command = "\\"
            j = 1 ### 0だとi+jは\\だからspecial_characterになる
            while ( var_str[i+j] not in special_characters ):
                this_command += var_str[i+j]
                j += 1
            if ( len(this_command) == 1 ):
                this_command += var_str[i+j]
            return_list.append(this_command)
            num_v = i+j
    return return_list


### givenなコマンドのリストvar_listにマクロが使われていたらTrueを返す関数

def func_use_Macros_bool(var_list):
    this_bool = False
    for this_command in var_list:
        if ( this_command in myMacro_name_dict):
            this_bool = True
    return this_bool

### givenなvar_strのコマンドをマクロを使わないレベルまで展開する関数

def func_full_expand_Macros(var_str):
    result_str = var_str
    this_bool = func_use_Macros_bool(func_use_commands(result_str))
    while ( this_bool == True ):
        result_str = func_expand_commands(result_str)
        this_bool = func_use_Macros_bool(func_use_commands(result_str))
    return result_str


### myMacroの辞書のそれぞれをマクロを使わないレベルまで展開して格納

myMacro_name_dict_expanded = {}

for this_command in myMacro_name_dict:
    this_key = this_command
    this_list = myMacro_name_dict[this_command]
    this_list[2] = func_full_expand_Macros(myMacro_name_dict[this_command][2])
    myMacro_name_dict_expanded[this_key] = this_list

pprint.pprint(myMacro_name_dict_expanded)


### マクロ関係はいい感じになった









### my_new_theorems_dataはnewtheoremの辞書。
### 1つ目がthmとかremとか。二つ目が「定理」とか「注意」とか。三つ目はtheorem style。

my_new_theorems_data = {}

my_theorem_styles_line = myTheoremEnvironments_text.split('\\theoremstyle{')
if ( "\\renewcommand{\\sectionautorefname}" not in my_theorem_styles_line[0]):
    my_new_theorems_data["section"] = ["Section", ""]
else:
    sect_text = my_theorem_styles_line[0].split("\\renewcommand{\\sectionautorefname}{")[1]
    this_sect = ""
    i = 0
    while ( sect_text[i] != "}" ):
        this_sect += sect_text[i]
        i += 1
    my_new_theorems_data["section"] = [this_sect, ""]
for i in range(1, len(my_theorem_styles_line)):
    newtheorem_list = []
    this_theorem_style = my_theorem_styles_line[i].split('}')[0]
    for line in my_theorem_styles_line[i].splitlines():
        test_len = line.split('newtheorem')
        if len(test_len) > 1:
            line_text = re.split(r'[{}]', test_len[1])
            line_text.pop(0)
            this_line_text = []
            my_new_theorems_data[line_text[0]] = [line_text[2], this_theorem_style]


pprint.pprint(my_new_theorems_data)





### 参考文献リストを格納

this_documents = tex_data.split('\\begin{thebibliography}')[1]

bib_datas_dict = {}  ### 参考文献データを格納する辞書
bibitem_counter = 0  ### 参考文献の数をカウントするカウンター


def func_text_bfandit(var_str):
    return_str = ""
    num_v = 0
    for i in range(0, len(var_str)):
        if ( var_str[i] != "\\" ):
            if ( i <= num_v ):
                return_str += ""
            else:
                return_str += var_str[i]
        else:
            j = 0
            this_command_name = ""
            while ( var_str[i+j] != "{" ):
                this_command_name += var_str[i+j]
                j += 1
            j += 1
            if ( this_command_name == "\\textit" ):
                return_str += "<i>"
                while ( var_str[i+j] != "}" ):
                    return_str += var_str[i+j]
                    j += 1
                j += 1
                return_str += "</i>"
            elif ( this_command_name == "\\textbf" ):
                return_str += "<b>"
                while ( var_str[i+j] != "}" ):
                    return_str += var_str[i+j]
                    j += 1
                j += 1
                return_str += "</b>"
            num_v = i+j
    return return_str


this_documents_split = this_documents.split("\\bibitem")
for i in range(1, len(this_documents_split)):
    this_documents_split[i] = this_documents_split[i].split("\\end")[0]
    this_bibitem_list = this_documents_split[i].splitlines()
    this_bibitem_list_a = []
    for i in range(0, len(this_bibitem_list)):
        this_bibitem_list_a.append(this_bibitem_list[i].strip())
    this_bibitem_all_text = " ".join(this_bibitem_list_a) ### bibitemから次のbibitemまでの内容から改行と余計な空白を削除
    bib_item_data_list = [] ### 参考文献データを格納するリスト、表示名と表示内容のペア
    print_text_bibitem = "" ### 表示名を所得
    num = 1
    while ( this_bibitem_all_text[num] != "]" ):
        print_text_bibitem += this_bibitem_all_text[num]
        num += 1
    bib_item_data_list.append(print_text_bibitem)
    num += 2
    label_bibitem = "" ### ラベルを所得
    while ( this_bibitem_all_text[num] != "}" ):
        label_bibitem += this_bibitem_all_text[num]
        num += 1
    num += 2
    this_bibitem_text = "" ### 表示内容を所得
    num_v = 0
    for num_1 in range(num, len(this_bibitem_all_text)):
        if ( this_bibitem_all_text[num_1] != "\\" ) :
            if ( num_1 <= num_v ):
                this_bibitem_text += ""
            else:
                this_bibitem_text += this_bibitem_all_text[num_1]
        else :
            this_command_name = ""
            left_text = ""
            j = 0
            while ( this_bibitem_all_text[num_1+j] != "{" ):
                this_command_name += this_bibitem_all_text[num_1+j]
                j += 1
            j += 1
            if ( this_command_name == "\\href" ):
                link_url = "" ### URLを所得
                while ( this_bibitem_all_text[num_1+j] != "}" ):
                    link_url += this_bibitem_all_text[num_1+j]
                    j += 1
                this_bibitem_text += "<a href=\"" + link_url + "\">"
                j += 2
                mid_bracket_number = 1
                link_print = "" ### aタグの中身を所得
                while ( mid_bracket_number != 0 ):
                    link_print += this_bibitem_all_text[num_1+j]
                    if ( this_bibitem_all_text[num_1+j] == "{" ):
                        mid_bracket_number += 1
                    elif ( this_bibitem_all_text[num_1+j] == "}" ):
                        mid_bracket_number += -1
                    j += 1
                this_bibitem_text += func_text_bfandit(link_print)
                this_bibitem_text += "</a>"
                num_v = num_1 + j
            elif ( this_command_name == "\\textit" ):
                if ( num_1 <= num_v ):
                    this_bibitem_text += ""
                else:
                    this_bibitem_text += "<i>"
                    while ( this_bibitem_all_text[num_1+j] != "}" ):
                        this_bibitem_text += this_bibitem_all_text[num_1+j]
                        j += 1
                    j += 1
                    this_bibitem_text += "</i>"
                    num_v = num_1 + j
            elif ( this_command_name == "\\textbf" ):
                if ( num_1 <= num_v ):
                    this_bibitem_text += ""
                else:
                    this_bibitem_text += "<b>"
                    while ( this_bibitem_all_text[num_1+j] != "}" ):
                        this_bibitem_text += this_bibitem_all_text[num_1+j]
                        j += 1
                    j += 1
                    this_bibitem_text += "</b>"
                    num_v = num_1 + j
    bib_item_data_list.append(this_bibitem_text)
    bib_datas_dict[label_bibitem] = bib_item_data_list

pprint.pprint(bib_datas_dict)


### HTML書き出し用str

html_bib_data = "</section>\n\n<section classs=\"bibliography-section\">\n"
html_bib_data += "<h2 class=\"bibliography-h2\">\nReferences\n</h2>\n<ul class=\"bibliography-ul\">\n"
for bib_item in bib_datas_dict.items():
    html_bib_data += "<li "
    html_bib_data += "id=\"bib-item-" + bib_item[0] + "\" class=\"bibliography-li\">\n"
    html_bib_data += "<h3 class=\"bibliography-h3\">\n[" + bib_item[1][0] + "]\n</h3>\n"
    html_bib_data += "<p class=\"bibliography-p\">\n" + bib_item[1][1] + "\n</p>\n</li>\n"
html_bib_data += "</ul>\n</section>"








### ref系のコマンド処理

### ref系コマンドの処理、ラベルに応じてhtmlを返す
### auxファイルを掃除

aux_data = the_aux_file_data.read()
aux_line_list_all = aux_data.splitlines()
aux_newlabel_dict = {}
for line in aux_line_list_all:
    command_list = func_use_commands(line)
    if ( command_list[0] == "\\newlabel" ):
        l = len("\\newlabel") + 1
        label_name = "" ### labelの名前を格納
        while ( line[l] != "}" ):
            label_name += line[l]
            l += 1
        ### labelの名前格納終了
        ### 今の時点でline[l]は"}"
        l += 2
        this_newlabel_list = [] ### labelに対応するデータを格納
        bracket_num = 0
        bracket_right_num = 0
        var_str = ""
        while ( bracket_right_num < 5 ):
            var_str += line[l]
            if ( line[l] == "{"):
                bracket_num += 1
            elif ( line[l] == "}"):
                bracket_num -= 1
            if ( bracket_num == 0 ):
                bracket_right_num += 1
                this_newlabel_list.append(var_str[1:-1])
                var_str = ""
            l += 1
        aux_newlabel_dict[label_name] = this_newlabel_list

pprint.pprint(aux_newlabel_dict)
















### テキスト系のコマンドの展開
### ここのvar_strにはこれ以上いかなる{}も入らない

def func_text_command_expand(var_str):
    return_str_0 = ""
    count_back_slash_0 = 0 ### \\の数をカウント
    command_list_0 = func_use_commands(var_str)
    num_v = 0
    for i in range(0, len(var_str)):
        if ( i >= num_v ):
            if ( var_str[i] != "\\" ):
                return_str_0 += var_str[i]
            else:
                count_back_slash_0 += 1
                if ( command_list_0[count_back_slash_0-1] not in default_accent_functions ):
                    return_str_0 += var_str[i]
                elif ( command_list_0[count_back_slash_0-1] == "\\textit" ) or ( command_list_0[count_back_slash_0-1] == "\\textbf" ):
                    return_str_0 += var_str[i]
                else:
                    return_str_0 += "&" + var_str[i+3] + default_accent_functions[command_list_0[count_back_slash_0-1]] + ";"
                    num_v = i + 5
    return_str_1 = ""
    count_back_slash_1 = 0 ### \\の数をカウント
    command_list_1 = func_use_commands(return_str_0)
    num_w = 0
    for i in range(0, len(return_str_0)):
        if ( i >= num_w ):
            if ( return_str_0[i] != "\\" ):
                return_str_1 += return_str_0[i]
            else:
                count_back_slash_1 += 1
                if ( command_list_1[count_back_slash_1-1] not in default_accent_functions ):
                    return_str_1 += return_str_0[i]
                else:
                    j = 1
                    bracket_num = 1
                    this_text = ""
                    while ( bracket_num != 0 ):
                        this_text += return_str_0[i+7+j]
                        if ( return_str_0[i+7+j] == "{" ):
                            bracket_num += 1
                        elif ( return_str_0[i+7+j] == "}" ):
                            bracket_num -= 1
                        j += 1
                    ### この時点でthis_textは{}の中身と最後の}になっている
                    if ( command_list_1[count_back_slash_1-1] == "\\textit" ):
                        return_str_1 += "<i>" + this_text[:-1] + "</i>"
                    elif ( command_list_1[count_back_slash_1-1] == "\\textbf" ):
                        return_str_1 += "<b>" + this_text[:-1] + "</b>"
                    num_w = i + 7 + j
    return return_str_1

### 以上でdefault_accent_functionsに入っているコマンドは展開できた



print(func_text_command_expand("\\href{https://stacks.math.columbia.edu/}{\\textit{Stacks Pr\\\"{o}ject}}."))

### 数式環境を展開する関数

def func_math_mode_expand(var_str):
    return_str_0 = ""
    count_back_slash_0 = 0 ### \\の数をカウント
    command_list_0 = func_use_commands(var_str)
    num_v = 0
    for i in range(0, len(var_str)):
        if ( i >= num_v ):
            if ( var_str[i] != "\\" ):
                return_str_0 += var_str[i]
            else:
                count_back_slash_0 += 1
                if ( command_list_0[count_back_slash_0-1] not in default_math_modes ):
                    return_str_0 += var_str[i]
                else:
                    num_v = i+2
                    if ( command_list_0[count_back_slash_0-1] == "\\(" ):
                        return_str_0 += "\\("
                    elif ( command_list_0[count_back_slash_0-1] == "\\)" ):
                        return_str_0 += "\\)"
                    elif ( command_list_0[count_back_slash_0-1] == "\\[" ):
                        return_str_0 += "\\["
                    elif ( command_list_0[count_back_slash_0-1] == "\\]" ):
                        return_str_0 += "\\]"
    return return_str_0


### マクロを展開する関数はfunc_full_expand_Macros

print(func_math_mode_expand(func_full_expand_Macros("\\(A\\to \\colim_{F\\in\\mcJ_M}F\\)を\\(\\varphi\\)の核を与える射とすると、")))


### hrefコマンドの展開

def func_href_expand(var_str):
    return_str_0 = ""
    count_back_slash_0 = 0 ### \\の数をカウント
    command_list_0 = func_use_commands(var_str)
    num_v = 0
    for i in range(0, len(var_str)):
        if ( i >= num_v ):
            if ( var_str[i] != "\\" ):
                return_str_0 += var_str[i]
            else:
                count_back_slash_0 += 1
                if ( command_list_0[count_back_slash_0-1] != "\\href" ):
                    return_str_0 += var_str[i]
                else:
                    j = 6
                    bracket_num = 1
                    right_bracket_num = 0
                    url_text = ""
                    this_text = ""
                    while ( right_bracket_num < 2 ):
                        if ( right_bracket_num == 0 ):
                            url_text += var_str[i+j]
                        elif ( right_bracket_num == 1 ):
                            this_text += var_str[i+j]
                        if ( var_str[i+j] == "{" ):
                            bracket_num += 1
                        elif ( var_str[i+j] == "}" ):
                            bracket_num -= 1
                            if ( bracket_num == 0):
                                right_bracket_num += 1
                                num_v = i+j+1
                        j += 1
                    ### url_textは「hogeurl}{」みたいな感じになってて
                    ### this_textは「hoge}」みたいになってる
                    return_str_0 += "<a href=\"" + url_text[:-1] + "\">"
                    return_str_0 += func_text_command_expand(this_text[1:-1]) + "</a>"
    return return_str_0


print(func_href_expand("\\href{https://stacks.math.columbia.edu/}{\\textit{Stacks Pr\\\"{o}ject}}."))


### citeの展開

def func_cite_expand(var_str):
    return_str_0 = ""
    count_back_slash_0 = 0 ### \\の数をカウント
    command_list_0 = func_use_commands(var_str)
    num_v = 0
    for i in range(0, len(var_str)):
        if ( i >= num_v ):
            if ( var_str[i] != "\\" ):
                return_str_0 += var_str[i]
            else:
                count_back_slash_0 += 1
                if ( command_list_0[count_back_slash_0-1] != "\\cite" ):
                    return_str_0 += var_str[i]
                else:
                    j = 6
                    bracket_num = 1
                    right_bracket_num = 0
                    this_text = ""
                    this_bib_label = ""
                    while ( right_bracket_num < 2 ):
                        if ( right_bracket_num == 0 ):
                            this_text += var_str[i+j]
                        elif( right_bracket_num == 1 ):
                            this_bib_label += var_str[i+j]
                        if ( var_str[i+j] in ["[","{"] ):
                            bracket_num += 1
                        elif ( var_str[i+j] in ["]","}"] ):
                            bracket_num -= 1
                            if ( bracket_num == 0 ):
                                right_bracket_num += 1
                                num_v = i+j+1
                        j += 1
                    return_str_0 += "[<a href=\"#bib-item-" + this_bib_label[1:-1] + "\">"
                    return_str_0 += bib_datas_dict[this_bib_label[1:-1]][0] + "</a>, "
                    return_str_0 += func_href_expand(this_text[:-1]) + "]"
    return return_str_0

print(func_cite_expand("\\cite[\\href{https://stacks.math.columbia.edu/tag/058G}{Tag 058G}]{stacks-project}"))






### refやautorefを含む一文の中でrefとautorefを展開
### var_strは1行

def func_ref_expand(var_str):
    return_str = ""
    count_back_slash = 0 ### \\の数をカウント
    command_list = func_use_commands(var_str)
    num_v = 0
    for i in range(0, len(var_str)):
        if ( i >= num_v ):
            if ( var_str[i] != "\\" ):
                return_str += var_str[i]
            else:
                count_back_slash += 1
                if ( command_list[count_back_slash - 1] != "\\ref" ) and ( command_list[count_back_slash - 1] != "\\autoref" ):
                    return_str += var_str[i]
                else:
                    j = 0
                    this_command_str = ""
                    while ( var_str[i+j] != "}" ):
                        this_command_str += var_str[i+j]
                        j += 1
                    ### 今の時点でvar_str[i+j]は\ref{hoge}などの閉じカッコの部分
                    label_str = this_command_str.split("{")[1]
                    id_list = re.split(": | ", label_str)
                    id_str = "-".join(id_list)
                    return_str += "<a href=\"#" + id_str + "\">"
                    if ( command_list[count_back_slash - 1] == "\\ref" ):
                        return_str += aux_newlabel_dict[label_str][0]
                    elif ( command_list[count_back_slash - 1] == "\\autoref" ):
                        this_str = aux_newlabel_dict[label_str][3]
                        this_str_list = this_str.split(".")
                        return_str += my_new_theorems_data[this_str_list[0]][0] + " " + aux_newlabel_dict[label_str][0]
                    ### returnに展開後のものを追加
                    return_str += "</a>"
                    num_v = i+j+1
    return return_str


print(func_ref_expand("\\autoref{lem: Lazerd lem}と\\ref{enumi: eq flat cofinal}より\\(\\Rightarrow\\varphi:\\colim_{F\\in \\mcJ_M}F\\to M\\)\\)がただちに従う。"))

### これでref系コマンドを含む文の中のref系コマンドを展開できた







section_counter = 0 ### セクション数カウンター
theorem_counter = 0 ### 定理数カウンター
enumi_head = [] ### itemが箇条書き環境の先頭かどうか。enumerateやitemizeを読んだらTrueをappend、itemを読んだらすぐFalseにする
environment_data = [] ### どれだけ入れ子になった環境の中にいるかのデータ
if_enumi_bool = False ### enumerate環境内かどうか
if_enumii_bool = False ### enumerate環境内の中のenumerate環境内かどうか
if_display_math_mode = False ### displayの数式環境内かどうか
if_inline_math_mode = False ### inlineの数式環境内かどうか
if_math_mode = False ### 数式環境かどうか
normal_previous_bool = False ### 直前の一文が通常の文かどうか
normal_after_bool = False ### 直後の一文が通常の文かどうか







### labelとbeginとendとitemが関係しない文の展開方法


def func_normal_text_expand(var_str):
    global if_inline_math_mode
    global if_display_math_mode
    global if_math_mode
    return_str_0 = func_href_expand(func_cite_expand(func_ref_expand(func_math_mode_expand(func_full_expand_Macros(func_text_command_expand(var_str))))))
    return_str_1 = ""
    for i in range(0,len(return_str_0)):
        if ( return_str_0[i] == "\\" ):
            if ( return_str_0[i:i+2] == "\\(" ):
                if_inline_math_mode = True
                if_math_mode = True
            elif ( return_str_0[i:i+2] == "\\)" ):
                if_inline_math_mode = False
                if_math_mode = False
            elif ( return_str_0[i:i+2] == "\\[" ):
                if_display_math_mode = True
                if_math_mode = True
            elif ( return_str_0[i:i+2] == "\\]" ):
                if_display_math_mode = False
                if_math_mode = False
        if ( return_str_0[i] not in ["{","}"] ):
            if ( return_str_0[i-1:i+2] == " \\ " ):
                return_str_1 += ""
            else:
                return_str_1 += return_str_0[i]
        else:
            if ( if_math_mode ):
                return_str_1 += return_str_0[i]
    return return_str_1

print(func_normal_text_expand("\\autoref{lem: Lazerd lem}と\\cite[\\href{https://stacks.math.columbia.edu/tag/058G}{Tag 058G}]{stacks-project}\\textit{より}\\(\\Rightarrow\\varphi:\\colim_{F\\in \\mcJ_M}F\\to M\\)\\)が従\\\"{u}"))


















### 書き出し用HTMLファイル

this_html_file = open(the_html, 'w', encoding='UTF-8')
html_head = '''---
layout: article-type
title: "Equational Criterion of Flatness"
category: Notes
tag: "Commtative Algebra"
author: Yujitomo
description: "平坦性の Equational Criterion について"
---
'''

this_html_file.write(html_head)



### begin{document}以降を所得
this_documents = tex_data.split('\\begin{document}')[1]
this_document_lines = this_documents.splitlines()










### \\sectionを読んだらその中身を返す処理
### var_strはtexファイルの1行、次がラベルならそれも含む

def func_section_name(var_str):
    return_html = ""
    return_str = ""
    l = len("\\section")
    if ( var_str[l] == "[" ):
        j = 1
        bracket_num = 1
        while ( bracket_num != 0 ):
            if ( var_str[l+j] == "[" ):
                bracket_num += 1
            elif ( var_str[l+j] == "]" ):
                bracket_num -= 1
            j += 1
        l += j
    k = 1
    mid_bracket_num = 1
    while ( mid_bracket_num != 0 ):
        return_str += var_str[l+k]
        if ( var_str[l+k] == "{" ):
            mid_bracket_num += 1
        elif ( var_str[l+k] == "}" ):
            mid_bracket_num -= 1
        k += 1
    l += k
    return_html += "<section"
    if ( len(var_str) >= l+1 ) and ( var_str[l+1:l+7] == "\\label" ):
        m = 8
        label_name = ""
        while ( var_str[l+m] != "}" ):
            label_name += var_str[l+m]
            m += 1
        id_list = re.split(": | ", label_name)
        id_str = "-".join(id_list)
        return_html += " id=\"" + id_str + "\""
    return_html += ">\n<h2 class=\"section-name-h2\">\n"
    return_html += "Section " + str(section_counter) + ". "
    return_html += func_normal_text_expand(return_str) + "\n</h2>\n"
    return return_html




### \\beginを読んだらその中身を返す処理
### var_strはtexファイルの1行

def func_if_begin(var_str):
    return_str = ""
    for i in range(len("\\begin{"),len(var_str)):
        while ( var_str[i] != "}" ):
            return_str += var_str[i]
    environment_data.append(return_str)
    return return_str


### \\endを読んだらその中身を返す処理。beginのコピペ
### var_strはtexファイルの1行

def func_if_end(var_str):
    return_str = ""
    for i in range(len("\\end{"),len(var_str)):
        while ( var_str[i] != "}" ):
            return_str += var_str[i]
    environment_data.pop(-1)
    return return_str



### \\beginの中身に応じてhtmlを返す処理
### var_strは各行みたいなやつ
### もし\\begin{thm}みたいなのがきてたら、strの部分はあとの行に書いてあるlabelとかをつないだものとかにする

def func_if_begin_env(var_str):
    global if_math_mode
    return_html = ""
    env_name = ""
    command_list = func_use_commands(var_str)
    i = len("\\begin{}") - 1
    while ( var_str[i] != "}" ):
        env_name += var_str[i]
        i += 1
    l = i + 1 ### 閉じカッコの次まできてる
    if ( env_name == "enumerate" ):
        return_html += "<ol>\n"
    elif ( env_name == "itemize" ):
        return_html += "<ul>\n"
    elif ( env_name == "proof" ):
        return_html += "<article class=\"proof-env-article\">\n"
        return_html += "<h3 class=\"proof-env-h3\">\n"
        if ( var_str[l] != "[" ):
            return_html += "Proof." + "\n</h3>\n"
        else:
            k = 1
            bracket_num = 1
            option_name_str = ""
            while ( bracket_num > 0 ):
                option_name_str += var_str[l+k]
                if ( var_str[l+k] == "[" ):
                    bracket_num += 1
                elif ( var_str[l+k] == "]" ):
                    bracket_num -= 1
                k += 1
            option_name_str = func_line_with_ref_command(option_name_str[:-1])
            if ( japanese_document_bool == True ):
                return_html += option_name_str + ". \n</h3>\n"
            else:
                return_html += "Proof of " + option_name_str + ". \n</h3>\n"
    elif ( env_name in my_new_theorems_data ):
        return_html += "<article class=\"" + my_new_theorems_data[env_name][1] + "-env-article\""
        label_name = ""
        option_name_str = ""
        l_1 = l
        if ( var_str[l] == "[" ): ### optionがあったらその中身を所得
            k = 1
            bracket_num = 1
            while ( bracket_num > 0 ):
                option_name_str += var_str[l+k]
                if ( var_str[l+k] == "[" ):
                    bracket_num += 1
                elif ( var_str[l+k] == "]" ):
                    bracket_num -= 1
                k += 1
            l_1 += k
        if ( var_str[l_1] == "\\" ): ### labelがあったらその中身を所得、beginのあとの[]のあとのコマンドはラベルしか来ない
            k = 7
            while ( var_str[l_1+k] != "}" ):
                label_name += var_str[l_1+k]
                k += 1
            id_list = re.split(": | ", label_name)
            id_str = "-".join(id_list)
            return_html += " id=\"" + id_str + "\""
        return_html += ">\n" ### これで<article class="hoge" id="hoge">が完成
        return_html += "<h3 class=\"" + my_new_theorems_data[env_name][1] + "-env-h3\">\n"
        return_html += my_new_theorems_data[env_name][0]
        if ( env_name[-1] != "*" ):
            return_html += " " + str(section_counter) + "." + str(theorem_counter) + "."
        if ( option_name_str != "" ):
            return_html += " (" + func_normal_text_expand(option_name_str[:-1]) + ")"
        return_html += "\n</h3>\n"
    else:
        if_math_mode = True
        return_html += var_str
    return return_html


print(func_if_begin_env("\\begin{cor}[{Lazardの\\(A\\otimes \\Hom_B\\)定理: cf. \\cite[\\href{https://stacks.math.columbia.edu/tag/058G}{Tag 058G}]{stacks-project}}]\\label{Lazard thm}"))






### \\endの中身に応じてhtmlを返す処理。beginに対応する閉じタグ
### var_strは1行

def func_if_end_env(var_str):
    global if_math_mode
    return_html = ""
    env_name = ""
    command_list = func_use_commands(var_str)
    i = len("\\end{}") - 1
    while ( var_str[i] != "}" ):
        env_name += var_str[i]
        i += 1
    if ( env_name == "enumerate" ):
        return_html += "</li>\n</ol>\n"
    elif ( env_name == "itemize" ):
        return_html += "</li>\n</ul>\n"
    elif ( env_name == "proof" ):
        return_html += "</article>\n"
    elif ( env_name in my_new_theorems_data ):
        return_html += "</article>\n"
    else:
        if_math_mode = False
        return_html += "\\end{" + env_name + "}\n"
    return return_html





### itemをhtml化
### var_strは一文


def func_item_expand(var_str):
    return_html = ""
    option_name_str = ""
    l = 6
    if ( enumi_head[-1] == True ):
        return_html += "<li"
    else:
        return_html += "</li>\n<li"
    if ( var_str[5] == "["): ### もし\item[]みたいになってたら[]の中身をとる
        j = 0
        bracket_num = 1
        while ( bracket_num != 0 ):
            option_name_str += var_str[6+j]
            if ( var_str[6+j] == "[" ):
                bracket_num += 1
            elif ( var_str[6+j] == "]" ):
                bracket_num -= 1
            j += 1
        option_name_str = option_name_str[:-1]
        l = 7+j
    if ( var_str[l:l+6] == "\\label" ):
        j = 7
        label_name = ""
        while ( var_str[l+j] != "}" ):
            label_name += var_str[l+j]
            j += 1
        l += j+1
        id_list = re.split(": | ", label_name)
        id_str = "-".join(id_list)
        return_html += " id=\"" + id_str + "\""
    return_html += ">\n"
    if ( option_name_str != "" ):
        return_html += "<h4>\n" + func_normal_text_expand(option_name_str) + "\n</h4>\n"
    left_text = ""
    for k in range(l,len(var_str)):
        left_text += var_str[k]
    if ( left_text != "" ):
        return_html += "<p>\n" + func_normal_text_expand(left_text)
    return return_html









### givenなvar_strが普通の文かどうか判定
### beginやendは普通でない、maketitleも普通でない、改行だけも普通ではない

non_normal_str_commands = ["\\begin", "\\end", "\\item", "\\section", "\\maketitle", "\\[", "\\]"]

def func_normal_next_bool(var_str):
    normal_bool = True
    command_list = func_use_commands(var_str) ### 使用コマンド一覧を所得
    if ( command_list != [] ) and ( command_list[0] in non_normal_str_commands ):
        normal_bool = False
    elif ( var_str in ["\n", "\\["] ): ### 改行オンリーの行とかカッコのみの行は普通の1行ではない
        normal_bool = False
    return normal_bool

def func_normal_prev_bool(var_str):
    normal_bool = True
    command_list = func_use_commands(var_str) ### 使用コマンド一覧を所得
    if ( command_list != [] ) and ( command_list[0] in ["\\begin", "\\end", "\\section", "\\maketitle", "\\[", "\\]"]):
        normal_bool = False
    elif ( command_list != [] ) and ( command_list[0] == "\\item" ):
        l = 6
        if ( var_str[5] == "["): ### もし\item[]みたいになってたら[]の中身をとる
            j = 0
            bracket_num = 1
            while ( bracket_num != 0 ):
                if ( var_str[6+j] == "[" ):
                    bracket_num += 1
                elif ( var_str[6+j] == "]" ):
                    bracket_num -= 1
                j += 1
            l = 7+j
        if ( var_str[l:l+6] == "\\label" ):
            j = 7
            while ( var_str[l+j] != "}" ):
                j += 1
            l += j+1
        left_text = ""
        for k in range(l,len(var_str)):
            left_text += var_str[k]
        if ( left_text != "" ):
            normal_bool = False
    elif ( var_str in ["\n", "\\]"] ): ### 改行オンリーの行とかカッコのみの行は普通の1行ではない
        normal_bool = False
    return normal_bool










### 本文をhtml化

if_bib = False
num_lab = 0

for i in range(1, len(this_document_lines)):
    effective_str = this_document_lines[i].split("%")[0] ### コメントアウト以降は無視
    effective_str = effective_str.strip() ### 先頭と末尾から空白を削除
    effective_str += "\n" ### 末尾には改行を入れとく
    command_list = func_use_commands(effective_str) ### 使用コマンド一覧を所得
    if ( "thebibliography" in effective_str ):
        if_bib = True
    if ( effective_str == "\\[" ):
        if_display_math_mode = True
        if_math_mode = True
    elif ( effective_str == "\\]" ):
        if_display_math_mode = False
        if_math_mode = False
    if ( i >= num_lab ) and ( if_bib == False):
        if ( command_list != [] ):
            num_n_count = 0 ### 初期化
            if ( command_list[0] == "\\begin" ):
                next_line_command = func_use_commands(this_document_lines[i+1].split("%")[0])
                if ( next_line_command != [] ) and ( next_line_command[0] == "\\label" ): ### もし次がラベルならつけ加えてnum_labを更新
                    effective_str = effective_str[:-1] + this_document_lines[i+1].split("%")[0].strip()
                    num_lab = i+2
                j = len("\\begin{")
                env_name = ""
                while ( effective_str[j] != "}" ):
                    env_name += effective_str[j]
                    j += 1
                if ( env_name in ["equation", "align", "equation*", "align*"] ):
                    this_html_file.write("<p class=\"display-math\">\n")
                    this_html_file.write(func_if_begin_env(effective_str))
                    if_display_math_mode = True
                    if_math_mode = True
                else:
                    this_html_file.write(func_if_begin_env(effective_str)) ### fileに書き出す
                if ( env_name in my_new_theorems_data ) and ( env_name[-1] != "*" ): ### もし定理環境や定義環境なら、定理番号を更新
                    theorem_counter += 1
                elif ( env_name in ["enumerate", "itemize"] ):
                    enumi_head.append(True)
            elif ( command_list[0] == "\\end" ): ### この行が\endで始まっていたら
                this_html_file.write(func_if_end_env(effective_str))
                j = len("\\end{")
                env_name = ""
                while ( effective_str[j] != "}" ):
                    env_name += effective_str[j]
                    j += 1
                if ( env_name in ["enumerate", "itemize"]):
                    enumi_head.pop()
                elif ( env_name in ["equation", "align", "equation*", "align*"] ):
                    this_html_file.write("\n</p>\n")
                    if_display_math_mode = False
                    if_math_mode = False
            elif ( command_list[0] == "\\item" ):
                next_line_command = func_use_commands(this_document_lines[i+1].split("%")[0])
                num_lab = i+1
                if ( next_line_command == [] ): ### もし次が普通ならつけ加えてnum_labを更新
                    effective_str = effective_str + this_document_lines[i+1].split("%")[0].strip()
                    num_lab = i+2
                elif ( next_line_command[0] not in non_normal_str_commands ): ### もし次が普通ならつけ加えてnum_labを更新
                    effective_str = effective_str + this_document_lines[i+1].split("%")[0].strip()
                    num_lab = i+2
                print(effective_str)
                this_html_file.write(func_item_expand(effective_str))
                next_str = this_document_lines[num_lab].split("%")[0]
                next_str = next_str.strip() ### 先頭と末尾から空白を削除
                next_str += "\n" ### 末尾には改行を入れとく
                if ( func_normal_next_bool(next_str) == False ):
                    this_html_file.write("</p>\n")
                print(enumi_head)
                enumi_head[-1] = False ### 最初のitemではないのでこれをfalseにする
            elif ( command_list[0] == "\\section" ):
                next_line_command = func_use_commands(this_document_lines[i+1].split("%")[0])
                if ( next_line_command != [] ) and ( next_line_command[0] == "\\label" ): ### もし次がラベルならつけ加えてnum_labを更新
                    effective_str = effective_str + this_document_lines[i+1].split("%")[0].strip()
                    num_lab = i+2
                if ( section_counter != 0 ): ### もし最初のsectionなら閉じない、つまり最初のsectionじゃないなら閉じる
                    this_html_file.write("</section>\n")
                theorem_counter = 0 ### 定理数カウンターを初期化
                section_counter += 1 ### セクション数カウンターを増やす、この段階で増やす。
                this_html_file.write(func_section_name(effective_str))
            elif ( command_list[0] == "\\maketitle" ): ### これは無視、今は。
                this_html_file.write("\n")
            elif ( command_list[0] == "\\[" ):
                this_html_file.write("\\[\n")
                if_display_math_mode = True
                if_math_mode = True
            elif ( command_list[0] == "\\]" ):
                this_html_file.write("\\]\n")
                if_display_math_mode = False
                if_math_mode = False
            else: ### この行が\begin\end\section\itemでも\maketitleでもないなら、command_listが[]でないので、コマンドのある普通の文か数式
                if ( if_math_mode ):
                    this_html_file.write(func_full_expand_Macros(effective_str))
                else:
                    next_str = this_document_lines[i+1].split("%")[0]
                    next_str = next_str.strip() ### 先頭と末尾から空白を削除
                    next_str += "\n" ### 末尾には改行を入れとく
                    prev_str = this_document_lines[i-1].split("%")[0]
                    prev_str = prev_str.strip() ### 先頭と末尾から空白を削除
                    prev_str += "\n" ### 末尾には改行を入れとく
                    if ( func_normal_prev_bool(prev_str) == False ) or ( prev_str[:6] == "\\label" ):
                        this_html_file.write("<p>\n")
                    this_html_file.write(func_normal_text_expand(effective_str))
                    if ( func_normal_next_bool(next_str) == False ):
                        this_html_file.write("</p>\n")
        else: ### この行のcommand_listが[]なら、文字しかない普通の文 (これは数式環境内かもしれない) か、改行しかないかのどちらか。
            if ( if_math_mode ):
                this_html_file.write(effective_str)
            else:
                if ( effective_str != "\n" ):
                    next_str = this_document_lines[i+1].split("%")[0]
                    next_str = next_str.strip() ### 先頭と末尾から空白を削除
                    next_str += "\n" ### 末尾には改行を入れとく
                    prev_str = this_document_lines[i-1].split("%")[0]
                    prev_str = prev_str.strip() ### 先頭と末尾から空白を削除
                    prev_str += "\n" ### 末尾には改行を入れとく
                    if ( func_normal_prev_bool(prev_str) == False ):
                        this_html_file.write("<p>\n")
                    this_html_file.write(func_normal_text_expand(effective_str))
                    if ( func_normal_next_bool(next_str) == False ):
                        this_html_file.write("</p>\n")
                else:
                    this_html_file.write(effective_str)



















this_html_file.write(html_bib_data)

this_html_file.close()
