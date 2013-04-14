var Availability = function() {
	"use strict";
	var self = this;

    this.cellSize = 4;

    this.day = d3.time.format("%w");
    this.percent = d3.format(".2%");
    this.week = d3.time.format("%U");
    this.format_day = d3.time.format("%Y-%m-%d");

    this.parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

    this.piece_length = 54;
    this.piece_rows = 2;

    this.y_start = 2010;
    this.y_end = 2014;

//    this.date_min;
//    this.date_max;

    this.width = this.cellSize * this.piece_length;
    this.height = this.cellSize * this.piece_rows;

    var color = d3.scale.quantize()
        .domain([.01, 1])
        .range(d3.range(0,11).map(function(d) { return "q" + d + "-11"; }));

    this.x = d3.scale.linear()
             .domain([0, (this.y_end - this.y_start)])
             .range([0, this.width - this.cellSize * this.piece_length]);


    // Default settings
	this.options = {
		// DOM ID of the container to append the graph to
		id : "availability",
		// Size of each cell, in pixel
		cellsize : 3,
		// URL, where to fetch the original datas
		data_url : "",

        show_headers: false,

        date_min: new Date(2011,1,1),
        date_max: Date.now()
};

	var _init = function() {

        self.options.date_min = self.parseDate(self.options.date_min);
        if (self.options.date_max == "")
            self.options.date_max = Date.now();
        else
            self.options.date_max = self.parseDate(self.options.date_max);


        var svg = d3.select("#" + self.options.id).selectAll("svg")
            .data(d3.range(self.y_start, self.y_end))
            .enter().append("svg")
            .attr("width", self.width)
            .attr("height", self.height)
            .attr("class", "RdYlGn")
            .append("g")
//            .attr("transform", function(d, i) {
//                return "translate(" + 1.8* self.x(i) + ", " + (self.height - self.cellSize * 1) + ")";
//            })
            ;

//        if (self.options.show_headers){
//            svg.append("text")
//                .attr("transform", "translate("+  ((self.cellSize * self.piece_length) / 2) + "," + self.cellSize * -1 + ")")
//                .style("text-anchor", "middle")
//                .text(function(d) { return d; });
//        }
        var flag = true;
        var rect = svg.selectAll(".day")
            .data(function(d) { return d3.time.weeks(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
            .enter().append("rect")
            .attr("class", function(d) {
                if ( d > self.options.date_min
                  && d < self.options.date_max )
                    return "active";
                else
                    return "day";
                })
            .attr("width", self.cellSize)
            .attr("height", self.cellSize)
                .attr("x", function(d) { return self.week(d) * self.cellSize; })
                .attr("y", function(d) { return 1; })
            .datum(self.format_day);

        rect.append("title")
            .text(function(d) { return d; });


        d3.json(self.options.data_url,
            function(error, json) {
                var g = JSON.parse(json['gaps']);
                var data = {};
                var day_format = d3.time.format("%Y-%m-%d");
                for (var d in g){
                    var _day = day_format(new Date(d*1000));
                    var _value = g[d];
                    data[_day] = _value;
                }

                rect.filter(function(d) { return d in data; })
                    .attr("class", function(d) { return "day " + color(data[d]); })
                    .select("title")
                    .text(function(d) { return d + ": " + self.percent(data[d]/100); });
            });

		return true;
	};


	this.init = function(settings) {

		// Merge settings with default
		if ( settings !== null && settings !== undefined && settings !== "undefined" ){
				for ( var opt in self.options ) {
					if ( settings[ opt ] !== null &&
						settings[ opt ] !== undefined &&
						settings[ opt ] !== "undefined" ){
							self.options[ opt ] = settings[ opt ];
				}
			}
		}
		return _init();
	};
};


Availability.prototype = {


};


/**
 * AMD Loader
 */
if (typeof define === "function" && define.amd) {
	define(["d3"], function(d3) {
		return Availability;
	});
}