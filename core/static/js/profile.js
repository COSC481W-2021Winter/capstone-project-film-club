$(document).ready(function(){
	$('#user-follow').on('click', function(){
		var button = this;
		
		$.ajax({
			url: '/follow/',
			type: 'POST',
			data: {
				'username': $('#profile-username').val()
			},
			success: function(data){
				if (data['added']){
					$(button).addClass('following');
					
					$(button).find('.main-label').text('Following');
				} else {
					$(button).removeClass('following');
					
					$(button).find('.main-label').text('Follow');
				}
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
	
	$('#all-followers').on('click', function(){
		var button = this;
		
		$.ajax({
			url: 'followers',
			type: 'GET',
			success: function(data){
				console.log(data);
				
				var i;
				
				for (i = 0; i < data.followers.length; i++){
					var follower = data.followers[i];
					
					$(button).parents('.tile').find('.slider-items').append(`
						<a href = "` + follower.profile_url + `">
							<div class = "slider-item circle" style = "background-image: url(` + follower.profile_pic_url + `)" title = "` + follower.username + `">
								
							</div>
						</a>
					`);
				}
				
				$(button).remove();
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
	
	$('#all-followees').on('click', function(){
		var button = this;
		
		$.ajax({
			url: 'followees',
			type: 'GET',
			success: function(data){
				console.log(data);
				
				var i;
				
				for (i = 0; i < data.followees.length; i++){
					var followee = data.followees[i];
					
					$(button).parents('.tile').find('.slider-items').append(`
						<a href = "` + followee.profile_url + `">
							<div class = "slider-item circle" style = "background-image: url(` + followee.profile_pic_url + `)" title = "` + followee.username + `">
								
							</div>
						</a>
					`);
				}
				
				$(button).remove();
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
	
	$('#all-movies').on('click', function(){
		var button = this;
		
		$.ajax({
			url: 'movies',
			type: 'GET',
			success: function(data){
				console.log(data);
				
				var i;
				
				for (i = 0; i < data.movies.length; i++){
					var movie = data.movies[i];
					
					$(button).parents('.tile').find('.slider-items').append(`
						<a href = "` + movie.movie_url + `">
							<div class = "slider-item" style = "background-image: url(` + movie.poster_url + `)" title = "` + movie.title + `">
								
							</div>
						</a>
					`);
				}
				
				$(button).remove();
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
});