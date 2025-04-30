 /*--#
File Name: deptPie.js
Description:javaScript for charts in department leader home page
Author: Umayma Jabbar (W19694885)
Co-Authors: None 
*/ 
 
 
 /*
    * Title: Doughnut Chart
      * Author: AnyChart.com
      * Date: <date>
      * Code version: version v8 
      * Availability:https://docs.anychart.com/Basic_Charts/Doughnut_Chart
*/

// create data
var data = [
    {x: "Red", value: 47700,
        normal:  {
           fill: "#16D95D"      
        }},
        {x: "Red", value: 47700,
            normal:  {
               fill: "#F3FF0F"      
            }},
            {x: "Red", value: 47700,
                normal:  {
                   fill: "#F10001"      
                }}, 
  ];
  
  // create a chart and set the data
  chart = anychart.pie(data); 
  // set the container id
  chart.container("pieChart_container");
  chart.title("department summary");
  // initiate drawing the chart
  chart.draw();

  /*
    * Title: Spline Area Chart
      * Author: AnyChart.com
      * Date: <date>
      * Code version: version v8 
      * Availability:https://docs.anychart.com/Basic_Charts/Spline_Area_Chart
*/
// create data
var linerdata = [
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
]
  
  // create a chart
  chart = anychart.area();
  
  // create an area series and set the data
  var series = chart.area(linerdata);
  
  series.normal().fill("#3A7D9A", 0.3);
  series.markers(true);
  series.markers().fill("white")
  chart.background().fill({
    keys: ["#fff", "#B2CFD1", "#fff"],
    angle: 90,
  });
  chart.background().stroke("2  #B2CFD1");
  // set the container id
  chart.container("lContainer");
  chart.title("progress over time");
  // initiate drawing the chart
  chart.draw();
  

  /*
    * Title: Bar Chart
      * Author: AnyChart.com
      * Date: <date>
      * Code version: version v8 
      * Availability:https://docs.anychart.com/Basic_Charts/Bar_Chart
*/
// create a data set
var bardata = anychart.data.set([
    ["Team 4", 20, 3, 5],
    ["Team 3", 12, 5, 23],
    ["Team 1", 5, 14, 12],
    ["Team 2", 40, 4, 3],
    ["Team 6", 3, 12, 10]
  ]);
  
  // map the data
  var seriesData_1 = bardata.mapAs({x: 0, value: 1});
  var seriesData_2 = bardata.mapAs({x: 0, value: 2});
  var seriesData_3 = bardata.mapAs({x: 0, value: 3});
  
  // create a chart
  var chart = anychart.bar();
  
  // create bar series and set the data
  var series1 = chart.bar(seriesData_1);
  series1.name("Red Votes");
  series1.normal().fill("#E41A1A");
  series1.normal().stroke("#E41A1A");



  var series2 = chart.bar(seriesData_2);
  series2.name("Yellow Votes");
  series2.normal().fill("#FFE75D");
  series2.normal().stroke("#FFE75D");
  
  var series3 = chart.bar(seriesData_3);
  series3.name("Green Votes");
  series3.normal().fill("#16D95D");
  series3.normal().stroke("#16D95D");
  
  // set chart title and legend
  chart.title("Votes per Team (Stacked Bar)");
  chart.legend(true);
  
 
  
  // set the container id
  chart.container("barChart_Container");
  
  // draw the chart
  chart.draw();


  //for scrollbar
  function scrollLeft() {
    document.getElementById('scrollContainer').scrollBy({ left: -300, behavior: 'smooth' });
  }

  function scrollRight() {
    document.getElementById('scrollContainer').scrollBy({ left: 300, behavior: 'smooth' });
  }