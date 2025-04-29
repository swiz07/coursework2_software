
const cardData = {
    {% for c in user_cards %}
    "{{ c.id }}": {
      red:    {{ c.red_count }},
      yellow: {{ c.yellow_count }},
      green:  {{ c.green_count }},
      title:  "{{ c.title|escapejs }}"
    }{% if not forloop.last %},{% endif %}
    {% endfor %}
  };
  
  let detailPie, detailRedBadge, detailYellowBadge, detailGreenBadge;
  
  
  document.addEventListener('DOMContentLoaded', () => {
    detailRedBadge    = document.getElementById('detailRedCount');
    detailYellowBadge = document.getElementById('detailYellowCount');
    detailGreenBadge  = document.getElementById('detailGreenCount');
  
    const ctx = document.getElementById('detailPieChart').getContext('2d');
    detailPie = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Red','Yellow','Green'],
        datasets: [{
          data: [0,0,0],
          backgroundColor: ['#db4b4b','#f2c94c','#27ae60']
        }]
      },
      options: { plugins: { legend: { position: 'bottom' } } }
    });
  });
  
  function showCardDetail(cardId) {
    const d = cardData[cardId];
    document.getElementById('detailCardId').value = cardId;
    document.getElementById('detailCardTitle').textContent = d.title;
  
    detailRedBadge.textContent    = d.red;
    detailYellowBadge.textContent = d.yellow;
    detailGreenBadge.textContent  = d.green;
  
    detailPie.data.datasets[0].data = [d.red, d.yellow, d.green];
    detailPie.update();
  }
  