export function showAlert(alertMsg, alertType){
    $("#alert-div").append(
        `<div class="alert alert-${alertType} alert-dismissible fade show" id="alert" role="alert">
            ${alertMsg}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`
    )
    $("#alert").fadeTo(2000, 500).slideUp(1000, function(){
        $("#alert").slideUp(1000);
        $("#alert").alert('close')
    });
    $('html,body').animate({scrollTop:0},'fast')
}