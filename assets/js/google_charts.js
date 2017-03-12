---
# This file needs a front-matter section for Jekyll to it to the output
---

/* Load chart packages and set callback function to run when the Visualization API is loaded */
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

/* Callback that creates and populates a data table, instantiates the pie chart, passes in the data and draws it. */
function drawChart() {
    /* Create the data table. */
    var data = new google.visualization.DataTable();
    data.addColumn('date', '');
    data.addColumn('number', 'Miles');
    data.addRows([
        {% for day in site.data.stats.miles_per_day %}
            [ new Date('{{ day[0] }}'), {{ day[1] }}],
        {% endfor %}
    ]);
    data.sort({column: 0, desc: false});

    /* Calculate a new column to hold the rolling average */
    var days = 7;
    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1, {
        type: 'number',
        calc: function (dt, row) {
            /* calculate moving average */
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

    /* Set chart options */
    var options = {
        bar: {
            groupWidth: '100%'
        },
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
            0: {type: 'bars'},
            1: {type: 'line'}
        },
        titleTextStyle: {
            color: '#5b5f63'  /* soften the text from black to light grey */
        },
        vAxis: {
            gridlines: {
                color: 'transparent'
            }
        }
    };

    /* Instantiate and draw our chart, passing in some options. */
    var chart = new google.visualization.ComboChart(document.getElementById('pace_chart'));
    chart.draw(view, options);
}
