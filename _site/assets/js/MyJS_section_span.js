/* 親タグがliでないh2タグのテキストはSpanで囲む */
/*
$("h2").text(function() {
  const var_str = $(this).text();
  const new_str = "<h2><span class=\".first-color-change-IC\">" + var_str + "</span></h2>";
  const parent_element = $(this).parent();
  const child_elements = $(this).children();
  const child_tags = child_elements.prop("tagName");
  console.log(child_tags);
  if ( child_tags === undefined ) {
    $(this).replaceWith(new_str);
    console.log(new_str);
  };
});
*/
