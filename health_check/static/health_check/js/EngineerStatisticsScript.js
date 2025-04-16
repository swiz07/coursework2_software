document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded");
  
    const pie = document.getElementById("mainPieChart");
    const line = document.getElementById("lineChart");
    const bar = document.getElementById("barChart");
  
    if (pie) {
      new Chart(pie, {
        type: 'pie',
        data: {
          labels: ["Red", "Yellow", "Green"],
          datasets: [{
            data: [969, 148, 463],
            backgroundColor: ["#e74c3c", "#f1c40f", "#2ecc71"]
          }]
        }
      });
    } else {
      console.warn("mainPieChart not found");
    }
  
    if (line) {
      new Chart(line, {
        type: 'line',
        data: {
          labels: Array(12).fill("session 1"),
          datasets: [{
            label: "Quality",
            data: [98, 85, 76, 60, 55, 63, 80, 75, 50, 30, 20, 90],
            borderColor: "#3498db",
            fill: false
          }]
        }
      });
    } else {
      console.warn("lineChart not found");
    }
  
    if (bar) {
      new Chart(bar, {
        type: 'bar',
        data: {
          labels: ["card 1", "card 1", "card 1", "card 1", "card 1", "card 1", "card 1", "card 1", "card 1", "card 1", "card 1", "card 1"],
          datasets: [
            {
              label: 'Red',
              backgroundColor: "#e74c3c",
              data: [23, 28, 15, 32, 25, 30, 12, 9, 16, 21, 14, 27]
            },
            {
              label: 'Yellow',
              backgroundColor: "#f1c40f",
              data: [30, 25, 35, 18, 20, 30, 15, 10, 14, 28, 22, 25]
            },
            {
              label: 'Green',
              backgroundColor: "#2ecc71",
              data: [45, 47, 50, 49, 55, 40, 73, 81, 70, 51, 64, 48]
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              max: 100
            }
          }
        }
      });
    } else {
      console.warn("barChart not found");
    }
  });
  