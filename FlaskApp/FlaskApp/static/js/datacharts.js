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

function champPickRate(regions, tiers, results_url) {

    query_url = getQueryURL(regions, tiers, 'champions', results_url);

    initialiseChampPickrate();

}

function initialiseChampPickrate(){

    $.getJSON(query_url, function(data){
        data = data.pickrate;
        console.log(data);

        var max = 0
        for (i in data){
            max = Math.max(max, data[i][2])
        }

        var width = $('#chart-container').width();
        var barHeight = 35;
        var startwidth = 150;

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
            .duration(3000)
            .attr("width", function(d) { return x(d[2]);});

        bars.enter().append("rect")
            .attr("transform", function(d, i) {return "translate(" + startwidth + "," + i * barHeight + ")";})
            .style("align", "center")
            .attr("width", 0)
            .attr("height", barHeight - 1)
            .transition()
            .duration(3000)
            .attr("width", function(d) { return x(d[2]);});


        bars.exit().select("rect").remove();
/*
        //update champ icon
        var bars = chart.selectAll("svg:image").data(data);

        bars.attr("height", barHeight - 1)
            .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d[1] + ".png";});

        bars.enter().append("svg:image")
            .attr("transform", function(d, i) {return "translate(" + (startwidth-barHeight) + "," + i * barHeight + ")";})
            .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d[1] + ".png";})
            .attr("width", barHeight)
            .attr("height", barHeight);

        bars.exit().select("svg:image").remove();*/

    //update champ text
        var bars = chart.selectAll("text").data(data);

        bars.attr("height", barHeight - 1)
            .transition()
            .text(function(d){return d[1] + '-' + d[2] + '-' + d[3]});


        bars.enter().append("text")
            .transition()
            .attr("transform", function(d, i) {return "translate(" + (0) + "," + i * barHeight + ")";})
            .attr("dy", barHeight/2)
            .text(function(d){return d[1] + '-' + d[2] + '-' + d[3]});

        bars.exit().select("text").remove();

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



