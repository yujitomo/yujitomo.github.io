
import os
import re
import pprint


the_file_name = input()
the_file_path = "./assets/Python/" + the_file_name + ".tex"
the_html = "./assets/Python/" + the_file_name + ".html"
the_file_data = open(the_file_path, 'r', encoding='UTF-8')

tex_data = the_file_data.read()
preamble = tex_data.split('\\begin{document}')[0]

special_characters = ["\\", "_", "{", "}", "[", "]", "*", " ", "\n", "^", "(", ")"]




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
            if (len(this_command) == 1):
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
    print(type(this_list))
    myMacro_name_dict_expanded[this_key] = this_list

pprint.pprint(myMacro_name_dict_expanded)


### マクロ関係はいい感じになった









### my_new_theorems_listはnewtheoremのリスト。
### 1つ目がthmとかremとか。二つ目が「定理」とか「注意」とか。三つ目はtheorem style。

my_new_theorems_data = {}

my_theorem_styles_line = myTheoremEnvironments_text.split('\\theoremstyle{')
for i in range(1, len(my_theorem_styles_line)):
    newtheorem_list = []
    this_theorem_style = my_theorem_styles_line[i].split('}')[0]
    print(this_theorem_style)
    for line in my_theorem_styles_line[i].splitlines():
        test_len = line.split('newtheorem')
        if len(test_len) > 1:
            line_text = re.split(r'[{}]', test_len[1])
            line_text.pop(0)
            this_line_text = []
            my_new_theorems_data[line_text[0]] = [line_text[2], this_theorem_style]


pprint.pprint(my_new_theorems_data)



the_file_data.close()



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
html_bib_data += "<h2 class=\"bibliography-h2\">\n\tReferences\n</h2>\n<ul class=\"bibliography-ul\">\n"
for bib_item in bib_datas_dict.items():
    html_bib_data += "\t<li class=\"bibliography-li\">\n\t\t<h3 class=\"bibliography-h3\">[" + bib_item[1][0] + "]</h3>\n"
    html_bib_data += "\t\t<p class=\"bibliography-p\">\n\t\t\t" + bib_item[1][1] + "\n\t\t</p>\n\t</li>\n"
html_bib_data += "</ul>\n</section>"




#
#
#def myfunc_href_html(var_str):
    #left_mid_bra_num = 0
    #url_text = ""
    #print_text_all = ""
    #for char in var_str:
        #if ( left_mid_bra_num = 1 ) and ( char != "{" ) and ( char != "}" ) :
            #url_text += char
        #elif ( left_mid_bra_num > 1 ):
            #print_text_all += char
        #if ( char == "{" ):
            #left_mid_bra_num += 1
#
    #print_text = print_text_all[:-1]







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


section_counter = 0 ### セクション数カウンター
theorem_counter = 0 ### 定理数カウンター
environment_data = [] ### どれだけ入れ子になった環境の中にいるかのデータ
if_enumi_bool = False ### enumerate環境内かどうか
if_enumii_bool = False ### enumerate環境内の中のenumerate環境内かどうか
if_display_math_mode = False ### displayの数式環境内かどうか
if_inline_math_mode = False ### inlineの数式環境内かどうか
if_in_p_tag = False ### pタグで囲むべきかどうか

### 通常のコマンド
default_command_names = ["item", "label", "ref", "autoref", "cite", "href", "textit", "textbf"]
default_math_modes = ["(", ")", "[", "]"]
default_accent_functions = ["\'", "\"", "^", "=", "u", "v", "`", "~", "c", ".", "H", "r"]



### \\sectionを読んだらその中身を返す処理
### var_strはtexファイルの1行

def func_section_name(var_str):
    return_str = ""
    for i in range(len("\\section"),len(var_str)):
        if ( var_str[i] != "{" ) and ( var_str[i] != "}"):
            return_str += var_str[i]
    return return_str




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
### var_strは環境名

def func_if_begin_env(var_str):
    return_html = ""
    if ( var_str == enumerate ):
        return_html += "<ol>\n"
    elif ( var_str == itemize ):
        return_html += "<ul>\n"
    elif ( var_str == proof ):
        return_html += "<article class=\"proof-env-article\">\n<h3 class=\"proof-env-h3\">\nProof\n</h3>\n"
    elif ( var_str in my_new_theorems_data ):
        return_html += "<article class=\"" + my_new_theorems_data[var_str][1] + "-env-article\">\n<h3 class=\""
        return_html += "<h3 class=\"" + my_new_theorems_data[var_str][1] + "-env-h3\">\n"
        return_html += my_new_theorems_data[var_str][0] + "\n</h3>\n"
    else:
        return_html += "\\begin{" + var_str + "}\n"
    return return_html


### \\endの中身に応じてhtmlを返す処理。beginに対応する閉じタグ
### var_strは環境名

def func_if_end_env(var_str):
    return_html = ""
    if ( if_comment_out == False ):
        if ( var_str == enumerate ):
            return_html += "</ol>\n"
        elif ( var_str == itemize ):
            return_html += "</ul>\n"
        elif ( var_str == proof ):
            return_html += "</article>\n"
        elif ( var_str in my_new_theorems_data ):
            return_html += "</article>\n"
        else:
            return_html += "\\end{" + var_str + "}\n"
    return return_html




### 各行をhtml化
### var_strは各行

def func_line_to_html_not_only_label(var_str):
    return_html = ""
    num_v = 0
    effective_str = var_str.split("%")[0] ### コメントアウト以降は無視
    effective_str.strip() ### 先頭と末尾から空白を削除
    effective_str += "\n" ### 末尾には改行を入れとく
    command_list = func_use_commands(effective_str) ### 使用コマンド一覧を所得
    if ( command_list[0] == "\\begin" ): ### この行が\beginから始まっていた場合
        this_env = func_if_begin(effective_str)
        return_html += func_if_begin_env(this_env)
        l = len("\\begin{}")
        l += len(this_env) + 1
        if ( effective_str[l] == "[" ):
        elif ( effective_str[l] == "\\" ):
    elif ( command_list[0] == "\\end" ): ### この行が\endから始まっていた場合
        this_env = func_if_end(effective_str)
        return_html += func_if_end_env(this_env)
    elif ( command_list[0] == "\\section" ): ### この行が\sectionから始まっていた場合
        this_section = func_section_name(effective_str)
        return_html += "</section>\n<section>\n"
    else: ### この行が\beginでも\endでもないものから始まっていた場合
        for i in range(0, len(effective_str)):
            num_v = 0
    return return_html





### 本文をhtml化











this_html_file.write(html_bib_data)

this_html_file.close()
