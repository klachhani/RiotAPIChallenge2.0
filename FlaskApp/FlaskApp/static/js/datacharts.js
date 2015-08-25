function getQueryURL(regions, tiers, category, results_url){

    var query = []
    for (i in regions){
        if ($('#'+category+'-'+regions[i]).hasClass('active')){
        query.push('r='+regions[i]);
        }
    }
    for (i in tiers){
        if ($('#'+category+'-'+tiers[i]).hasClass('active')){
        query.push('t='+tiers[i]);
        }
    }
    query = query.join("&");
    return results_url + "?" + query;
}

function champChart(regions, tiers, results_url, mode) {

    query_url = getQueryURL(regions, tiers, 'champions', results_url);

    $.getJSON(query_url, function(data){
        if (mode == 'pickrate'){
            data = data.pickrate;
        } else {
            data = data.winrate;
        }
        data = data.slice(0,19);
        var max = 0

        for (i in data){
            max = Math.max(max, data[i][2])
        }

        var width = $('#chart-container').width();
        var barHeight = 50;
        var startwidth = 50;

        var x = d3.scale.linear()
            .domain([0, max])
            .range([0, width-startwidth]);

        var chart = d3.select(".champ-chart")
            .attr("width", width)
            .attr("height", barHeight * (data.length + 1));


        //update bars
        var bars = chart.selectAll("rect").data(data);

        bars.attr("height", barHeight - 1)
            .transition()
            .duration(1000)
            .attr("width", 0);


        bars.attr("height", barHeight - 1)
            .transition()
            .delay(1000)
            .duration(1000)
            .attr("width", function(d) { return x(d[2]);});

        bars.enter().append("rect")
            .attr("transform", function(d, i) {return "translate(" + startwidth + "," + i * barHeight + ")";})
            .style("align", "center")
            .attr("width", 0)
            .attr("height", barHeight - 1)
            .transition()
            .duration(1000)
            .attr("width", function(d) { return x(d[2]);});


        bars.exit().select("rect").remove();

        //update champ icon
        var img = chart.selectAll("image").data(data);

        img.attr("width", barHeight - 3)
            .transition()
            .delay(1000)
            .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d[1] + ".png";});

        img.enter().append("image")
            .attr("transform", function(d, i) {return "translate(" + (startwidth-barHeight) + "," + i * barHeight + ")";})
            .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d[1] + ".png";})
            .attr("width", barHeight - 3)
            .attr("height", barHeight - 3);

        img.exit().select("image").remove();

        //update champ text
        var text = chart.selectAll("text").data(data);

        text.attr("height", barHeight)
            .transition()
            .delay(1000)
            .attr("transform", function(d, i) {return "translate(" + (x(d[2]) + startwidth/2) + "," + i * barHeight + ")";})
            .text(function(d){
                    if (mode == 'pickrate'){
                            return d[1] + '      ' + d[2] + '%      ' + d[3];
                        } else {
                            return d[1] + '      ' + d[2] + '%';
                        }

            });


        text.enter().append("text")
            .attr("transform", function(d, i) {return "translate(" + (x(d[2]) + startwidth/2) + "," + i * barHeight + ")";})
            .attr("dy", barHeight/2 + 5)
            .text(function(d){
                    if (mode == 'pickrate'){
                            return d[1] + '      ' + d[2] + '%      ' + d[3];
                        } else {
                            return d[1] + '      ' + d[2] + '%';
                        }
                });

        text.exit().select("text").remove();

    });
}















function champWinRate(regions, tiers, results_url) {

    query_url = getQueryURL(regions, tiers, 'champions', results_url);

    $.getJSON(query_url, function(data){
        data = data.winrate;

        var max = 0
        for (i in data){
            max = Math.max(max, data[i][2])
        }

        console.log(data.length);


        var width = $('#chart-container').width()-60;
        var barHeight = 35;

        var x = d3.scale.linear()
            .domain([0, max])
            .range([0, width]);

        var chart = d3.select(".champ-chart")
            .attr("width", width)
            .attr("height", barHeight * (data.length + 1));


        chart.selectAll("g").remove();

        var bar = chart.selectAll("g")
            .data(data)
            .enter().append("g")
            .attr("transform", function(d, i) {return "translate(" + 0 + "," + i * barHeight + ")";});

        bar.append("rect")
            .attr("width", function(d) { return x(d[2]);})
            .attr("height", barHeight - 1);

        bar.append("text")
            .attr("x", function(d) { return x(d[2]) - 3; })
            .attr("y", barHeight / 2)
            .attr("dy", ".35em")
            .text(function(d) { return d[1] + " - " + d[2] +"%"; });


    });
}



