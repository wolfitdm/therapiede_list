function findWartezeit() {
	 $(function(){ $('h4:contains("Freie Plätze / Wartezeiten") + ul > li:first-child').addClass('wartezeit_select'); });
	 return $("li.wartezeit_select").last().html();
}
window.findWartezeit = findWartezeit;