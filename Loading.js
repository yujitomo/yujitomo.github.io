$(function () {
	var loader = $('.loading');

	//4秒後にアニメーションを非表示にする
	setTimeout(function () {
		loader.fadeOut();
	}, 4000);
});