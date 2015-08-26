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

function champBarChart(regions, tiers, results_url, mode) {

    query_url = getQueryURL(regions, tiers, 'champions', results_url);

    $.getJSON(query_url, function(data){
        if (mode == 'pickrate'){
            data = data.pickrate;
            panel = '#champ-pickrate-panel';
            chart = '#champ-pickrate-chart';
        } else {
            data = data.winrate;
            panel = '#champ-winrate-panel';
            chart = '#champ-winrate-chart';
        }
        var max = 0

        for (i in data){
            max = Math.max(max, data[i][2])
        }

        var width = $(panel).width();
        var barHeight = 50;
        var startwidth = 50;

        var x = d3.scale.linear()
            .domain([0, max])
            .range([0, (width-startwidth)*0.9]);

        var chart = d3.select(chart)
            .attr("width", width*0.9)
            .style("height", barHeight * data.length + 1);



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
                            return d[2] + '% ' + d[3];
                        } else {
                            return d[2] + '%';
                        }

            });


        text.enter().append("text")
            .attr("transform", function(d, i) {return "translate(" + (x(d[2]) + startwidth/2) + "," + i * barHeight + ")";})
            .attr("dy", barHeight/2 + 5)
            .text(function(d){
                    if (mode == 'pickrate'){
                            return d[2] + '%      ' + d[3];
                        } else {
                            return d[2] + '%';
                        }
                });

        text.exit().select("text").remove();

    });
}

function champScatterPlot(regions, tiers, results_url) {

    query_url = getQueryURL(regions, tiers, 'champions', results_url);

    $.getJSON(query_url, function(data){
        panel = '#champ-scatter-panel';
        chart = '#champ-scatter-chart';

        var max_pickrate = 0
        var max_winrate = 0

        for (i in data.winrate){
            max_winrate = Math.max(max_winrate, data.winrate[i][2]);
        }

        for (i in data.pickrate){
            max_pickrate = Math.max(max_pickrate, data.pickrate[i][2]);
        }


        scatterset = []
        for (i in data.pickrate){
            scatterset.push([data.pickrate[i][0],
                            data.pickrate[i][1],
                            data.pickrate[i][2],
                            data.winrate[i][2]]);
        }


        var width = $(panel).width();
        var height = $(panel).height();

        var x = d3.scale.log()
            .base(Math.E)
            .domain([Math.exp(1), max_pickrate])
            .range([0, width*0.9]);

        var y = d3.scale.log()
            .base(Math.E)
            .domain([Math.exp(1), max_winrate])
            .range([0, height*0.9]);

        var chart = d3.select(chart)
            .attr("width", width*0.9)
            .style("height", height*0.9);

        var circles = chart.selectAll("circle").data(scatterset);

        circles.attr("cx", function(d){ return x(d[2]);})
            .attr("cy", function(d){ return y(d[3]);})
            .attr("r", 5);

        circles.enter().append("circle")
            .attr("cx", function(d){ return x(d[2]);})
            .attr("cy", function(d){ return y(d[3]);})
            .attr("r", 5);

        circles.exit().select("cirlce").remove();

        var labels = chart.selectAll("text").data(scatterset);

        labels.attr("x", function(d){ return x(d[2]);})
            .attr("y", function(d){ return y(d[3]);})
            .text(function(d) {return d[1];});

        labels.enter().append("text")
            .attr("x", function(d){ return x(d[2]);})
            .attr("y", function(d){ return y(d[3]);})
            .attr("font-family", "sans-serif")
           .attr("font-size", "11px")
           .attr("fill", "red")
           .text(function(d) {return d[1];});


        labels.exit().select("text").remove();






    });

}










