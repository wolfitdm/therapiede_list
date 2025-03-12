function getContentUrl(nurl, callback) {
	let hrefs = [];
	let nextNumber = [];
	let next = [];
    $.ajax({
        type: 'GET', //or POST i don't know which one
        url: nurl, //or should this be the url: ?
    }).done(function(data){
        //data should be the DOM of the second page
        let html = $(data);
        html.find('#canvas .search-results .search-results-list li a[href*="/profil/"]').each(function() {
		    hrefs.push($(this).attr("href"));
		});
		$("#pagenav-bottom li.active a").each(function() {
			nextNumber.push($(this).html());
		    next.push($(this).attr("href"));
		});
		$("#pagenav-bottom li.next a").each(function() {
		    nextNumber.push($(this).html());
		    next.push($(this).attr("href"));
		});
		$("#pagenav-bottom li:not(.active):not(.next) a").each(function() {
			nextNumber.push($(this).html());
		    next.push($(this).attr("href"));
		});
		let siteNumber = activeSite.html();
    }).fail(function(f) {
        callback(nurl);
    });
};

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
function listColumns(key) {
	let selector = "h2#"+key +" + .list-columns";
	return document.querySelector(selector);
}

function fixUmlauts(value) {
    value = value.replace(/ä/g, '&auml;');
    value = value.replace(/ö/g, '&ouml;');
    value = value.replace(/ü/g, '&uuml;');
    value = value.replace(/ß/g, '&szlig;');
    value = value.replace(/Ä/g, '&Auml;');
    value = value.replace(/Ö/g, '&Ouml;');
    value = value.replace(/Ü/g, '&Uuml;');
    return value;
}

function createLoc(name) {
	const para = document.createElement("p");
    const name_lower = name.toLowerCase();
	para.innerHTML = '<a data-href="https://www.therapie.de/therapeutensuche/ergebnisse/?arbeitsschwerpunkt=12&verfahren=37&search_radius=0&weiteres=Trans&ort=' + name + '" data-locx="'+name+'" class="thera_link noname" href="/psychotherapie/-verfahren-/online-therapie/-ort-/'+name_lower+'/">'+name+'</a>';
	return para;
}

// Append to body:
let new_locs = {};
new_locs["Leipzig"] = true;
new_locs["Berlin"] = true;
new_locs["Brandenburg an der Havel"] = true;
new_locs["Erkner"] = true;
new_locs[fixUmlauts("Lüneburg")] = true;
new_locs["Hamburg"] = true;
new_locs["Kiel"] = true;
new_locs["Saterland"] = true;
new_locs["Verden (Aller)"] = true;
new_locs["Sottrum"] = true;
new_locs["Bremen"] = true;
new_locs["Bad Oeynhausen"] = true;
new_locs["Detmold"] = true;
new_locs["Kassel"] = true;
new_locs["Marburg"] = true;
new_locs[fixUmlauts("Göttingen")] = true;
new_locs["Eschwege"] = true;
new_locs["Braunschweig"] = true;
new_locs[fixUmlauts("Düsseldorf")] = true;
new_locs[fixUmlauts("Mönchengladbach")] = true;
new_locs["Grevenbroich"] = true;
new_locs["Solingen"] = true;
new_locs["Dortmund"] = true;
new_locs["Bochum"] = true;
new_locs["Essen"] = true;
new_locs["Recklinghausen"] = true;
new_locs["Gelsenkirchen"] = true;
new_locs["Duisburg"] = true;
new_locs[fixUmlauts("Münster (Münster, Stadt)")] = true;
new_locs[fixUmlauts("Georgsmarienhütte")] = true;
new_locs["Kerpen"] = true;
new_locs[fixUmlauts("Köln")] = true;
new_locs["Trier"] = true;
new_locs[fixUmlauts("Bad Homburg v. d. Höhe")] = true;
new_locs["Wiesbaden"] = true;
new_locs["Mannheim"] = true;
new_locs["Ladenburg"] = true;
new_locs["Stuttgart"] = true;
new_locs[fixUmlauts("Tübingen")] = true;
new_locs["Altensteig"] = true;
new_locs["Remshalden"] = true;
new_locs["Karlsruhe"] = true;
new_locs["Ettlingen"] = true;
new_locs["Konstanz"] = true;
new_locs["Freiburg (Elbe)"] = true;
new_locs["Freiburg im Breisgau"] = true;
new_locs[fixUmlauts("München")] = true;
new_locs[fixUmlauts("Grafing b.München")] = true;
new_locs["Amtzell"] = true;
new_locs["Ulm"] = true;
new_locs["Ulmen"] = true;
new_locs["Straubing"] = true;
new_locs["Dresden"] = true;
new_locs["Hannover"] = true;
new_locs[fixUmlauts("Nürnberg")] = true;
new_locs["Bochum"] = true;
new_locs["Wuppertal"] = true;
new_locs["Bielefeld"] = true;
new_locs["Bonn"] = true;
new_locs["Augsburg"] = true;
new_locs["Wiesbaden"] = true;
new_locs["Braunschweig"] = true;
new_locs["Chemnitz"] = true;
new_locs["Halle (Saale)"] = true;
new_locs["Magdeburg"] = true;
new_locs["Krefeld"] = true;
new_locs["Mainz"] = true;
new_locs[fixUmlauts("Lübeck")] = true;
new_locs["Oberhausen (Neuburg-Schrobenhausen)"] = true; 
new_locs["Oberhausen (Oberhausen, Stadt)"] = true;
new_locs[fixUmlauts("Oberhausen (Südliche Weinstraße)")] = true;
new_locs["Oberhausen (Weilheim-Schongau)"] = true;
new_locs["Oberhausen an der Appel"] = true;
new_locs["Oberhausen an der Nahe"] = true;
new_locs["Oberhausen bei Kirn"] = true;
new_locs["Oberhausen-Rheinhausen"] = true;
new_locs["Rostock"] = true;
new_locs[fixUmlauts("Hagen (Hagen, Stadt der FernUniversität)")] = true;
new_locs["Hagen (Segeberg)"] = true;
new_locs["Hagen am Teutoburger Wald"] = true;
new_locs["Hagen im Bremischen"] = true;
new_locs["Hagenbach"] = true;
new_locs[fixUmlauts("Hagenbüchach")] = true;
new_locs["Hagenburg"] = true;
new_locs["Hagenow"] = true;
new_locs[fixUmlauts("Saarbrücken")] = true;
new_locs[fixUmlauts("Hamm (Eifelkreis Bitburg-Prüm)")] = true;
new_locs["Hamm (Hamm, Stadt)"] = true;
new_locs["Hamm (Sieg)"] = true;
new_locs["Hamm am Rhein"] = true;
new_locs["Hammah"] = true;
new_locs["Hammelburg"] = true;
new_locs["Hammer a.d. Uecker"] = true;
new_locs["Hammersbach"] = true;
new_locs["Hammerstedt"] = true;
new_locs["Hammerstein"] = true;
new_locs["Hamminkeln"] = true;
new_locs["Hammoor"] = true;
new_locs["Ludwigshafen am Rhein"] = true;
new_locs["Oldenburg (Oldenburg)"] = true;
new_locs[fixUmlauts("Mülheim an der Ruhr")] = true;
new_locs[fixUmlauts("Osnabrück")] = true;
new_locs["Leverkusen"] = true;
new_locs["Darmstadt"] = true;
new_locs["Heidelberg"] = true;
new_locs["Regensburg"] = true;
new_locs["Herne"] = true;
new_locs["Paderborn"] = true;
new_locs["Ingolstadt"] = true;
new_locs["Offenbach am Main"] = true;
new_locs[fixUmlauts("Fürth (Bergstraße)")] = true;
new_locs[fixUmlauts("Fürth (Fürth)")] = true;
new_locs[fixUmlauts("Fürthen")] = true;
new_locs["Heilbronn"] = true;
new_locs["Pforzheim"] = true;
new_locs[fixUmlauts("Würzburg")] = true;
new_locs["Wolfsburg"] = true;
new_locs["Bottrop"] = true;
new_locs["Erlangen"] = true;
new_locs["Bremerhaven"] = true;
new_locs["Bergisch Gladbach"] = true;
new_locs["Moers"] = true;
new_locs["Jena"] = true;
new_locs["Salzgitter"] = true;
new_locs["Hanau"] = true;
new_locs[fixUmlauts("Gütersloh")] = true;
new_locs["Hildesheim"] = true;
new_locs["Siegen"] = true;
new_locs["Kaiserslautern"] = true;
new_locs["Cottbus"] = true;
$(document).ready(function() {
    let link_part1 = "https://www.therapie.de/therapeutensuche/ergebnisse/?arbeitsschwerpunkt=12&verfahren=37&weiteres=Trans&ort=";
	let link_part2 = "&search_radius=";
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
    let nl = Object.keys(new_locs).filter(k => new_locs[k]);
	console.log(nl);
	for (let i = 0; i < nl.length; i++) {
		$(lca).append(createLoc(nl[i]));
	}
	$(".list-columns").toggleClass("thera_cool", true);
    let links = document.querySelectorAll('.list-columns a[href*="/psychotherapie/-verfahren-/online-therapie/-ort-/"]');
	let radius = {};
	radius["Aichwald"] = 0;
	radius["default"] = 0;
    for (let i = 0; i < links.length; i++) {
        let loc = links[i].innerHTML.trim();
        let thera_link = link_part1 + loc;
		thera_link = thera_link + link_part2;
		if (!(loc in radius)) {
		    radius[loc] = radius["default"];
		}
	    thera_link = thera_link + str(radius[loc]);
		console.log("thera_link:");
        console.log(thera_link);
		$(links[i]).attr("href", thera_link).html(loc).toggleClass("thera_link", true).attr("data-locx", loc);
    }
	links = document.querySelectorAll('.list-columns a.noname');
    for (let i = 0; i < links.length; i++) {
        let loc = links[i].innerHTML.trim();
        let thera_link = link_part1 + loc;
		thera_link = thera_link + link_part2;
		if (!(loc in radius)) {
		    radius[loc] = radius["default"];
		}
	    thera_link = thera_link + str(radius[loc]);
		console.log("thera_link:");
        console.log(thera_link);
		$(links[i]).attr("href", thera_link).data("href", thera_link).html(loc).toggleClass("thera_link", true).attr("data-locx", loc);
    }
    // /\(\D+([0-9]+\sTreffer).+$/.exec(document.querySelector("h5.subheader").innerHTML);
    //#pagenav-top .prev
    //#pagenav-top .next;
});