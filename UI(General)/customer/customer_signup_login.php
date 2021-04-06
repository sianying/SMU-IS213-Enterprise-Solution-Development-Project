<!doctype html>
<html lang="en">

    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    
    <!--Icons API-->
    <script src="https://kit.fontawesome.com/44084b3444.js" crossorigin="anonymous"></script>

    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <!--ReCaptcha API-->
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>

    <!--Import Rubik font-->
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik&display=swap');
    </style>

    <!--Import Roboto font-->
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
    </style>

    <!--Import Patua One font-->
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Patua+One&display=swap');
    </style>
<head>
    <?php 
        session_start();
        function function_alert($message) { 
            
            // Display the alert box  
            echo "<script>alert('$message');</script>"; 
        } 
        if (isset($_SESSION['error'])) { 

        function_alert($_SESSION['error']);
        unset($_SESSION["error"]);

        }

    ?>
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
      body{
        font-family: 'Roboto', sans-serif;
        background-image: url('../images/bg-img.JPG');
        background-position: center;
        background-attachment: fixed;
      }
        
        button:hover {
            cursor: pointer;
        }
        
        .hide {
            display: none;
        }
        
        .wrapper {
            background: rgba(0, 0, 0, 0.6);
            position: relative;
            width: 600px;
            height: 250px;
            margin: 0 auto;
            margin-top: 30%;
        }
        
        .left,
        .right {
            width: 50%;
        }
        
        .left {
            float: left;
        }
        
        .right {
            float: right;
        }
        
        .bh{
            margin-left: 20px;
            margin-right: 20px;
            color: #fafafa;
            letter-spacing: 1px;
            text-align: center;
            font-size: 27.5px;
            font-weight: 500;
        }
        
        .background button {
            position: absolute;
            left: 0;
            bottom: 60px;
        }
        
        
        .background .left button {
            left: 15%;
            margin-top:20px;
        }
        
        .background .right button {
            left: 550px;
            margin-top:
        }
        
        .form-container {
            position: absolute;
            width: 305px;
            height: 500px;
            background-color:#EEE2CC;
            top: -50%;
            left: 20px;
            -webkit-box-shadow: 9px 10px 10px 0px rgba(0, 0, 0, 0.75);
            box-shadow: 9px 10px 10px 0px rgba(0, 0, 0, 0.75);
            border-radius: 20px 20px 20px 20px;
        }
        
        .sign-up,
        .login {
            margin: 40px;
        }

        .login{
            padding-top:60px;
        }
        
        .back-btn {
            width: 100px;
            height: 40px;
            font-size: 15px;
            border: 0;
            border-radius: 30px;
            background: transparent;
            border: 1px solid white;
            color: #fafafa;
            -webkit-transition: .3s all;
            transition: .3s all;
            justify-content: center;
            
        }
        
        .back-btn:hover {
            background-color: gray;
            border: 1px solid gray;
        }
        
        .form-btn {
            display: block;
            margin-top: 30px;
            width: 150px;
            height: 40px;
            font-size: 18px;
            border: 1px solid #9E8A81;
            border-radius: 20px;
            background-color: #1C00ff00;
            color: #9E8A81;
            -webkit-transition: .4s all;
            transition: .4s all;
            
        }

        .sign-up button:hover,
        .login button:hover {
            background-color: gray;
            color:white;
        }
        
        
        .form-header {
            font-size: 32px;
            color: black;
            text-align: center;
        }
        
        .form-container input {
            margin-top: 20px;
            width: 70%;
            height: 30px;
            border: 0;
            background-color:#FCF9F2;
            border-radius: 10px 10px 10px 10px;
            padding-left:10px;
            margin-left:4%;
        }
        
        input[type="text"],
        input[type="email"] {
            color: gray;
        }
        
        .form-container i {
            margin-left: 10px;
            margin-bottom: -5px;
            color: #888;
        }
        
        .login button,
        .forgot {
            display: inline-block;
          
        }
        
        .forgot {
            margin-left: 15px;
            text-decoration: none;
            color: black;
        }
        
        .forgot:hover {
            color: #FC7D5F;
            text-decoration: underline;
        }

        body{
            background-color:#F7F0E6; 
            background-size: cover; 
        
        }

        .g-recaptcha {
            transform:scale(0.77);
            transform-origin:0 0;
        }

        
    </style>
</head>

<body>

    <div class="container" id = 'background'>
        <div class='row'>
            <div class="col-sm-6" style = 'float: left; margin-top: 4.5%'>
                <div class="wrapper" style = 'background-color: #9E8A81; border-radius:0px 10px 10px 0px;' >
                    <div class="background">
                        <div class="left" style = 'text-align: center'>
                            <h2 class="bh" style = 'margin-top: 20%' ></b>Don't have an account?</b></h2>
                            <button class="back-btn signup-but" style='margin-bottom:3%;'>Sign Up</button>
                        </div>

                        <div class="right">
                            <h2 class="bh" style = 'margin-top: 20%; '>Already Registered?</h2>
                            <button class="back-btn login-but" style='margin-bottom:3%; left:67%'>Log In</button>
                        </div>
                    </div>
                    <div class="form-container">
                        <div class="sign-up">
                            <form method="post" action="#put into some registering processing page" >
                                <h2 class="form-header">Sign Up</h2>
                                <input type="text" name="fullname" id = 'fullnameSU' placeholder="Full Name"><i class="fa fa-user"></i></input>
                                <input type="text" name="username" id = 'UsernameSU' placeholder="Username"><i class="far fa-address-card"></i></input>
                                <input type = 'text' name='handle' id = 'teleSU' placeholder='Telegram Handle'><i class="fa fa-telegram"></i></input>
                                <input type = 'text' name ='contact' id ='contactSU' placeholder='Contact Number'><i class="fas fa-phone-volume"></i></input>
                                <input type="text" name="email" id = 'emailSU' placeholder="Email"><i class="fa fa-envelope-o"></i></input>
                                <input type="password" name="password" id='passwordSU' placeholder="Password"><i class="fa fa-lock"></i></input>
                                <button type="submit" class="form-btn " style="margin-left: 10%;" onclick = "signUpValidate()" >Sign Up</button>
                                <div id = "errorSU"></div>
                            </form>
                        </div>
                        <div class="my-5">
                            <div class="login hide ">
                                <!-- <form method="post"  action="../Main/process_login.php" > -->
                                <form method="get">
                                <h2 class="form-header">Log In</h2>  
                                <input type="text" name="username" id = 'usernameLI' placeholder="Username"><i class="fa fa-envelope-o"></i></input>
                                
                                <input type="password" name="password" id = 'passwordLI' placeholder="Password"><i class="fa fa-lock"></i></input>
                            
                                <div class="g-recaptcha" style="margin-top: 10%;" data-sitekey="6Lf2x-IZAAAAALMzDGQ3989jbM0-iRozvWHqGvb9"></div>
                                <br/>
                                <div id = 'errorLI'></div>
                                <button type = 'button' id='login-button' class="form-btn text-center" style="margin-left: 20%;" onclick='logInValidate()'>Log In</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                </div>
                <!-- <div class='col-sm-4' style='left: 60%; font-family: Patua One;font-style: normal; font-weight: normal; font-size: 60px; line-height: 73px; text-align: center; color:#CEA68C;'>
                    "Greatness meets Speed"
                </div> -->
                <!-- <div class="col-sm-4" style='position: absolute; top: 25%; left:60%; width: 200px;  font-family: Patua One;font-style: normal; font-weight: normal; font-size: 60px; line-height: 73px; text-align: center; color:#CEA68C;'>
                <div>"Greatness meets Speed"</div>
                </div>
                <div class='col-sm-2'>
                    <img src="images/lines.jpg" style=' position:absolute; width: 177px; height: 300px; left: 83%; top: 39.5%; z-index:-1;'>
                </div>
            </div> -->
        </div>
    </div>
    <script>

    function signUpValidate(){
        document.getElementById("errorSU").innerHTML = '';
        var fullnameSU = document.getElementById("fullnameSU").value;
        var usernameSU = document.getElementById("UsernameSU").value;
        var emailSU = document.getElementById("emailSU").value;
        var passwordSU = document.getElementById("passwordSU").value;
        var teleSU = document.getElementById('teleSU').value;
        var contactSU = document.getElementById('contactSU').value;
        var errors = [];

            if (fullnameSU === "" || usernameSU === "" || emailSU === "" || passwordSU === "" || teleSU === '' || contactSU === ''){
                event.preventDefault();
                errors.push('Error: None of your fields can be empty');
            };

            if (!emailSU.includes('@') || !emailSU.includes('.com')){
                event.preventDefault();
                errors.push('Error: Please enter a valid email');
            };

            for (error of errors){
                document.getElementById("errorSU").innerHTML += `<p style = 'margin: 2px; font-size: 10px; color:red;'>${error}</p>`;
            }
        };

    function logInValidate(){
        var username = document.getElementById("usernameLI").value;
        var passwordLI = document.getElementById("passwordLI").value;

        if (username === "" || passwordLI === ""){
            document.getElementById("errorLI").innerHTML = `<p style = 'margin: 2px; font-size: 10px; color:red;'>Error: None of your fields can be empty</p>`;

        };
    };

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

        $(document).ready(function() {
            var signUp = $('.signup-but');
            var logIn = $('.login-but');


            signUp.on('click', function() {
                $('.login').fadeOut('slow').css('display', 'none');
                $('.sign-up').fadeIn('slow');

                $('.form-container').animate({
                    left: '10px'
                }, 'slow');
            });

            logIn.on('click', function() {
                $('.login').fadeIn('slow');
                $('.sign-up').fadeOut('slow').css('display', 'none');

                $('.form-container').animate({
                    left: '300px'
                }, 'slow');
            });
        });
    </script>

<script>
    $("#login-button").click(function() {
        var username = $("#usernameLI").val();
        var password = $("#passwordLI").val();
        var account_type = "customer"
        // console.log(account_type);
        serviceURL = "http://localhost:5005/authenticate";

        fetch(serviceURL, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
                "account_type": "customer"
            })
        })
        .then(function (response) {
            data = response.json();
            console.log(data);
            // account = {
            //     "account_type": data.account_type,
            //     "customer_ID": data.customer_ID
            // }
            // localStorage.setItem("account", account);
            // console.log(account);
            // location.replace("http://localhost/esd/project/delivery_order.html");
            return data
            // return response.json();
        })
        .then(function (result) {
            json = JSON.stringify({
                "username": result.data.username,
                "customer_ID": result.data.customer_ID,
                "account_type": "customer"
            });
            console.log(json);
            sessionStorage.setItem("account_details", json);
            location.replace("../customer/delivery_order.html");
        })
        .catch(function (error) {
            console.log("Error:", error);
        });

        // async () => {
        //     const data = await response;
        //     console.log(data);
        // };

        // $(async() => {
        //     try {
        //         const response = await fetch (serviceURL, {
        //             method: 'POST',
        //             headers: {
        //                 'Content-Type': 'application/json'
        //             },
        //             body: JSON.stringify({
        //                 "username": username,
        //                 "password": password,
        //                 "account_type": account_type
        //             })
        //         });
        //         const data = await response.json();
        //         if (response.ok){
        //             console.log(data);
        //         }
        //         else {
        //         console.log("There is an error in logging in: Error " + response.status);
        //         }
        //     }
        //     catch(error){
        //         console.log(error);
        //     }
        // });

    });

</script>
</body>

</html>