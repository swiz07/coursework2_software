/*
    * Title: Heat Map Chart
      * Author: AnyChart.com
      * Date: <date>
      * Code version: version v8 
      * Availability: https://docs.anychart.com/Basic_Charts/Heat_Map_Chart
*/
var data= [
    {x:"Dept 1", y:"Team 1", fill:"#63D88E"}, 
    {x:"Dept 1", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 1", y:"Team 3", fill:"#DF6666" },
    {x:"Dept 1", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 1", y:"Team 5", fill:"#DF6666" },
    {x:"Dept 1", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 1", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 1", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 1", y:"Team 9", fill:"#63D88E" },
    {x:"Dept 1", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 2", y:"Team 1", fill:"#EFE08E" },
    {x:"Dept 2", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 2", y:"Team 3", fill:"#63D88E" },
    {x:"Dept 2", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 2", y:"Team 5", fill:"#EFE08E" },
    {x:"Dept 2", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 2", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 2", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 2", y:"Team 9", fill:"#DF6666" },
    {x:"Dept 2", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 3", y:"Team 1", fill:"#63D88E"  },
    {x:"Dept 3", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 3", y:"Team 3", fill:"#DF6666" },
    {x:"Dept 3", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 3", y:"Team 5", fill:"#DF6666" },
    {x:"Dept 3", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 3", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 3", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 3", y:"Team 9", fill:"#63D88E" },
    {x:"Dept 3", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 4", y:"Team 1", fill:"#EFE08E" },
    {x:"Dept 4", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 4", y:"Team 3", fill:"#63D88E" },
    {x:"Dept 4", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 4", y:"Team 5", fill:"#EFE08E" },
    {x:"Dept 4", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 4", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 4", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 4", y:"Team 9", fill:"#DF6666" },
    {x:"Dept 4", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 5", y:"Team 1", fill:"#63D88E" },
    {x:"Dept 5", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 5", y:"Team 3", fill:"#DF6666" },
    {x:"Dept 5", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 5", y:"Team 5", fill:"#DF6666" },
    {x:"Dept 5", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 5", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 5", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 5", y:"Team 9", fill:"#63D88E" },
    {x:"Dept 5", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 6", y:"Team 1", fill:"#EFE08E" },
    {x:"Dept 6", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 6", y:"Team 3", fill:"#63D88E" },
    {x:"Dept 6", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 6", y:"Team 5", fill:"#EFE08E" },
    {x:"Dept 6", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 6", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 6", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 6", y:"Team 9", fill:"#DF6666" },
    {x:"Dept 6", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 7", y:"Team 1", fill:"#63D88E" },
    {x:"Dept 7", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 7", y:"Team 3", fill:"#DF6666" },
    {x:"Dept 7", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 7", y:"Team 5", fill:"#DF6666" },
    {x:"Dept 7", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 7", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 7", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 7", y:"Team 9", fill:"#63D88E" },
    {x:"Dept 7", y:"Team 10", fill:"#EFE08E" },


    {x:"Dept 8", y:"Team 1", fill:"#EFE08E" },
    {x:"Dept 8", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 8", y:"Team 3", fill:"#63D88E" },
    {x:"Dept 8", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 8", y:"Team 5", fill:"#EFE08E" },
    {x:"Dept 8", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 8", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 8", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 8", y:"Team 9", fill:"#DF6666" },
    {x:"Dept 8", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 9", y:"Team 1", fill:"#63D88E" },
    {x:"Dept 9", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 9", y:"Team 3", fill:"#DF6666" },
    {x:"Dept 9", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 9", y:"Team 5", fill:"#DF6666" },
    {x:"Dept 9", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 9", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 9", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 9", y:"Team 9", fill:"#63D88E" },
    {x:"Dept 9", y:"Team 10", fill:"#EFE08E" },

    {x:"Dept 10", y:"Team 1", fill:"#EFE08E" },
    {x:"Dept 10", y:"Team 2", fill:"#DF6666" },
    {x:"Dept 10", y:"Team 3", fill:"#63D88E" },
    {x:"Dept 10", y:"Team 4", fill:"#EFE08E" },
    {x:"Dept 10", y:"Team 5", fill:"#EFE08E" },
    {x:"Dept 10", y:"Team 6", fill:"#63D88E" },
    {x:"Dept 10", y:"Team 7", fill:"#DF6666" },
    {x:"Dept 10", y:"Team 8", fill:"#DF6666" },
    {x:"Dept 10", y:"Team 9", fill:"#DF6666" },
    {x:"Dept 10", y:"Team 10", fill:"#EFE08E" },

    
  
      

];


 

var chart = anychart.heatMap(data);
chart.container("container");
    chart.draw();
 

 

 // enable and configure scrollers
chart.xScroller().enabled(true);
chart.xZoom().setToPointsCount(8);
chart.yScroller().enabled(true);
chart.yZoom().setToPointsCount(4); 


chart.selected().hatchFill("forward-diagonal", 2, 20);
chart.normal().stroke("white");
chart.hovered().stroke("white");
chart.selected().stroke("black", 2);
 

  
 document.querySelector('.flip_btn a').addEventListener('click', function (e) {
    e.preventDefault();
    
    var chartsContainer = document.getElementById('charts');
    var heatmap = document.getElementById('container');
    var newChart = document.getElementById('new-chart');
  
    chartsContainer.classList.toggle('flipped');
  
    if (chartsContainer.classList.contains('flipped')) {
      heatmap.style.display = 'none';
      newChart.style.display = 'block';
    } else {
      heatmap.style.display = 'block';
      newChart.style.display = 'none';
    }
  });


  /*
    * Title: Spline Area Chart
      * Author: AnyChart.com
      * Date: <date>
      * Code version: version v8 
      * Availability:https://docs.anychart.com/Basic_Charts/Spline_Area_Chart
*/
  var linear = [
    {x:"Session 1", value:20 },
    {x:"Session 2", value:30 },
    {x:"Session 3", value:60 },
    {x:"Session 4", value:70 },
    {x:"Session 5", value:90 },
    {x:"Session 6", value:20 },
    {x:"Session 7",value:60  },
    {x:"Session 8" ,value:70 },
    {x:"Session 9"  ,value:80},
    {x:"Session 10" ,value:80 },

  ];
  chart = anychart.area();
  
  var series = chart.splineArea(linear);

  series.normal().fill("#3A7D9A", 0.3);
  series.markers(true);
  series.markers().fill("white")
  chart.container("LinearChart_Container");
  chart.background().fill({
    keys: ["#fff", "#B2CFD1", "#fff"],
    angle: 90,
  });
  chart.background().stroke("2  #B2CFD1");
  chart.draw();


