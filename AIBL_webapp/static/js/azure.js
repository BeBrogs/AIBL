login_head = "https://prod-92.westeurope.logic.azure.com/workflows/3a8f17661ca04ec588cb3dac98e761bc/triggers/request/paths/invoke/rest/users/";
login_tail = "?api-version=2016-10-01&sp=%2Ftriggers%2Frequest%2Frun&sv=1.0&sig=S-uc7WSFZ-lfpSXPrdBrsnfrsT9AkNsBW5r2Pbs9ySo";

register_uri = "https://prod-120.westeurope.logic.azure.com/workflows/0b90fdd42958462f9b8cd8e7b3c69ea8/triggers/request/paths/invoke/rest/users/register?api-version=2016-10-01&sp=%2Ftriggers%2Frequest%2Frun&sv=1.0&sig=37HzTl6HoVzPbnWvikjQnKnXcNkqgpShr9rG7bTdfNQ";

populate_braille_detect_table_uri = "https://prod-58.westeurope.logic.azure.com/workflows/667dc689590443ada2ce09d1fdf38b28/triggers/request/paths/invoke/rest/aibl/populate_braille_count?api-version=2016-10-01&sp=%2Ftriggers%2Frequest%2Frun&sv=1.0&sig=bAUQEMkta4RXIoPRckoBEXDfCAOsM8kmkdkkEDpKKto";

user = sessionStorage.getItem("user");

console.log(user);

console.log("HELLOOO?");


$( document ).ready(function() {
    $("#login_btn").click(function(){
        login();
    }); 

    $("#logout").click(function(){
        logout();
    });
    
    $("#register_btn").click(function(){
        register();
        
    });

    $("#submit").click(function(){
        alert("Please wait as we analyse your image");
    });

});





function login(){
    if (sessionStorage.getItem('user') == null || sessionStorage.getItem('user') == 'null'){
        username = $('#username').val();
        password_input = $('#password').val();
        login_qry = login_head + username + login_tail;
        alert("Please wait...");
            $.getJSON(login_qry, function(data){
                if (data["password"] == password_input){
                    alert("Logged in Successfully")
                    sessionStorage.setItem("user", username);
                    window.location.replace("/");
                }else{
                    alert("Incorrect Password")
                }
            }).fail(function (response){
                    alert("Login failed, try again");
            });
    }else{
        alert("You are already logged in (account name: " + user + ")")
    }
}


function logout(){
    if (sessionStorage.getItem('user') != 'null'){
        sessionStorage.setItem('user', null);
        user=null;
        alert('Logged out successfully');
        window.location.replace("/");
      }
      else{
        alert("You can't log out because you're not logged in");
      }
}

function register(){
    if (sessionStorage.getItem("user") != "null"){
        alert("You must log out before registering a new accouunt");
    }else{

        //Validation on username
        usernameValid = usernameValidation($("#username").val());
        passwordValid = passwordValidation($("#password").val(), $("#username").val());
        if (usernameValid == true && passwordValid == true){
            var subObj={
                username: $("#username").val(),
                password: $("#password").val()
            }
    
            subObj = JSON.stringify(subObj);
            $.post({
                url: register_uri,
                data: subObj,
                contentType: 'application/json; charset=utf-8'
            }).done(function (response){
                alert("Please wait as we set up your account");
                populate_braille_count($("#username").val());
                alert("Account created successfully. Redirecting to login page...");
                window.location.replace("/login");
            }).fail(function (response){
                alert("Account name taken, try again.");
            });

        }
    }
}


function populate_braille_count(username){
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (i=0; i<alphabet.length; i++){
        letter = alphabet[i];
        var subObj = {
            username: username,
            braille_letter: letter
        }

        subObj = JSON.stringify(subObj);

        $.post({
            url: populate_braille_detect_table_uri,
            data: subObj,
            contentType: 'application/json; charset=utf-8'
        })
    }

}

function usernameValidation(username){
    if (username.length < 8){
        alert("Username must be over 8 characters");
        return false;
    }
    if (username.length >20){
        alert("Username should not be over 20 characters");
        return false;
    }
    return true;
}

function passwordValidation(password, username){
    if (password.length < 8){
        alert("Password must be over 8 characters");
        return false;
    }
    if (password.length >20){
        alert("Password should not be over 20 characters");
        return false;
    }

    if (password == username){
        alert("Username and password cannot be the same");
        return false;
    }
    return true;
}


function togglePassword(){
    var x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}
