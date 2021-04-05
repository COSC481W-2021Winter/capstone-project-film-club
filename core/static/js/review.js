$(document).ready(function(){
	$('.review-option.like img').on('click', function(){
		var reviewId = $(this).parents('.review').find('.review-id').val(),
			imgElement = this;
		
		$.ajax({
			url: '/r/' + reviewId + '/like',
			type: 'POST',
			success: function(data){
				if (data.success){
					if (data.liked){
						$(imgElement).prop('src', $(imgElement).prop('src').replace('like', 'like-red'));
						$(imgElement).siblings('p').text(parseInt($(imgElement).siblings('p').text()) + 1);
					} else {
						$(imgElement).prop('src', $(imgElement).prop('src').replace('like-red', 'like'));
						$(imgElement).siblings('p').text(parseInt($(imgElement).siblings('p').text()) - 1);
					}
				}
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
	$('.review-option.comment img').on('click', function(){
		$(this).parents('.review').find('.review-comment-box').focus();
	});
	
	$('.review-comment-post').on('click', function(){
		var reviewId = $(this).parents('.review').find('.review-id').val(),
			text = $(this).siblings('.review-comment-box').val(),
			element = this;
		
		$.ajax({
			url: '/r/' + reviewId + '/comment',
			type: 'POST',
			data: {
				'text': text
			},
			success: function(data){
				console.log(data);
				
				if (data.success){
					$(element).parents('.review').find('.review-comments').append(`
						<div class = "review-comment">
							<img class = "review-commenter-image" src = "` + data.comment.user.image_url + `">
							<div class = "review-comment-info">
								<p class = "review-commenter-name">` + data.comment.user.username + `</p>
								<div class = "review-comment-text">
									` + data.comment.text + `
								</div>
							</div>
						</div>
					`);
					
					$(element).parents('.review').find('.review-comment-box').val('');
					$(element).parents('.review').find('.review-comment-count').text(parseInt($(element).parents('.review').find('.review-comment-count').text()) + 1);
				}
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
});