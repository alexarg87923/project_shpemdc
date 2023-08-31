$(document).ready(function(){
    $("#showModal").click(function(){
        $("#myModal").modal('show');
    });
    
    $("#showPopup").click(function(){
        $("#myPopup").toggleClass('d-none');
    });
});
$(document).ready(function(){
    $("#closeModal").click(function(){
        $("#myModal").modal('hide');
    });
});