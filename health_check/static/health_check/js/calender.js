const calendarDates  = document.querySelector('.calendar-dates');
const monthYear = document.querySelector('#month-year');
const prevMonth = document.getElementById('prev-month');
const nextMonth = document.getElementById('next-month');


let currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

const months = [ 'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'];

function renderCalender(month,year) {
    calendarDates.innerHTML = '';
    monthYear.textContent = `${months [ month]} ${year}`;

    const firstDay = new Date (year, month, 1) .getDay();
    const MonthDays = new Date (year, month +1, 0).getDate();

    for( let i = 0; i<firstDay;i++) {
        const blank = document.createElement('div');
        calendarDates.appendChild(blank);
    }

    const today= new Date ();

    for(let i = 1; i <= MonthDays; i++) {
        const day = document.createElement('div');
        day.textContent = i;

        if (
            i === today.getDate () &&
            year === today.getFullYear() &&
            month ===today.getMonth()
        ) {
            day.classList.add('current-date');
        }
        calendarDates.appendChild(day);
    }
}
renderCalender(currentMonth, currentYear);

prevMonth.addEventListener('click', () => {
    currentMonth--;
    if(currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalender(currentMonth,currentYear);

});

nextMonth.addEventListener('click', () => {
    currentMonth++;
    if(currentMonth >11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalender(currentMonth,currentYear);

});


  /*
    * Title: Animated Skills Progress Chart
      * Author: Reza Farhadi
      * Date: October 2024
      * Code version: v5.3
      * Availability:https://bootstrapexamples.com/@reza-f/animated-skills-progress-chart
*/

document.addEventListener('DOMContentLoaded', () => {
    const voteItems = document.querySelectorAll('.vote-item');

    // Function to animate the progress circle
    const animateProgressCircle = (voteItem) => {
        const circle = voteItem.querySelector('.progress');
        const percent = parseInt(voteItem.dataset.percent); // Getting percentage from data attribute
        const percentText = voteItem.querySelector('.vote-percent');
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        const offset = circumference - (percent / 100) * circumference;

        // Set stroke-dashoffset to create the animation effect
        circle.style.strokeDashoffset = offset;

        // Animate percentage text
        let count = 0;
        const timer = setInterval(() => {
            if (count >= percent) {
                clearInterval(timer);
            } else {
                count++;
                percentText.textContent = count + '%';
            }
        }, 15); // Increase/decrease the delay for animation speed
    };

    // IntersectionObserver to trigger the animation when the element comes into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                animateProgressCircle(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    // Observe each vote item
    voteItems.forEach(vote => observer.observe(vote));
});
