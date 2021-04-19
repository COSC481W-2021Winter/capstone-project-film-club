$(document).ready(function(){
	var page = 1,
		reviewHtml = $('#review-html').html();
		
	$('#load-more').on('click', function(){
		var button = this;
		
		$.ajax({
			url: '/reviews/' + (page + 1),
			type: 'GET',
			success: function(data){
				console.log(data);
				
				page = data['page'];
				
				var i;
				
				for (i = 0; i < data['reviews'].length; i++){
					var tempReview = $(reviewHtml),
						review = data['reviews'][i];
					
					tempReview.find('.review-name').text(review.user.username);
					tempReview.find('.review-title').text(review.movie.title);
					tempReview.find('.media-title').text(review.movie.title);
					tempReview.find('.media-description').text(review.movie.description);
					tempReview.find('.review-added').text(review.added);
					tempReview.find('.review-score').text(review.score);
					tempReview.find('.review-body').text(review.text);
					tempReview.find('.review-image').prop('src', review.movie.poster_url);
					
					$('#feed').append(tempReview);
				}
				
				if (!data['more_to_load']){
					$('#load-more').css('display', 'none');
					$('#end-feed').css('display', 'block');
				}
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
});

function refreshRecomendations(){
	window.location.reload();
} 