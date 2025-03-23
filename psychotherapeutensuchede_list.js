function waitForElement(selector, callback) {
    const observer = new MutationObserver((mutations, observer) => {
        const element = document.querySelector(selector);
        if (element) {
            observer.disconnect();
            callback(element);
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });
}
$(document).ready(function() {
	$('#mySelect').append($('<option>', {
		value: 1,
		text: 'My option'
	}));
    let link_part1 = "https://www.therapie.de/therapeutensuche/ergebnisse/?arbeitsschwerpunkt=0&verfahren=37&ort=";
	let link_part2 = "&search_radius=";
	let link_part3 = "&weiteres=";
    let thera_links = [];
    waitForElement('.list-columns a[href="/psychotherapie/-verfahren-/online-therapie/-ort-/zwickau/"]', function(element) {
        console.log('Element exists:', element);
    });
	let lca = listColumns("a");
	let lcb = listColumns("b");
	let lcc = listColumns("c");
	let lcd = listColumns("d");
	let lce = listColumns("e");
	let lcf = listColumns("f");
	let lcg = listColumns("g");
	let lch = listColumns("h");
	let lci = listColumns("i");
	let lcj = listColumns("j");
	let lck = listColumns("k");
	let lcl = listColumns("l");
	let lcm = listColumns("m");
	let lcn = listColumns("n");
	let lco = listColumns("o");
	let lcp = listColumns("p");
	let lcq = listColumns("q");
	let lcr = listColumns("r");
	let lcs = listColumns("s");
	let lct = listColumns("t");
	let lcu = listColumns("u");
	let lcv = listColumns("v");
	let lcw = listColumns("w");
	let lcx = listColumns("x");
	let lcy = listColumns("y");
	let lcz = listColumns("z");
    let linksx = document.querySelectorAll('.list-columns a[href*="/psychotherapie/-verfahren-/online-therapie/-ort-/"]');
    for (let i = 0; i < linksx.length; i++) {
        let loc = linksx[i].innerHTML.trim();
		if (loc in new_locs) {
		   new_locs[loc] = false;
		}
    }
	let radius = {};
	radius["Aichwald"] = 0;
	radius["default"] = 0;
	//let search_words_queer = ["Transition", "Transitionsbegleitung", "transident", "lesbisch", "schwul", "bisexuell", "pansexuell", "intersexuell", "polyamor", "queer", "nonbinär", "trans*", "Trans*", "VLSP", "LGBTQ", "LGBTQ+", "LGBTQIA", ""]  
    let search_words_queer = ["Trans*"];
	let nl = Object.keys(new_locs).filter(k => new_locs[k]);
	console.log(nl);
	for (let i = 0; i < nl.length; i++) {
		let loc = nl[i];
		if (!(loc in radius)) {
		    radius[loc] = radius["default"];
		}
		for (let j = 0; j < search_words_queer.length; j++) {
			let cLoc = createLoc(loc, radius[loc], search_words_queer[j]);
			$(lca).append(cLoc);
		}
	}
	$(".list-columns").toggleClass("thera_cool", true);
    let links = document.querySelectorAll('.list-columns a[href*="/psychotherapie/-verfahren-/online-therapie/-ort-/"]');
    let eles = [];
	let idx_ = "";
	for (let i = 0; i < links.length; i++) {
		$(links[i]).toggleClass("thera_link", true);
		let par = $(links[i]).parent();
		$(par).parent().toggleClass("thera_cool", true);
		let idx = par.attr("id");
		idx_ = idx;
		let idxe = "#" + idx;
        let loc = links[i].innerHTML.trim();
        let thera_link = link_part1 + loc;
		thera_link = thera_link + link_part2;
		if (!(loc in radius)) {
		    radius[loc] = radius["default"];
		}
	    thera_link = thera_link + radius[loc] + "&weiteres=";
		console.log("thera_link:");
        console.log(thera_link);
		$(links[i]).html(loc).toggleClass("thera_link", true).attr("data-locx", loc).attr("href", thera_link);
		continue;
		let clone = $(links[i]).clone();
		for (let j = 0; j < search_words_queer.length; j++) {
			let new_thera_link = thera_link + link_part3 + search_words_queer[j];
			console.log(new_thera_link);
			let lc = $(clone);
			console.log("hhaaaaaaaaaaaaaaaaaaaaaaaaaaa");
			console.log(lc);
			let new_loc = loc + "-" + j;
			let el = lc.html(new_loc).attr("data-locx", new_loc).attr("href", new_thera_link);
			let elOuter = el.prop('outerHTML');
			console.log(elOuter);
			eles.push(elOuter);
		}
    }
	for (let i = 0; i < eles.length; i++) {
		$(lca).append(eles[i]);
	}
	links = document.querySelectorAll('.list-columns a.noname');
	eles = [];
    for (let i = 0; i < links.length; i++) {
		let par = $(links[i]).parent();
		$(par).parent().toggleClass("thera_cool", true);
		let idx = par.attr("id");
		let idxe = "#" + idx;
        let loc = links[i].innerHTML.trim();
        let thera_link = link_part1 + loc;
		thera_link = thera_link + link_part2
		if (!(loc in radius)) {
		    radius[loc] = radius["default"];
		}
	    thera_link = thera_link + radius[loc] + "&weiteres=";
		console.log("thera_link:");
        console.log(thera_link);
		$(links[i]).html(loc).toggleClass("thera_link", true).attr("data-locx", loc).attr("href", thera_link);
		continue;
		let clone = $(links[i]).clone();
		for (let j = 0; j < search_words_queer.length; j++) {
			let new_thera_link = thera_link + link_part3 + search_words_queer[j];
			console.log(new_thera_link);
			let lc = $(clone);
			console.log("hhaaaaaaaaaaaaaaaaaaaaaaaaaaa");
			console.log(lc);
			let new_loc = loc + "-" + j;
			let el = lc.html(new_loc).attr("data-locx", new_loc).attr("href", new_thera_link);
			let elOuter = el.prop('outerHTML');
			console.log(elOuter);
			eles.push(elOuter);
		}
    }
	for (let i = 0; i < eles.length; i++) {
		$(lca).append(eles[i]);
	}
    // /\(\D+([0-9]+\sTreffer).+$/.exec(document.querySelector("h5.subheader").innerHTML);
    //#pagenav-top .prev
    //#pagenav-top .next;
});