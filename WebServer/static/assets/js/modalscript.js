$(document).ready(function(){
    $(".showModal").click(function(){
        $("#myModal").modal('show');
    });
    
    $("#showPopup").click(function(){
        $("#myPopup").toggleClass('d-none');
    });
    
    $("#closeModal").click(function(){
        $("#myModal").modal('hide');
    });
});
