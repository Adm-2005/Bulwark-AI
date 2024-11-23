import React, { useEffect } from "react";
import * as d3 from "d3";

const BarChart = ({ logs }) => {
  useEffect(() => {
    const severityCounts = d3.rollup(
      logs,
      (v) => v.length,
      (d) => d.severity
    );

    const data = Array.from(severityCounts, ([severity, count]) => ({
      severity,
      count,
    }));

    const width = 600;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };

    const svg = d3
      .select("#barChart")
      .attr("width", width)
      .attr("height", height);

    const x = d3
      .scaleBand()
      .domain(data.map((d) => d.severity))
      .range([margin.left, width - margin.right])
      .padding(0.2);

    const y = d3.scaleLinear().domain([0, d3.max(data, (d) => d.count)]).nice().range([height - margin.bottom, margin.top]);

    svg.selectAll("rect")
      .data(data)
      .join("rect")
      .attr("x", (d) => x(d.severity))
      .attr("y", (d) => y(d.count))
      .attr("width", x.bandwidth())
      .attr("height", (d) => height - margin.bottom - y(d.count))
      .attr("fill", "#53FFD6"); 

    svg.selectAll("text")
      .data(data)
      .join("text")
      .attr("x", (d) => x(d.severity) + x.bandwidth() / 2)
      .attr("y", (d) => y(d.count) - 5)
      .attr("text-anchor", "middle")
      .text((d) => d.count);

    svg.append("g").call(d3.axisBottom(x)).attr("transform", `translate(0,${height - margin.bottom})`).attr("stroke", "white");
    svg.append("g").call(d3.axisLeft(y)).attr("transform", `translate(${margin.left},0)`).attr("stroke", "white");
  }, [logs]);

  return <svg id="barChart"></svg>;
};

export default BarChart;
