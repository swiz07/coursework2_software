let currentStep=1;
function showStep(step){
    document.querySelectorAll('.step')
    .forEach((e)=>e.classList.remove('active'));

    document.getElementById(`step${step}`)
    .classList.add('active');

    document.querySelectorAll('.step-indicator span')
    .forEach((e, index)=>{
        e.classList.toggle('active', index+1===step);
    });

    document.getElementById('prev-btn').disabled=step===1;
    document.getElementById('next-btn').innerHTML=step===3?
    'Finish': 'Next';
    if(step ===3){
      document.getElementById('next-btn').type='submit';
    }
    else{
      document.getElementById('next-btn').type='button';
    }
}


function arePasswordsMatching(){
    const password=document.querySelector('[name="password"]').value;
    const confirmPassword=document.querySelector('[name="confirm-password"]').value;

    if(password !==confirmPassword){
        document.getElementById("result").innerHTML="Password do not match";
        return false;
    }

    document.getElementById("result").innerHTML="";
    return true;
}

function nextStep(){
    //checks if password match on step 1
    if(currentStep===1 && !arePasswordsMatching()){
        return;
    }

    if(currentStep===1){
      let username=document.querySelector('[name="username"]').value;
      let email=document.querySelector('[name="email"]').value;
      let password=document.querySelector('[name="password"]').value;
      let confirmPassword=document.querySelector('[name="confirm-password"]').value;

      if(!username || !email || !password || !confirmPassword){
        document.getElementById("result").innerHTML="Please fill in all the required fields in step 1";
        return;
      }
    }

    if(currentStep===2){
      let role=document.querySelector('input[name="role"]:checked');
      if(!role){
        document.getElementById("result").innerHTML="Please enter the required role for step 2";
        return;
      }
    }

    if(currentStep===3){
      let name=document.querySelector('[name="name"]').value;
      let phone=document.querySelector('[name="phone"]').value;
      let address=document.querySelector('[name="address"]').value;

      if(!name || !phone || !address){
        document.getElementById("result").innerHTML="Please fill in all the required fields in step 3";
        return;
      }
    }
    if(currentStep <3){
        currentStep++;
        showStep(currentStep);
    }
    else{
        document.getElementById("result").innerHTML="Submitted successfully";
    }
}

function prevStep(){
    if(currentStep >1){
        currentStep--;
        showStep(currentStep);
    }
}

var passInput = document.getElementById("psw");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");

// When the user clicks on the password field, show the message box
passInput.onfocus = function() {
  document.getElementById("message").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
passInput.onblur = function() {
  document.getElementById("message").style.display = "none";
}

// When the user starts to type something inside the password field
passInput.onkeyup = function() {
  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if(passInput.value.match(lowerCaseLetters)) {  
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
  }
  
  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(passInput.value.match(upperCaseLetters)) {  
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(passInput.value.match(numbers)) {  
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }
  
  // Validate length
  if(passInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }
}