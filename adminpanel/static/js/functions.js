function get_token(){
    var token = "";
    $.ajax({
        url: "/api/token/", 
        type: "POST",
        async: false,
        data: {"username": "XcenaX", "password": "Dagad582#"},
        success: function(data){
            if(data["error"]){
                console.log(data["error"]);
            }else{
                token = data["token"];
                console.log(token);
            }
        }
    });
    return token;
}

function get_current_date(){
    var today = new Date();
    var date = today.getFullYear()+'_'+(today.getMonth()+1)+'_'+today.getDate();
    var time = today.getHours() + "_" + today.getMinutes() + "_" + today.getSeconds() + "_" + today.getMilliseconds();
    var dateTime = date+'_'+time;
    return dateTime;
}