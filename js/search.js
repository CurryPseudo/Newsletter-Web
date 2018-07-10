$(function () {
    var xmlhttp;

})
function submitVal(e) {
    var inputVal = $('#search-content').val();
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    if (inputVal == "") 
        e.preventDefault();
    else {
        xmlhttp.open("GET", "#inputVal", true);
        xmlhttp.send();
    }
}