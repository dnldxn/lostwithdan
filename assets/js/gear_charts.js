---
---

{% assign categories = site.data.gear | group_by: "category" %}

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

    /* Manually define the Google color pallette so the colors are in a predictable order */
    var colors = ['#3366CC','#DC3912','#FF9900','#109618','#990099','#3B3EAC','#0099C6','#66AA00','#DD4477',
    '#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']

    /* Set chart options */
    var options = {
        legend : 'none',
        colors: colors
    };

    /* Instantiate and draw our chart, passing in some options. */
    var chart = new google.visualization.PieChart(document.getElementById('weight_chart'));
    chart.draw(data, options);

    /* Step through all rows of the dataset and color the circles in the summary table */
    for (var i = 0; i < data.getNumberOfRows(); i++) {
        /* Retrieve the name of the category in the first column of the data table */
        var name = data.getValue(i, 0);
        var color = colors[i];

        /* Draw a small circle in the first column of the summary table */
        $('#' + name + 'color svg circle' ).css('fill', color)
    }
}
