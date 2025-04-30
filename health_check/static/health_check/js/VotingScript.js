let detailChart;

function initDetailChart() {
  const ctx = document.getElementById('detailPieChart').getContext('2d');
  detailChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Unsatisfied','Partially Satisfied','Satisfied'],
      datasets: [{
        data: [0,0,0],
        backgroundColor: ['#dc3545','#ffc107','#28a745']
      }]
    },
    options: {
      maintainAspectRatio: true,
      responsive: true,
      plugins: { legend: { display: false } }
    }
  });
}

function bindCardClicks() {
  document.querySelectorAll('.cardItem[data-card-id]')
    .forEach(card => card.addEventListener('click', () => {
      showCardDetail(card.dataset.cardId);
    }));
}

function showCardDetail(id) {
  const d = cardData[id];
  if (!d) return console.warn(`No data for card ${id}`);

  // form hidden
  document.getElementById('detailCardId').value = id;

  // header badges & title
  document.getElementById('detailCardTitle').textContent = d.title;
  document.getElementById('detailRedCount').textContent    = d.red;
  document.getElementById('detailYellowCount').textContent = d.yellow;
  document.getElementById('detailGreenCount').textContent  = d.green;

  // chart
  detailChart.data.datasets[0].data = [d.red, d.yellow, d.green];
  detailChart.update();

  // clear selects
  document.getElementById('voteValueSelect').value   = '';
  document.getElementById('voteOpinionSelect').value = '';
}

document.addEventListener('DOMContentLoaded', () => {
  initDetailChart();
  bindCardClicks();
});
