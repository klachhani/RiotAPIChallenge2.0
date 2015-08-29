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

function championsBarChart(queryType, regions, tiers, results_url) {

    if ($("#champions-descending").hasClass('active')){descending = true;} else {descending = false;}
    if ($("#champions-per5min").hasClass('active')) {per5min = "-per5min";} else {per5min = "";}

    charts = ['pickrate', 'winrate', 'kills', 'deaths', 'assists', 'physicalDamageDealtToChampions', 'magicDamageDealtToChampions', 'trueDamageDealtToChampions', 'goldEarned', 'minionsKilled', 'wardsPlaced'];
    per5minCharts = ["", "", per5min, per5min, per5min, per5min, per5min, per5min, per5min, per5min, per5min];

    if ($('#' + queryType + '-'+'won').hasClass('active') && !$('#' + queryType + '-'+'lost').hasClass('active')){
        outcome = 'won';
    } else if ($('#' + queryType + '-'+'lost').hasClass('active') && !$('#' + queryType + '-'+'won').hasClass('active')){
        outcome = 'lost';
    } else {
        outcome = 'total'
    }
    query_url = getQueryURL(regions, tiers, queryType, results_url);
    //queryType = 'champions'

    $.getJSON(query_url, function(data){
        data = data[outcome];

        for (c in charts){
            mode = charts[c];
            per5min = per5minCharts[c];

            console.log(mode);
            console.log(per5min);

            dataSorted = data.sort(function(a,b){
                return parseFloat(a[mode+per5min])-parseFloat(b[mode+per5min]);
            });

            if (descending == true){dataSorted = dataSorted.reverse()}

            console.log(dataSorted);

            panel = '#' + queryType + '-' + mode + '-panel';
            chart = '#' + queryType + '-' + mode + '-chart';

            mode = mode + per5min;

            var max = 0
            for (i in data){
                max = Math.max(max, dataSorted[i][mode])
            }

            var width = $(panel).width();
            var barHeight = 50;
            var startwidth = 50;

            var x = d3.scale.linear()
                .domain([0, max])
                .range([0, (width-startwidth)*0.90]);

            var chart = d3.select(chart)
                .attr("width", width*0.90)
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
                .attr("width", function(d) { return x(d[mode]);});

            bars.enter().append("rect")
                .attr("transform", function(d, i) {return "translate(" + startwidth + "," + i * barHeight + ")";})
                .style("align", "center")
                .attr("width", 0)
                .attr("height", barHeight - 1)
                .transition()
                .duration(1000)
                .attr("width", function(d) { return x(d[mode]);});


            bars.exit().select("rect").remove();

            //update champ icon
            var img = chart.selectAll("image").data(data);

            img.attr("width", barHeight - 3)
                .transition()
                .delay(1000)
                .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d['key'] + ".png";});

            img.enter().append("image")
                .attr("transform", function(d, i) {return "translate(" + (startwidth-barHeight) + "," + i * barHeight + ")";})
                .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d['key'] + ".png";})
                .attr("width", barHeight - 3)
                .attr("height", barHeight - 3);

            img.exit().select("image").remove();

            //update champ text
            var text = chart.selectAll("text").data(data);

            text.attr("height", barHeight)
                .transition()
                .delay(1000)
                .attr("transform", function(d, i) {return "translate(" + (x(d[mode]) + startwidth/2) + "," + i * barHeight + ")";})
                .text(function(d){return d[mode];});


            text.enter().append("text")
                .attr("transform", function(d, i) {return "translate(" + (x(d[mode]) + startwidth/2) + "," + i * barHeight + ")";})
                .attr("dy", barHeight/2 + 5)
                .text(function(d){return d[mode];});

            text.exit().select("text").remove();
        }
    });
}