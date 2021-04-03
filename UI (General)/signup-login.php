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
            width: 750px;
            height: 250px;
            margin: 0 auto;
            margin-top: 70px;
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
        }
        
        .bh {
            font-size: 30px;
            font-weight: 500;
        }
        
        .background button {
            position: absolute;
            left: 0;
            bottom: 60px;
        }
        
        
        .background .left button {
            left: 150px;
        }
        
        .background .right button {
            left: 550px;
        }
        
        .form-container {
            position: absolute;
            width: 375px;
            height: 400px;
            background-color:#EEE2CC;
            top: -28%;
            left: 20px;
            -webkit-box-shadow: 9px 10px 10px 0px rgba(0, 0, 0, 0.75);
            box-shadow: 9px 10px 10px 0px rgba(0, 0, 0, 0.75);
            border-radius: 20px 20px 20px 20px;
        }
        
        .sign-up,
        .login {
            margin: 40px;
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
            margin-left:20%;
            
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
            width: 80%;
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
        
    </style>
</head>

<body>

    <div class="container" id = 'background'>
    
        <div class="col-sm-12" style = 'float: left; margin-top: 9%'>
            <div class="wrapper" style = 'background-color: #9E8A81; border-radius:0px 10px 10px 0px;' >
            
            
                <div class="background">
                
                    <div class="left" style = 'text-align: center'>
                        <h2 class="bh" style = 'margin-top: 20%' ></b>Don't have an account?</b></h2>
                        <button class="back-btn signup-but" style='margin-bottom:3%;'>Sign Up</button>
                    </div>

                    <div class="right">
                        <h2 class="bh" style = 'margin-top: 20%; '>Already Registered?</h2>
                        <button class="back-btn login-but" style='margin-bottom:3%; left:70%'>Log In</button>
                    </div>
                </div>
                <div class="form-container">
                    <div class="sign-up">
                        <form method="post" action="#put into some registering processing page" >
                            <h2 class="form-header">Sign Up</h2>
                            <input type="text" name="fullname" id = 'fullnameSU' placeholder="Enter Full Name"><i class="fa fa-user"></i></input>
                            <input type="text" name="username" id = 'usernameSU' placeholder="Username"><i class="far fa-address-card"></i></input>
                            <input type="text" name="email" id = 'emailSU' placeholder="Email"><i class="fa fa-envelope-o"></i></input>
                            <input type="password" name="password" id='passwordSU' placeholder="Password"><i class="fa fa-lock"></i></input>
                            <button type="submit" class="form-btn " style="margin-left: 20%;" onclick = "signUpValidate()" >Sign Up</button>
                            <div id = "errorSU"></div>
                        </form>
                    </div>
                    <div class="my-5">
                        <div class="login hide ">
                            <form method="post"  action="../Main/process_login.php" >
                            <h2 class="form-header">Log In</h2>  
                            <input type="text" name="email" id = 'emailLI' placeholder="Email"><i class="fa fa-envelope-o"></i></input>
                            
                            <input type="password" name="password" id = 'passwordLI' placeholder="Password"><i class="fa fa-lock"></i></input>
                        
                            <div class="g-recaptcha" style="margin-top: 10%;" data-sitekey="6Lf2x-IZAAAAALMzDGQ3989jbM0-iRozvWHqGvb9"></div>
                            <br/>
                            <div id = 'errorLI'></div>
                            <button type = 'submit' class="form-btn text-center" style="margin-left: 20%;" onclick='logInValidate()'>Log In</button>
                            </form>
                        </div>

                    </div>
                
                </div>
            </div>
            <div class='container' style='position: absolute; width: 388px; height: 146px; left: 60%; top: 30%; font-family: Patua One;font-style: normal; font-weight: normal; font-size: 75px; line-height: 73px; text-align: center; color:#CEA68C;'>
                "Greatness meets Speed"
            </div>

            <img src="images/lines.jpg" style='position: absolute; width: 177px; height: 366px; left: 88.5%; top: 51%;'>
        </div>
    </div>
    <script>

    function signUpValidate(){
        document.getElementById("errorSU").innerHTML = '';
        var fullnameSU = document.getElementById("fullnameSU").value;
        var usernameSU = document.getElementById("usernameSU").value;
        var emailSU = document.getElementById("emailSU").value;
        var passwordSU = document.getElementById("passwordSU").value;
        var errors = [];

            if (fullnameSU === "" || usernameSU === "" || emailSU === "" || passwordSU === ""){
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
        var emailLI = document.getElementById("emailLI").value;
        var passwordLI = document.getElementByID("passwordLI").value;

        if (emailLI === "" || passwordLI === ""){
            document.getElementById("errorLI").innerHTML = `<p class = 'text-danger'>None of your fields can be empty</p>`;

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
                    left: '400px'
                }, 'slow');
            });
        });
    </script>
</body>

</html>