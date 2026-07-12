// Navbar shadow while scrolling

window.addEventListener("scroll", function(){

    const navbar = document.querySelector(".navbar");

    if(window.scrollY > 50){
        navbar.classList.add("shadow");
    }
    else{
        navbar.classList.remove("shadow");
    }

});

// Welcome Message

console.log("Salon Booking Pro Loaded Successfully");

function togglePassword(){

    let password = document.getElementById("password");

    if(password.type === "password"){
        password.type = "text";
    }
    else{
        password.type = "password";
    }

}