const TEAM_DATA   = window.TEAM_DATA;
const COLORS      = window.COLORS;
const DEFAULT_TEAM = window.DEFAULT_TEAM;

const listGroup   = document.querySelector('.team-list');
const pieCtx      = document.getElementById('pieChart').getContext('2d');
const barCtx      = document.getElementById('barChart').getContext('2d');
const ringEls     = document.querySelectorAll('#ring-container .ring');
const ringLabels  = document.querySelectorAll('.ring-label');
const ringTitle   = document.getElementById('ring-title');
const progressKPI = document.getElementById('progressKPI');

let pieChart, barChart, ringCharts = {}, currentId = DEFAULT_TEAM;


listGroup.querySelectorAll('a[data-team]').forEach(a => {
  if (a.dataset.team === DEFAULT_TEAM) {
    a.classList.add('active');
  }
});

// initialize charts
function initCharts(){
  pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
      labels:['Red','Amber','Green'],
      datasets:[{
        data:[0,0,0],
        backgroundColor:[COLORS.red,COLORS.amber,COLORS.green]
      }]
    },
    options:{ plugins:{ legend:{ position:'bottom' }}}
  });

  barChart = new Chart(barCtx, {
    type: 'bar',
    data: {
      labels:['Red','Amber','Green'],
      datasets:[{
        label:'Votes',
        data:[0,0,0],
        backgroundColor:[COLORS.red,COLORS.amber,COLORS.green]
      }]
    },
    options:{ plugins:{ legend:{ display:false }}}
  });

  ringEls.forEach(el => {
    const clr = el.dataset.color;
    const ctx = el.querySelector('canvas').getContext('2d');
    ringCharts[clr] = new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets:[{
          data:[1,1],
          backgroundColor:[COLORS[clr],'transparent'],
          cutout:'75%'
        }]
      },
      options:{ plugins:{ legend:{ display:false}, tooltip:{ enabled:false }}, animation:false }
    });
  });
}

// render a team’s data
function render(teamId){
  const d = TEAM_DATA[teamId];
  if (!d) return;
  ringTitle.textContent = d.name;

  ['red','amber','green'].forEach((c,i) => {
    const cnt   = d[c];
    const total = d.red + d.amber + d.green || 1;
    ringLabels[i].textContent = cnt;
    ringCharts[c].data.datasets[0].data = [cnt, total - cnt];
    ringCharts[c].update();
  });

  pieChart.data.datasets[0].data = [d.red, d.amber, d.green];
  barChart.data.datasets[0].data = [d.red, d.amber, d.green];
  pieChart.update();
  barChart.update();

  const pct = Math.round((d.green - d.red)/(d.red + d.amber + d.green || 1)*100);
  progressKPI.textContent = pct + '%';
  progressKPI.classList.toggle('text-success', pct >= 0);
  progressKPI.classList.toggle('text-danger', pct < 0);
}

// switch team on click
listGroup.addEventListener('click', e => {
  const a = e.target.closest('a[data-team]');
  if (!a) return;
  listGroup.querySelector('.active').classList.remove('active');
  a.classList.add('active');
  currentId = a.dataset.team;
  render(currentId);
});


initCharts();
render(currentId);
