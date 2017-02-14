/* Selector for chart element */
var chartSelector = '#weight_chart';

/* Load chart packages and set callback function to run when the Visualization API is loaded */
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

/* Callback that creates and populates a data table, instantiates the pie chart, passes in the data and draws it. */
function drawChart() {

    /* Create the data table */
    var data = google.visualization.arrayToDataTable([
        ['Category', 'Weight'],
        {% for category in categories %}
            {% assign cat_weight = 0 %}
            {% for item in category.items %}
                {% assign w = item.weight | times: item.qty %}
                {% assign cat_weight = cat_weight | plus: w %}
            {% endfor %}

            ['{{ category.name }}', {{ cat_weight }}],
        {% endfor %}
    ]);

    /* Set chart options */
    var options = {
        legend : 'none'
    };

    /* Instantiate and draw our chart, passing in some options. */
    var chart = new google.visualization.PieChart(document.getElementById('weight_chart'));
    chart.draw(data, options);

    var length = $('#weight_chart svg g path').length

    /* Step through all the labels in the legend. */
    $('#weight_chart svg g path').each(function (i, v) {
        
        /* Retrieve the name of the category in the first column of the data table */
        var name = data.getValue(length - 1 - i, 0);
        var color = $(v).css('fill');

        /* Draw a small circle in the first column of the summary table */
        $('#' + name + 'color svg circle' ).css('fill', color)
    });
}
