anychart.onDocumentReady(function () {
  var data = anychart.data.set([
    ["John", 10000, 12500],
    ["Jake", 12000, 15000],
    ["Peter", 13000, 16500],
    ["James", 10000, 13000],
    ["Mary", 9000, 11000],
    ["Mary", 9000, 11000],
    ["Mary", 9000, 11000],
    ["Mary", 9000, 11000],
    ["Mary", 9000, 11000],
    ["Mary", 9000, 11000],
    ["Mary", 9000, 11000],
    ["Mary", 9000, 11000],
  ]);

  var seriesData_1 = data.mapAs({ x: 0, value: 1 });
  var seriesData_2 = data.mapAs({ x: 0, value: 2 });

  var chart = anychart.column();

  var series1 = chart.column(seriesData_1);
  series1.name("Sales in 2015");
  series1.fill("#7A162F");      
  series1.stroke("#7A162F");    

  var series2 = chart.column(seriesData_2);
  series2.name("Sales in 2016");
  series2.fill("#7A162F 0.5");  
  series2.stroke("#7A162F 0.5");

  chart.barsPadding(0);
  chart.barGroupsPadding(2);

  chart.container("grafico");
  chart.draw();
});
