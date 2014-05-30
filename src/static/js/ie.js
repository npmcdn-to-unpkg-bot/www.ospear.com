(function() {
	// for HTML5
	var els = [ 'section', 'article', 'hgroup', 'header', 'footer', 'nav',
			'aside', 'figure', 'mark', 'time', 'ruby', 'rt', 'rp' ];
	for ( var i = 0; i < els.length; i++) {
		document.createElement(els[i]);
	}
	// for IE6
	if (!document.documentMode || document.documentMode < 7) {
		var min_width_enable = function() {
			if (typeof (document.body.style.minWidth) != "undefined") {
				return;
			}
			var w = parseInt(document.body.clientWidth);
			if (w < 800) {
				document.getElementById("wrapper").style.width = "800px";
			}
		};
		attachEvent("onload", min_width_enable);
		attachEvent("onresize", min_width_enable);
	}
})();