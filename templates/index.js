window.addEventListener("load", function load(event){

		var prev = document.getElementById("previous-page");
		var next = document.getElementById("next-page");

		document.addEventListener('keydown', function(e){

				var loc;

				if ((e.keyCode == 37) && (prev)){
					loc = prev.getAttribute("href");
				}

				if ((e.keyCode == 39) && (next)){
					loc = next.getAttribute("href");
				}
				
				if (loc){
					location.href = loc;
				}
		});

		// please track touch events
		// https://developer.mozilla.org/en-US/docs/Web/API/Touch_events
		
});