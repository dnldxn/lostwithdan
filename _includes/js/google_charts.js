// Load chart packages and set callback function to run when the Visualization API is loaded
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table, instantiates the pie chart, passes in the data and draws it.
function drawChart() {
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('date', '');
    data.addColumn('number', 'Miles');
    data.addRows([ 
        [new Date(2017,3,8), 7],
        [new Date(2017,3,9), 10],
        [new Date(2017,3,10), 12],
        [new Date(2017,3,11), 11],
        [new Date(2017,3,12), 14],
        [new Date(2017,3,13), 15],
        [new Date(2017,3,14), 9],
        [new Date(2017,3,15), 8],
        [new Date(2017,3,16), 14],
        [new Date(2017,3,17), 13],
        [new Date(2017,3,18), 16],
        [new Date(2017,3,19), 15],
        [new Date(2017,3,20), 9],
        [new Date(2017,3,21), 8],
        [new Date(2017,3,22), 14],
        [new Date(2017,3,23), 13],
        [new Date(2017,3,24), 16]
    ]);

    // Set chart options
    var options = {
        chart: {
            title: 'Pace'
        },
        hAxis: {
            format: 'MMM d',
            gridlines: {
                color: 'transparent'
            },
            textPosition: 'in'
        },
        interpolateNulls: true,
        legend: { position: 'none' },
        lineWidth: 4,
        vAxis: {
            gridlines: {
                color: 'transparent'
            }
        }
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('paceChart'));
    chart.draw(data, options);
}
