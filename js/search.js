$(function () {

})
function submitVal(e) {
    var inputVal = $('#search-content').val();
    if (inputVal == "") 
        e.preventDefault();
    else {
        url = "/search/" + inputVal;
        window.location.href = url;
    }
    return false;
}