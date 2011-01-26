function getSidebarContent(box_id, loadingImage_id, url) {
   var box = $(box_id)
   var loadingImage = $(loadingImage_id)
   loadingImage.show();
   Effect.SlideUp(box, {duration: 0.5});
   setTimeout(function() {
	  new Ajax.Updater({success: box},
					   url,
					   {
						  method: 'get',
						  onComplete: function() {
							 Effect.SlideDown(box, {duration: 0.5});
							 loadingImage.hide();
						  },
						  onFailure: function() {
							 alert('ごめんなさい。“通信”のえらーがはっせいしてしまいました。');
						  }
					    })
   }, 500);
}