
import re


the_file_name = input()
the_file_path = "./assets/Python/" + the_file_name + ".tex"
the_html = "./assets/Python/" + the_file_name + ".html"
the_file_data = open(the_file_path, 'r', encoding='UTF-8')

tex_data = the_file_data.read()
preamble = tex_data.split('\\begin{document}')[0]




### my_new_theorems_listはnewtheoremのリスト。
### 1つ目がthmとかremとか。二つ目が「定理」とか「注意」とか。三つ目はtheorem style。

my_new_theorems_list = []

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




my_commands = preamble.split('\\usepackage{latexsym}')
