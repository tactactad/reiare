function generateGetEntryBodyLink(entryID, entryTitle, createdDatetime, permaURL) {
   document.write('<a href="#" onclick="getEntryBody(' + entryID + ');return false;">' + entryTitle + '</a>'
		  + ' <span class="date">- ' + createdDatetime + ' -</span> '
		  + '<a href="' + permaURL + '" title="permalink" class="fontSizeSmall">▼</a>');
}

function getEntryBody(entryID) {
   var box = $('entryBody' + entryID);
   var titleBox = $('entryTitle' + entryID);
   var loadingImage = $('nowLoading' + entryID);
   loadingImage.show();
   if (!box.visible()) {
      var url = '/blog/body/' + entryID + '/';
      var result = new Ajax.Updater('entryBody' + entryID,
				    url,
				    {
				       method: 'get',
				       onComplete: function() {
					     titleBox.addClassName('activeEntryTitle');
					     loadingImage.src = '/site_media/icon/ajax-loader3.gif';
					     Effect.BlindDown(box, {duration: 0.5});
					     new Form.Observer('entryCommentForm' + entryID, 0.5, function(element, value) {
						elements = value.toQueryParams();
						if (elements['author'] != null && elements['body'] != null) {
						   $('submitButton' + entryID).disabled = false;
						} else {
						   $('submitButton' + entryID).disabled = true;
						}
							    });
					     setTimeout(function() {
						   initLightbox();
						   /*previousOnload();*/
						   /*addReflections();*/
						   if(previousOnload) previousOnload(); addReflections();
						   loadingImage.hide();
						   },
						500);
					  }
				    });
   } else {
      Effect.BlindUp(box, {duration: 0.5});
      setTimeout(function() {
	    titleBox.removeClassName('activeEntryTitle');
	    loadingImage.hide();
	 },
		800);
      setTimeout(function()
		 {
		    if (titleBox.hasClassName('row1')) {
		       loadingImage.src = '/site_media/icon/ajax-loader1.gif';
		    } else if (titleBox.hasClassName('row2')) {
		       loadingImage.src = '/site_media/icon/ajax-loader2.gif';
		    }
		 }, 900);
    }
}