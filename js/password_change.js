$(function(){
    var form = document.querySelector('form');

    form.onsubmit = function(e){
        var inputNewPassword = $('#inputNewPassword').val();   
    var inputConfirmPassword = $('#inputConfirmPassword').val();
        if(inputNewPassword!=inputConfirmPassword){
           
            alert("judge success")
            e.preventDefault();
            alert("Plz confirm ur new password");
        }
    }
})