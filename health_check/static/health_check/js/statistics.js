document.addEventListener("DOMContentLoaded", () => {
  const ctx     = window.STATS_CONTEXT;
  const colourMap = { red:"#e74c3c", amber:"#f1c40f", green:"#2ecc71" };

  const deptSel  = document.getElementById("deptSelect");
  const teamUL   = document.getElementById("teamList");
  const ringTit  = document.getElementById("ringTitle");
  const kpiNode  = document.getElementById("progressKPI");

  /* ring charts */
  const ringCharts = {};
  document.querySelectorAll(".ring").forEach(r => {
    const col = r.dataset.colour;
    ringCharts[col] = new Chart(r.querySelector("canvas").getContext("2d"), {
      type:"doughnut",
      data:{datasets:[{data:[1,1],
                       backgroundColor:[colourMap[col],"rgba(0,0,0,0)"],
                       cutout:"75%"}]},
      options:{plugins:{legend:{display:false},tooltip:{enabled:false}},
               responsive:false, animation:false}
    });
  });

  /* big ones */
  const pie = new Chart(document.getElementById("mainPieChart"), {
    type:"pie",
    data:{labels:["Red","Amber","Green"],
          datasets:[{data:[0,0,0],
                     backgroundColor:[colourMap.red, colourMap.amber, colourMap.green]}]},
    options:{plugins:{legend:{position:"bottom"}}}
  });

  const bar = new Chart(document.getElementById("barChart"), {
    type:"bar",
    data:{labels:["Red","Amber","Green"],
          datasets:[{data:[0,0,0],
                     backgroundColor:[colourMap.red, colourMap.amber, colourMap.green]}]},
    options:{plugins:{legend:{display:false}},
             scales:{y:{beginAtZero:true, ticks:{stepSize:1}}}}
  });

  /* render helper */
  function render(id){
    const d = ctx.teamData[id];
    if(!d) return;

    ringTit.textContent = d.name;
    const total = d.red + d.amber + d.green || 1;

    ["red","amber","green"].forEach((c,i)=>{
      ringCharts[c].data.datasets[0].data = [d[c], total-d[c]];
      ringCharts[c].update();
      document.querySelectorAll(".ring-label")[i].textContent = d[c];
    });

    pie.data.datasets[0].data = [d.red,d.amber,d.green];
    pie.update();

    bar.data.datasets[0].data = [d.red,d.amber,d.green];
    bar.update();

    const pct = Math.round((d.green - d.red) / total * 100);
    kpiNode.textContent = `${pct} %`;
    kpiNode.classList.toggle("text-danger", pct < 0);
    kpiNode.classList.toggle("text-success", pct >= 0);
  }

  /* select first team */
  const firstLi = teamUL.querySelector("li[data-team]");
  if(firstLi){ firstLi.classList.add("active"); render(firstLi.dataset.team); }

  /* click team */
  teamUL.addEventListener("click", e=>{
    const li = e.target.closest("li[data-team]");
    if(!li) return;
    teamUL.querySelectorAll(".active").forEach(x=>x.classList.remove("active"));
    li.classList.add("active");
    render(li.dataset.team);
  });

  /* department change */
  deptSel?.addEventListener("change", e=>{
    window.location = ctx.statUrl + "?department=" + encodeURIComponent(e.target.value);
  });
});
