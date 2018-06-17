$('input').mousedown(function(e){
  e.preventDefault();
  $(this).blur();
  return false;
});
var flag = false;
$(".press").bind('touchstart click', function(event) {
  if (!flag) {
    flag = true;
    setTimeout(function() {
      flag = false;
    }, 100);
    event.preventDefault();
    var input = $(this).attr('id');
    var existing = $("#mynumber").val();
    var result;
    if (input == "GO") {
       console.log(eel.check_cpf($("#mynumber").val()));
    } else if (input == "DEL") {
      result = existing.slice(0,-1);
      $("#mynumber").val(result);
    } else {
      existing = $("#mynumber").val();
      result = existing + input;
      $("#mynumber").val(result);
      try {
    	$("#mynumber").unmask();
    } catch (e) {}
      $("#mynumber").mask("999.999.999-99");
    }
  }

  return false
});

// $("#mynumber").keydown(function(){
//     try {
//     	$("#mynumber").unmask();
//     } catch (e) {}
    
//     var tamanho = $("#mynumber").val().length;
	
//     if(tamanho < 11){
//         $("#mynumber").mask("999.999.999-99");
//     } else if(tamanho >= 11){
//         $("#mynumber").mask("99.999.999/9999-99");
//     }
    
//     // ajustando foco
//     var elem = this;
//     setTimeout(function(){
//     	// mudo a posição do seletor
//     	elem.selectionStart = elem.selectionEnd = 10000;
//     }, 0);
//     // reaplico o valor para mudar o foco
//     var currentValue = $(this).val();
//     $(this).val('');
//     $(this).val(currentValue);
// });
