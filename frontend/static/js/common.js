function showToast(type,msg){
        $.toast({
            heading: type,
            text: msg,
            icon: type,
            position: 'top-center', 
            showHideTransition: 'slide'
        });
}
$(document).ready(function(e){
$('#default_loader').hide();
$("#frm_register").validationEngine();
$("#frm_login").validationEngine();
$("#frm_feedback").validationEngine();
$("#frm_forgotpassword").validationEngine();
// login user
$("#frm_login").submit(function(e)
{   
    var valid = $("#frm_login").validationEngine('validate');
    
    if (valid == true) {
    var formURL = $(this).attr("action");
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data:  new FormData(this),
        contentType: false,
        cache: false,
        processData:false,
        beforeSend: function() {
            $('#default_loader').show();
        },
        success:function(data, textStatus, jqXHR) 
        {
            $('#default_loader').hide();
            var obj = jQuery.parseJSON( data );
            if(obj.ack==="1"){
              $("#msg_error").hide();  
              $("#msg_success").show();  
              $("#msg_success").html(obj.msg);
              $('#btn_signin') .prop('disabled', true);
                setTimeout(function(){ location.assign("/dashboard/"); }, 3000);
            } else{
                $("#msg_success").hide();  
                $("#msg_error").show();  
                $("#msg_error").html(obj.msg);
            }
              //setTimeout(function(){ location.assign("/admin/product-gallery/"+product_id+"/"); }, 3000);
            
        },
        error: function(jqXHR, textStatus, errorThrown) 
        {
            $('#default_loader').hide();
            return false;      
        }
    }); 
} 
    e.preventDefault(); //STOP default action
    //e.unbind(); //unbind. to stop multiple form submit.
});

// register user

$("#frm_register").submit(function(e)
{  
    var valid = $("#frm_register").validationEngine('validate');
    if(valid == true) {
    var formURL = $(this).attr("action");
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data:  new FormData(this),
        contentType: false,
        cache: false,
        processData:false,
        beforeSend: function() {
            $('#default_loader').show();
        },
        success:function(data, textStatus, jqXHR) 
        {
            $('#default_loader').hide();
            var obj = jQuery.parseJSON( data );
            if(obj.ack==="1"){
              $('#btn_signup').prop('disabled', true);
              $('#error_msg').hide();
              //$('#success_msg').show();
              //$('#success_msg').html(obj.msg);
              $("#frm_register")[0].reset();
              location.assign("/dashboard/");
              //showToast("success",obj.msg);
              //setTimeout(function(){ location.assign("/dashboard/"); }, 3000);
            } else{
                 $('#success_msg').hide();
                 $('#error_msg').show();
                 $('#error_msg').html(obj.msg);
                 //showToast("error",obj.msg);
            }
              //setTimeout(function(){ location.assign("/admin/product-gallery/"+product_id+"/"); }, 3000);
            
        },
        error: function(jqXHR, textStatus, errorThrown) 
        {
            $('#default_loader').hide();
            //showToast("error","Sry some technical error!");
            return false;      
        }
    }); 
}
    e.preventDefault(); //STOP default action
    //e.unbind(); //unbind. to stop multiple form submit.
});


$("#frm_forgotpassword").submit(function(e)
{   
    var valid = $("#frm_forgotpassword").validationEngine('validate');
    
    if (valid == true) {
    var formURL = $(this).attr("action");
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data:  new FormData(this),
        contentType: false,
        cache: false,
        processData:false,
        beforeSend: function() {
            $('#default_loader').show();
        },
        success:function(data, textStatus, jqXHR) 
        {
            $('#default_loader').hide();
            var obj = jQuery.parseJSON( data );
            if(obj.ack==="1"){
              $("#msg_err").hide();  
              $("#msg_sucss").show();  
              $("#msg_sucss").html(obj.msg);
              $('#btn_forgot').prop('disabled', true);
                //setTimeout(function(){ location.assign("/"); }, 3000);
            } else{
                $("#msg_sucss").hide();  
                $("#msg_err").show();  
                $("#msg_err").html(obj.msg);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) 
        {
           $('#default_loader').hide();
            return false;      
        }
    }); 
} 
    e.preventDefault(); //STOP default action
    //e.unbind(); //unbind. to stop multiple form submit.
});

     
});