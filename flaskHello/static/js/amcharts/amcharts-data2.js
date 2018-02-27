
// var chartData = [ {
//     "country": "13100",
//     "visits": 4252
//     }, {
//     "country": "7890",
//     "visits": 1882
//     }, {
//     "country": "1001",
//     "visits": 1809
//     }, {
//     "country": "2022",
//     "visits": 1322
//     }, {
//     "country": "13",
//     "visits": 1122
//     }];

var chartData = [{country:""}];
var country = ["USA", "China", "German", "Russia", "Japan"];

// Object-based setup
AmCharts.ready( function() {

    var chart = new AmCharts.AmSerialChart();
    chart.dataProvider = chartData;
    chart.categoryField = "country";
    chart.startDuration = 1;


    // var graph = new AmCharts.AmGraph();
    // graph.valueField = "visits";
    // graph.type = "column";
    // graph.legendValueText="[[category]]";

    // graph.fillAlphas = 0.5;
    // graph.balloonText = "[[category]]: <b>[[value]]</b>";

    // chart.addGraph( graph );

    for (var i=0; i < country.length ; i++) {
        //chartData[0]["val"+i] = Math.floor(Math.random() * 20);
        chartData[0][country[i]] = Math.floor(Math.random() * 20);
        console.log(chartData);
        var graph = new AmCharts.AmGraph();
        //graph.valueField = "val"+i;
        graph.valueField = country[i];
        //graph.title = "Graph #"+i;
        graph.title = country[i];
        graph.type = "column";
        graph.lineAlpha = 0;
        graph.fillAlphas = 1;
        //graph.legendValueText="[[category]]";
        //graph.balloonText = "[[category]]: <b>[[value]]</b>";
        chart.addGraph(graph);


    }

    var legend = new AmCharts.AmLegend();
    chart.addLegend(legend, 'legenddiv');

    chart.write("chartdiv2");

    $('#mySlider').on('input change', function() {
        var target = chart.graphs[0];
        target['fillAlphas'] = this.value;
        $('#demo').text(this.value);
        chart.validateNow();
    });

});

