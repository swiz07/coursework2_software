 /*--#
File Name: calender.js
Description:javaScript for calender in engineer and team leader home pages
Author: Umayma Jabbar (W19694885)
Co-Authors: None 
*/

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


  
