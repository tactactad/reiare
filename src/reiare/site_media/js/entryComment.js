function generateEntryCommentLink(entryID) {
   document.write('<img src="/site_media/icon/ajax-loader.gif" width="10" height="10" id="commentBoxNowLoading'
		  + entryID + '" style="display: none;" />');
   document.write('<a href="javascript:void(0)" onclick="getEntryComment(' + entryID + ');return false;">こめんと</a>');
}

function getEntryComment(entryID) {
   var box = $('entryComment' + entryID);
   var loadingImage = $('commentBoxNowLoading' + entryID);
   loadingImage.show();

   var url = '/blog/comment/' + entryID + '/';
   var result = new Ajax.Updater(box,
				 url,
				 {
				    method: 'get',
				    onFailure: function() {
				          Element.update($('entryComment' + diaryID),
							 '<a onclick="getDiaryComment(' + diaryID + ');return false;" href="javascript:void(0)">こめんと</a>')},
				    onComplete: function() {
				          if (!$('commentBox' + entryID).visible()) {
					     Effect.BlindDown(box, {duration:0.5});
					  }
				          new Form.Observer('entryCommentForm' + entryID, 0.5, function(element, value) {
					     elements = value.toQueryParams();
					     if (elements['author'] != null && elements['body'] != null) {
						$('submitButton' + entryID).disabled = false;
					     } else {
						$('submitButton' + entryID).disabled = true;
					     }
							    });
					  setTimeout(function() { loadingImage.hide(); }, 500);
				    }
				 });
}

function postEntryComment(entryID) {
   var loadingImage = $('commentBoxNowLoading' + entryID);
   loadingImage.show();
   Effect.BlindUp($('entryCommentForm' + entryID));
   var url = '/blog/post_comment/' + entryID + '/';
   var pars = Form.serialize('entryCommentForm' + entryID);
   var result = new Ajax.Updater('entryComment' + entryID,
				 url,
				 {
				    method: 'post',
				    parameters: pars,
				    onComplete: function() { Effect.BlindDown($('entryCommentForm' + entryID), {duration: 0.5});
				    new Form.Observer('entryCommentForm' + entryID, 0.5, function(element, value) {
					     elements = value.toQueryParams();
					     if (elements['author'] != null && elements['body'] != null) {
						$('submitButton' + entryID).disabled = false;
					     } else {
						$('submitButton' + entryID).disabled = true;
					     }
							    });},
				    onFailure: function() { alert('ごめんなさい。“通信”のえらーがはっせいしてしまいました。');
                        //getEntryComment(entryID);
                    }
				 });
}