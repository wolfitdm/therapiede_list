function findWartezeit() {
	 $(function(){ $('h4 + ul > li:contains("Wartezeit")').addClass('wartezeit_select'); });
	 return $("li.wartezeit_select").last().html();
}
window.findWartezeit = findWartezeit;