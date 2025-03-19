function findWartezeit() {
     let select_waits = $('h4:contains("Freie Plätze / Wartezeiten") + ul > li:first-child');
	 if (select_waits.length > 0) {
		$(select_waits).toggleClass('wartezeit_select', true);
		$(select_waits.parent()).toggleClass('wartezeit_list', true);
		return true;
	 } else {
		 return false;
	 }
}
function getWartezeit() {
     let select_waits = $('ul.wartezeit_list > li.wartezeit_select');
	 if (select_waits.length > 0) {
		return select_waits.last().html();
	 } else {
		return "";
	 }
}
window.findWartezeit = findWartezeit;
window.getWartezeit = getWartezeit;
//#generellinfos > .headline + .shadowbox-row + .shadowbox-row.row > div + div > ul:last-child > li:first-child