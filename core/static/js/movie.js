$(document).ready(function(){
	$('#mark-watched').on('click', function(){
		var button = this;
		
		$.ajax({
			url: '/watch/',
			type: 'POST',
			data: {
				'movie_id': movie_id
			},
			success: function(data){
				console.log(data);
				console.log(movie_id);
				
				if (data['added'])
					$(button).addClass('watched');
				else
					$(button).removeClass('watched');
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
});