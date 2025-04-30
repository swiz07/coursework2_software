 /*--#
File Name: deptPie.js
Description:javaScript for piechart in engineer and team leader home page
Author: Umayma Jabbar (W19694885)
Co-Authors: None 
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
  chart.title("team summary");
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