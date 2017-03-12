---
# This file needs a front-matter section for Jekyll to it to the output
---

{% assign categories = site.data.finances | group_by: "category" %}
{% assign total_amount = 0 %}

/* Load the Visualization API and the corechart package. */
google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    /* Create the data table. */
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Category');
    data.addColumn('number', 'Amount');

    /* Loop through each spending category, summing up all the individual purchases */
    data.addRows([
        {% for category in categories %}
        {% assign cat_amount = 0 %}
            {% for item in category.items %}
                {% assign cat_amount = cat_amount | plus: item.amount %}
            {% endfor %}

            {% assign total_amount = total_amount | plus: cat_amount %}

            ['{{ category.name | capitalize }}', {{ cat_amount }}],

        {% endfor %}
    ]);

    data.sort([{column: 1, desc: true}, {column: 0}]);

    /* Chart options */
    var options = {
        haxis: {
            format: 'currency'
        },
        legend: { position: 'none' }
    };

    /* Instantiate and draw the chart, passing in some options */
    var chart = new google.visualization.BarChart(document.getElementById('finance_bars'));
    chart.draw(data, options);

    /* Set total spent amount */
    document.getElementById('total_spent').textContent = 'Total Spent: ${{ total_amount }}'
}