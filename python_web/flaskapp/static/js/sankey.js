google.charts.load("current", {packages:["sankey"]});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
    var data = new google.visualization.DataTable();
    //var data = sankeyvalue;
    data.addColumn('string', 'From');
    data.addColumn('string', 'To');
    data.addColumn('number', 'Weight');
    // data.addRows([
    //     [ '903(0)', '16(1)', 1 ],
    //     [ '1003(0)', '16384(1)', 1 ],
    //     [ '5000(0)', '5008(1)', 1 ],
    //     [ '16(1)', '15(2)', 1 ],
    //     [ '5008(1)', '1000(2)', 1 ],
    //     [ '16384(1)', '903(2)', 1 ],
    //     [ '15(2)', '16(3)', 1 ],
    //     [ '903(2)', '16(3)', 1 ],
    //     [ '1000(2)', '16(3)', 1 ],
    // ]);
    
    data.addRows(sankeyvalue)
    // Set chart options
    var options = {
        
        sankey: {
            node: {
                colors: sankeycolor,
                //colors: ['#42A5F5', '#EF5350', '#EF5350', '#42A5F5', '#EF5350', '#EF5350']
                //nodePadding: 
                
            },
            link: {
                colorMode: 'gradient',
            }
        }
    };
    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.Sankey(document.getElementById('sankeychart'));
    chart.draw(data, options);
}