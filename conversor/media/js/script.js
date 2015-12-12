$(document).ready(function(){
	//$( ".conversor-dow" ).hide();
	$( "#conversor-progress" ).hide();
	$( "#gif-carregando" ).hide();
	$( "#conversor-down" ).hide();
	$( "#rodape" ).hide();
	
});

function validURL(str) {
  var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
  '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
  '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
  '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
  '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
  '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  if(!pattern.test(str)) {
    return false;
  } else {
    return true;
  }
}

$(window).load(function(){//funcao acionada depois do carregamento da pagina

	$("#b-submit").click(function(){
		$("form").submit(function () { return false; });//Retirando o submit do form
		var q = $("#i-q").val();		
		if (validURL(q)){//verifica se é um link de video
			data_GET={ "q": q}
				$.ajax({
					type: "GET",
					data: data_GET,				
					url: "/search?",
					dataType: "json",
					
					beforeSend: function(){
						//$( "#conversor-progress" ).show();
						//$( "#conversor-progress" ).css('width', 1 + "%");
						$( "#conversor-down" ).hide();
						$( "#gif-carregando" ).show();						
					},
					success: function(result){
						//alert(result);
						
						//alert(result.links.mp3);
						//alert(result.links.video);
						alert(result.erro.menssagem);
						$( "#bt-down-mp3" ).attr("href", result.links.mp3);						
						$( "#bt-down-video" ).attr("href", result.links.video);
						
						$( "#gif-carregando" ).hide();						
						$( "#conversor-down" ).show();						
					},
					complete: function(msg){
						//$('#loading').css({display:"none"});
					},
					error: function(xhr, er){
						 console.log(er);
						 alert ( " Can't do because: " + xhr );
					}
				
				});			
		}else{
			var aaltura = $(window).height(); 
			//var largura = $(window).width(); 

			$( "#conversor-down" ).hide();
			$( "#gif-carregando" ).hide();
			var idtable1 = "#listaa tbody";
			var idtable2 = "#listab tbody";
			
			var q = $("#i-q").val();
			data_GET={ "q": q, "type":"json"}
		
			//result = request_ajax(data_GET);	
			
			$.ajax({
				type: "GET",
				data: data_GET,				
				url: "/search?",
				dataType: "html",
				
				beforeSend: function(){
					//$('#loading').css({display:"block"});
				},
				success: function(result){
					//alert('Result: ' + result)		
	
					var idlista = " #lista ";		
					$(idlista + ' #listaa').remove();
					$(idlista + ' #paginacao').remove();											
					$( idlista ).append( result ); 
	
				},
				complete: function(msg){
					//$('#loading').css({display:"none"});
				},
				error: function(xhr, er){
					 console.log(er);
					 alert ( " Can't do because: " + xhr );
				}
	
			});
		
				
		}
 
	});
	
	

	/*$(window).resize(function(){
						var altura = $(window).height(); 
						//var largura = $(window).width();
						$("h2").text(altura)
						//alert(altura,largura);
						rolstab(altura, idtable1);
						rolstab(altura, idtable2);
																																				
	});*/			
			
	
});

