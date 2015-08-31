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

function championsBarChart(queryType, regions, tiers, results_url, champsSelected, champsLength) {

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

        champsSelectedData = []

        for (d in data){
            for (c in champsSelected){
                if (champsSelected[c] == data[d]['name']){
                    champsSelectedData.push(data[d]);
                    break;
                }
            }
        }

        for (c in charts){
            mode = charts[c];
            per5min = per5minCharts[c];

            dataSorted = champsSelectedData.sort(function(a,b){
            if (a[mode+per5min] == b[mode+per5min]){
                if (a['name'] < b['name']) return 1;
                if (a['name'] > b['name']) return -1;
            } else
                return parseFloat(a[mode+per5min])-parseFloat(b[mode+per5min]);
            });

            if (descending == true){dataSorted = dataSorted.reverse()}

            dataSorted = dataSorted.slice(0, champsLength);



            panel = '#' + queryType + '-' + mode + '-panel';
            chart = '#' + queryType + '-' + mode + '-chart';

            mode = mode + per5min;

            var max = 0
            for (i in dataSorted){
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
                .attr("height", barHeight * dataSorted.length + 1);


            //update bars
            var bars = chart.selectAll("rect").data(dataSorted);



            bars.attr("height", barHeight - 2)
                .transition()
                .duration(1000)
                .attr("width", 0);

            bars.attr("height", barHeight - 2)
                .transition()
                .delay(1000)
                .duration(1000)
                .attr("width", function(d) { return x(d[mode]);});

            bars.enter().append("rect")
                .attr("transform", function(d, i) {return "translate(" + startwidth + "," + (i * barHeight + 1) + ")";})
                .style("align", "center")
                .attr("width", 0)
                .attr("height", barHeight - 1)
                .transition()
                .delay(1000)
                .duration(1000)
                .attr("width", function(d) { return x(d[mode]);});


            bars.exit().remove();

            //update champ icon
            var img = chart.selectAll("image").data(dataSorted);

            img.transition()
                .duration(1000)
                .style('opacity', 0);


            img.attr("id", function(d) {return mode + ',' + dataSorted.indexOf(d);})
                .transition()
                .delay(1000)
                .duration(1000)
                .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d['key'] + ".png";})
                .style('opacity', 1);

            img.enter().append("image")
                .attr("id", function(d) {return mode + ',' + dataSorted.indexOf(d);})
                .style('opacity', 0)
                .attr("transform", function(d, i) {return "translate(" + (startwidth-barHeight) + "," + (i * barHeight + 1) + ")";})
                .attr("xlink:href", function(d){return "http://ddragon.leagueoflegends.com/cdn/5.15.1/img/champion/" + d['key'] + ".png";})
                .attr("width", barHeight - 2)
                .attr("height", barHeight - 2)
                .transition()
                .delay(1000)
                .duration(1000)
                .style('opacity', 1);

            img.exit().remove();

            img.on("mouseover", function(){
                icon = d3.select(this);
                transform = icon.attr("transform").split("(")[1].split(")")[0].split(",");
                mode = icon.attr("id").split(",")[0];
                id = icon.attr("id").split(",")[1];


                hoverData = champsSelectedData.sort(function(a,b){
                if (a[mode] == b[mode]){
                    if (a['name'] < b['name']) return 1;
                    if (a['name'] > b['name']) return -1;
                } else
                    return parseFloat(a[mode])-parseFloat(b[mode]);
                });

                if (descending == true){hoverData = hoverData.reverse()}

                var gradient = d3.select(this.parentNode)
                    .append("linearGradient")
                    .attr("y1", 0)
                    .attr("y2", 0)
                    .attr("x1", 0)
                    .attr("x2", "100%")
                    .attr("id", "gradient")
                    .attr("gradientUnits", "userSpaceOnUse")

                gradient
                    .append("stop")
                    .attr("offset", "0.4")
                    .style("stop-opacity", "1")
                    .attr("stop-color", "brown");

                gradient
                    .append("stop")
                    .attr("offset", "1")
                    .style("stop-opacity", "0")
                    .attr("stop-color", "brown");


                d3.select(this.parentNode).append("rect")
                    .attr("width", 0)
                    .transition()
                    .duration(500)
                    .attr("id", "gradientBar")
                    .attr("width", 500)
                    .attr("height", barHeight - 2)
                    .attr("x", startwidth)
                    .attr("y", transform[1])
                    .style("fill", "url(#gradient)");

                d3.select(this.parentNode).append("text")
                    .attr("fill-opacity", 0)
                    .attr("id", "barName")
                    .attr("x", startwidth + 10)
                    .attr("y", transform[1])
                    .attr("dy", barHeight/2 - 5)
                    .transition('dataName')
                    .duration(250)
                    .delay(250)
                    .attr("fill-opacity", 1)
                    .text(function(){return hoverData[id]['name'];});

                d3.select(this.parentNode).append("text")
                    .attr("fill-opacity", 0)
                    .attr("id", "barStat")
                    .attr("x", startwidth + 10)
                    .attr("y", transform[1])
                    .attr("dy", barHeight/2 + 15)
                    .transition('dataString')
                    .duration(250)
                    .delay(250)
                    .attr("fill-opacity", 1)
                    .text(function(){return formatDataString(mode, hoverData[id][mode]);});

            }).on("mouseout", function(){
                d3.selectAll('#gradientBar')
                    .transition("gradientBarOut")
                    .duration(1500)
                    .style("opacity", 0)
                    .remove();
                d3.selectAll('#barStat')
                    .transition("barStatOut")
                    .duration(750)
                    .style("fill-opacity", 0)
                    .remove();
                d3.selectAll('#barName')
                    .transition("barNameOut")
                    .duration(750)
                    .style("fill-opacity", 0)
                    .remove();
            });

        }
    });
}

function formatDataString(mode, num){
    switch(true){
        case /rate/.test(mode):
            return numeral(num).format('0.000') + '%';
        case /per5min/.test(mode):
            return numeral(num).format('0.000');
        default:
            return numeral(num).format('0.000a');

    }
}