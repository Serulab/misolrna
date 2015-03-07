
$(document).ready(function(){
    $('#submitir').click(function(){
    var data = $('#blastform').serialize();
    $.post("blastresult_ax",data, 
    function(html){
                    $('#ajaxblastres').html(html);
                  }
         );
         return false;
});
 if ($("#MainBlastForm").is(":hidden")) {
   $('#MainBlastForm').slideDown('1000');
} 


 });
