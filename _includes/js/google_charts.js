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
        [new Date(2017,3,8),    7],
        [new Date(2017,3,9),    10],
        [new Date(2017,3,10),   12],
        [new Date(2017,3,11),   11],
        [new Date(2017,3,12),   14],
        [new Date(2017,3,13),   15],
        [new Date(2017,3,14),   9],
        [new Date(2017,3,15),   8],
        [new Date(2017,3,16),   14],
        [new Date(2017,3,17),   13],
        [new Date(2017,3,18),   16],
        [new Date(2017,3,19),   15],
        [new Date(2017,3,20),   9],
        [new Date(2017,3,21),   8],
        [new Date(2017,3,22),   14],
        [new Date(2017,3,23),   13],
        [new Date(2017,3,24),   16],
        [new Date(2017,3,25),    12],
        // [new Date(2017,3,26),    15],
        // [new Date(2017,3,27),   17],
        // [new Date(2017,3,28),   16],
        // [new Date(2017,3,29),   19],
        // [new Date(2017,3,30),   20],
        // [new Date(2017,3,31),   14],
        // [new Date(2017,4,1),   13],
        // [new Date(2017,4,2),   19],
        // [new Date(2017,4,3),   18],
        // [new Date(2017,4,4),   21],
        // [new Date(2017,4,5),   20],
        // [new Date(2017,4,6),   0],
        // [new Date(2017,4,7),   16],
        // [new Date(2017,4,8),   19],
        // [new Date(2017,4,9),   19],
        // [new Date(2017,4,10),   18]
    ]);

    // Calculate a new column to hold the rolling average
    var days = 7;
    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1, {
        type: 'number',
        calc: function (dt, row) {
            // calculate moving average
            var total = 0;
            var i = row;
            while(i >= 0 && row - i < days ) {
                total += data.getValue(i, 1);
                i--;
            }
            
            var avg = total / (row - i);
            return {v: avg, f: avg.toFixed(2)};
        }
    }]);

    // Set chart options
    var options = {
        title: 'Pace (Miles)',
        hAxis: {
            format: 'MMM d',
            gridlines: {
                color: 'transparent'
            },
            showTextEvery: 1
        },
        
        height: 120,
        legend: { position: 'none' },
        lineWidth: 4,
        series: {
            0: {type: 'bars', lineWidth: 100 },
            1: {type: 'line', lineDashStyle: [8, 4]}
        },
        vAxis: {
            gridlines: {
                color: 'transparent'
            }
        }
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.ComboChart(document.getElementById('pace_chart'));
    chart.draw(view, options);
}
