
function myfunctUppColorChange(var_str) { /*最初の文字が小文字でないなら色を変える*/
  let first_char_of_str = var_str.slice(0,1);
  let new_str = "";
  if ( first_char_of_str == "\(" ) { /* カッコの場合はその次をみる */
    let second_char_of_str = var_str.slice(1,2);
    if ( second_char_of_str == second_char_of_str.toUpperCase() ) {
      new_str = "\(<span class=\"first-character-color\">" + second_char_of_str + "</span>" + var_str.slice(2);
    } else {
      new_str = var_str;
    };
  } else {
    if ( first_char_of_str == first_char_of_str.toUpperCase() ) {
      new_str = "<span class=\"first-character-color\">" + first_char_of_str + "</span>" + var_str.slice(1);
    } else {
      new_str = var_str;
    };
  };
  return new_str;
};

/***
最初の文字が小文字でない場合、大文字なら色を変え、数字なら色またはフォントを変える。
AとBにはCngかIgnを入れて、Cngなら変わりうる、Ingはignore。
Aは色、Bはフォント
***/

function myfunctABtoSpan(var_A, var_B) {
  let new_str = "";
  if ( var_A == "C" ) {
    if ( var_B == "C" ) {
      new_str = "first-character-color first-number-font";
    } else {
      new_str = "first-character-color";
    }
  } else {
    if ( var_B == "C" ) {
      new_str = "first-number-font";
    };
  };
  return new_str;
};

function myfunctNumFC_Change(var_A, var_B, var_str) {
  let first_char_of_str = var_str.slice(0,1);
  let new_str = "";
  if ( isFinite(first_char_of_str) ) {
    new_str = "<span class=\"" + myfunctABtoSpan(var_A, var_B) + "\">" + first_char_of_str + "</span>" + var_str.slice(1);
  } else {
    new_str = myfunctUppColorChange(var_str);
  };
  return new_str;
};


/***
.first-color-change-CIのようなクラスに対して、
CIの値に応じて、各単語の先頭の文字の色やフォントを変えるCSSに変換する
CCなら、文字列の先頭が数字であれば色とフォントを変え、そのあとの各単語の先頭の数字はいじらず、大文字に対して色を変える
***/


function myfunctChangeFC_CSS(var_str) {
  $( var_str ).text(function() {
    let var_A = var_str.slice( -2, -1 ); /* var_strの末尾から2文字目を所得 */
    let var_B = var_str.slice( -1 ); /* var_strの末尾の文字を所得 */
    if ( var_A == "g" ) {
      var_A = "I";
      var_B = "I";
    } /* Classの名前の最後にCIがなければ最後はchangeになるからvar_Aはgになる。その場合はIIと同じように振る舞う */
    let str_this = $(this).text(); /* クラスvar_strのかかっているテキストを所得 */
    let ary_this = str_this.split(" ");

    let new_ary = []; /* aryの各要素を変換した後のものを格納するary */
    new_ary.push(myfunctNumFC_Change(var_A, var_B, ary_this[0])); /* 先頭の単語を変換して格納 */
    for ( var i = 1; i < ary_this.length;  i++  ) {
      new_ary.push(myfunctNumFC_Change("I", "I", ary_this[i]));
    } /* 先頭以外の単語を変換して格納するfor文 */
    let new_str = new_ary.join(' ');
    $(this).replaceWith(new_str);
  });
}



$(function() {
  myfunctChangeFC_CSS(".first-color-change-CC");
  myfunctChangeFC_CSS(".first-color-change-CI");
  myfunctChangeFC_CSS(".first-color-change-IC");
  myfunctChangeFC_CSS(".first-color-change-II");
  myfunctChangeFC_CSS(".first-color-change");
});







var this_ym_previous = ["first"]; /*** 一つ前にクリックした年月を格納しておくリスト ***/

function myfunctThisYM_to_YM(var_str) { /*** var_strに「#ThisYearMonthIs-年-月」の文字列を渡して文字列「年-月」を所得する関数 ***/
  const var_ary = var_str.split("-");
  var_ary.shift();
  const new_str = var_ary.join('-');
  return new_str;
};

 /***
 classに対し一斉に, hiddenをadd or rmvする関数
 var_AR: addかrmvか, var_str: class or id 名
 ***/

function myfunctAddRmvHidden(var_AR, var_str) {
  const var_class = document.getElementsByClassName(var_str);  /*** class「var_str」を所得 ***/
  if ( var_AR == "add" ) {  /*** addなら追加 ***/
    for (  var i = 0;  i < var_class.length;  i++  ) {
      var classes = var_class[i].classList;
      classes.add('diary-this-is-hidden');
    };
  } else { /*** そうでないなら取り除く ***/
    for (  var i = 0;  i < var_class.length;  i++  ) {
      var classes = var_class[i].classList;
      classes.remove('diary-this-is-hidden');
    };
  };
};

$(function() {
  $( ".this-year-month" ).click(function () {
    const this_ym_id_name = $(this).parent().attr("id"); /*** クリックしたaタグの一つ上の親liタグのid名「#ThisYearMonthIs-年-月」を所得 ***/
    const this_ym = myfunctThisYM_to_YM(this_ym_id_name);
    console.log(this_ym);

    /*** クリックした年月を赤く表示して前に赤かったものを元に戻す ***/
    this_ym_previous.push(this_ym);
    $(this).addClass('DiaryYMListCurrent');  /*** クリックした年月のaタグに赤く表示するclassを追加 ***/
    if (this_ym_previous[0] != this_ym_previous[1]) { /*** もし前にクリックした年月と違うなら, 前の年月をもとの色に戻す ***/
      if (this_ym_previous[0] != "first") {
        const const_ThisYearMonthIs = "#ThisYearMonthIs-" + this_ym_previous[0];
        const child_ThisYearMonthIs = $(const_ThisYearMonthIs).children('a')[0];
        child_ThisYearMonthIs.classList.remove('DiaryYMListCurrent');
      };
    };

    /*** クリックした年月に対応するclass項目を表示して一つ前の年月に対応する項目を隠す ***/
    const diary_ym = "diary-here-" + this_ym;
    myfunctAddRmvHidden("rmv", diary_ym);   /*** クリックした年月に対応するclass項目を表示 ***/
    if (this_ym_previous[0] != this_ym_previous[1]) {  /*** 一つ前のやつを隠す ***/
      const diary_ym_second = "diary-here-" + this_ym_previous[0];
      myfunctAddRmvHidden("add", diary_ym_second);
    };

    myfunctAddRmvHidden("rmv", "diary-here-first-hide");  /*** 最初は隠されているけど二回目以降は表示する ***/

    this_ym_previous.shift(); /*** 最後にリストを更新 ***/
  });
});
