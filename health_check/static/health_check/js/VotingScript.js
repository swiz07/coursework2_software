let detailChart;

// 1) Initialize the pie chart
function initDetailChart() {
  const ctx = document.getElementById('detailPieChart').getContext('2d');
  detailChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Red','Yellow','Green'],
      datasets: [{
        data: [0,0,0],
        backgroundColor: ['#dc3545','#ffc107','#28a745']
      }]
    },
    options: {
      maintainAspectRatio: true,
      responsive: true
    }
  });
}

// 2) Bind click handlers on all cards
function bindCardClicks() {
  document.querySelectorAll('.cardItem[data-card-id]').forEach(card => {
    card.addEventListener('click', () => {
      const id = card.dataset.cardId;
      showCardDetail(id);
    });
  });
}

// 3) When a card is clicked
function showCardDetail(id) {
  const d = cardData[id];
  if (!d) return console.warn(`No data for card ${id}`);

  // fill hidden form field
  document.getElementById('detailCardId').value = id;

  // update title & badges
  document.getElementById('detailCardTitle').textContent = d.title;
  document.getElementById('detailRedCount').textContent    = d.red;
  document.getElementById('detailYellowCount').textContent = d.yellow;
  document.getElementById('detailGreenCount').textContent  = d.green;

  // update pie-chart
  detailChart.data.datasets[0].data = [d.red, d.yellow, d.green];
  detailChart.update();

  // clear prior vote selection
  const prev = document.querySelector('input[name="vote_choice"]:checked');
  if (prev) prev.checked = false;
  document.getElementById('reasonInput').value = '';
}

// 4) On DOM load, init everything
document.addEventListener('DOMContentLoaded', () => {
  initDetailChart();
  bindCardClicks();
});
