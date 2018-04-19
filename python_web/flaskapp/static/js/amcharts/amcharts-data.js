
// AmCharts data for Analytics As A Service Website

// Top 10 Error EventIDs chart
console.log("Amchart top 10 error ID");
//console.log(document.getElementById('myRange2').value);
  var chart = AmCharts.makeChart("chartdiv1", {
  "type": "serial",
  "theme": "light",
  "marginRight": 70,
  "dataProvider": dictlist_id,
  "valueAxes": [{
    "axisAlpha": 0,
    "position": "left",
    "title": "Frequency"
  }],
  "startDuration": 1,
  "graphs": [{
    "balloonText": "[[event]]: <b>[[value]]</b>",
    "fillColorsField": "color",
    "fillAlphas": 0.8,
    "lineAlpha": 0.2,
    "type": "column",
    "valueField": "frequency"
    
  }],
  "chartCursor": {
    "categoryBalloonEnabled": false,
    "cursorAlpha": 0,
    "zoomable": false
  },
  "categoryField": "id",
  "categoryAxis": {
    "gridPosition": "start",
    "labelRotation": 25,
    "title": "Event ID"
  },
  "titles": [{
    "text": "Top Error ID",
    "size": 15
  }, {
    "text":filename,
    "bold": false
  }],
  "export": {
    "enabled": true
  }

});

