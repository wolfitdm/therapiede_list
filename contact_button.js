function decryptCharcode(n, start, end, offset) {
    n = n + offset;
    if (offset > 0 && n > end) {
        n = start + (n - end - 1);
    } else if (offset < 0 && n < start) {
        n = end - (start - n - 1);
    }
    return String.fromCharCode(n);
}

function decryptString(enc, offset) {
    var dec = "";
    var len = enc.length;
    var i;
    for (i = 0; i < len; i++) {
        var n = enc.charCodeAt(i);
        if (n >= 0x2B && n <= 0x3A) {
            dec += decryptCharcode(n, 0x2B, 0x3A, offset);
        } else if (n >= 0x40 && n <= 0x5A) {
            dec += decryptCharcode(n, 0x40, 0x5A, offset);
        } else if (n >= 0x61 && n <= 0x7A) {
            dec += decryptCharcode(n, 0x61, 0x7A, offset);
        } else {
            dec += enc.charAt(i);
        }
    }
    return dec;
}

function getDecryptedEmail() {
	let contactButton = $('#contact-button, .contact-button');
	let contactUid = $(contactButton).data('contact-uid');
	let contactEmail = $(contactButton).data('contact-email');
	let contactEmailSubject = $(contactButton).data('contact-email-subject');
	let contactEmailBodyPrefix = $(contactButton).data('contact-email-body-prefix');
	let contactEmailBody = $(contactButton).data('contact-email-body');
	let contactEmailDecrypted = decryptString(contactEmail, -1);
	//$('#email-address-' + contactUid).text(contactEmailDecrypted);
	return contactEmailDecrypted;
}

function send_UnCryptMailto_with_data(contactEmail, contactEmailSubject, body) {
	
}

function getOpenerFunc(contactEmail, contactEmailSubject, contactEmailBodyPrefix, contactEmailBody) {

};