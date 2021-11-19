// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional



var firebaseConfig = {
    apiKey: "AIzaSyAl1JocYyMaUaT_YaLxVYxNTj-Wf-lL4Ac",
    authDomain: "qfitadminfiles.firebaseapp.com",
    projectId: "qfitadminfiles",
    storageBucket: "qfitadminfiles.appspot.com",
    messagingSenderId: "599986010502",
    appId: "1:599986010502:web:a8023a90ad043987cd1407",
    measurementId: "G-BHBTLKJ5XV"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();
storage = firebase.storage();

function upload_image_to_firebase(input, obj_id, request_type){
    
    var file = input.files[0];
    var storageref=storage.ref();
    var current_date = get_current_date();
    var full_name = current_date + ".png"; 
    var thisref=storageref.child("images/"+full_name).put(file);
    thisref.on('state_changed',function(snapshot) {
            console.log('Done');

        }, function(error) {
            console.log('Error',error);

        }, function() {
        // Uploaded completed successfully, now we can get the download URL
            thisref.snapshot.ref.getDownloadURL().then(function(downloadURL) {
                
                
                var token = get_token();
                var data = new FormData();
                data.append("url",downloadURL);
                data.append("company",obj_id);
                if(request_type == "update_avatar"){
                    main_img = $("#img_main_image")[0];
                    main_img.src = downloadURL;                    
                    $.ajax({
                        url: "/api/update_avatar/", 
                        type: "POST",
                        data: data,
                        headers: {"Authorization": "Token "+token},
                        success: function(data){
                            console.log(data);
                            if(data["error"]){
                                alertify.error(data["error"], 5);
                            }else{
                                alertify.success("Изображение добавлено!", 4);                                
                            }
                        },
                        cache: false,
                        contentType: false,
                        processData: false,
                        
                    });
                } else if(request_type == "add_image"){
                    
                    $.ajax({
                        url: "/api/add_image/", 
                        type: "POST",
                        data: data,
                        headers: {"Authorization": "Token "+token},
                        success: function(data){
                            console.log(data);
                            if(data["error"]){
                                alertify.error(data["error"], 5);
                            }else{
                                const div = document.createElement("div");
                                div.classList.add("service-image-block");
                                div.id= "image"+data["id"];
                                div.innerHTML = `
                                    <img src="`+data["image"]+`"  alt="" class="service-image">
                                    <div class="image-trash" onclick="delete_image_from_firebase(`+downloadURL+`, `+data["id"]+`)"></div>
                                `;
                                images_form = document.getElementById('images');
                                images_form.insertBefore(div, images_form.children[images_form.children.length-1]);
                                
                                alertify.success("Изображение добавлено!", 4);
                                $('#images')[0].reset();
                            }
                        },
                        cache: false,
                        contentType: false,
                        processData: false,
                        
                    });
                }
        });
    });
}

function delete_image_from_firebase(url, obj_id){    
    let pictureRef = storage.refFromURL(url);
    pictureRef.delete().then(() => {        
        token = get_token();        
        $.ajax({
            url: "/api/images/"+obj_id+"/", 
            type: "DELETE",
            headers: {"Authorization": "Token "+token},
            success: function(data){
                image = $("#image"+obj_id)[0];
                image.remove();
                
                alertify.success("Изображение удалено!", 4);
            },
        });
    }).catch((err) => {
        console.log(err);
    });
      
}

