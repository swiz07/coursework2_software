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
}

function nextStep(){
    if(currentStep <3){
        currentStep++;
        showStep(currentStep);
    }
    else{
        document.getElementById("result")
        .innerHTML="Submitted successfully"
    }
}


function prevStep(){
    if(currentStep >1){
        currentStep--;
        showStep(currentStep);
    }
}