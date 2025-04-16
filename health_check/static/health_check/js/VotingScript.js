
  function showCardDetail(cardId) {
    const detailTitleEl = document.getElementById("detailCardTitle");
    const detailCardIdEl = document.getElementById("detailCardId");
    const redCountEl     = document.getElementById("detailRedCount");
    const yellowCountEl  = document.getElementById("detailYellowCount");
    const greenCountEl   = document.getElementById("detailGreenCount");
  

    if (!cardData[cardId]) return;
  
    // Fill in
    detailTitleEl.textContent = cardData[cardId].title;
    detailCardIdEl.value = cardId;
    redCountEl.textContent    = cardData[cardId].red;
    yellowCountEl.textContent = cardData[cardId].yellow;
    greenCountEl.textContent  = cardData[cardId].green;
  
    // Update chart
    updatePieChart(
      cardData[cardId].red,
      cardData[cardId].yellow,
      cardData[cardId].green
    );
  }
  
  // Uses Chart.js 
  let pieChartRef = null;
  function updatePieChart(redVal, yelVal, grnVal) {
    if (!pieChartRef) {
      const ctx = document.getElementById("detailPieChart");
      pieChartRef = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Red','Yellow','Green'],
          datasets: [{
            data: [redVal, yelVal, grnVal],
            backgroundColor: ['#dc3545','#ffc107','#28a745']
          }]
        },
        options: {responsive:false}
      });
    } else {
      pieChartRef.data.datasets[0].data = [redVal, yelVal, grnVal];
      pieChartRef.update();
    }
  }
  