import React, { useEffect } from "react";
import * as d3 from "d3";

const LineChart = ({ logs }) => {
  useEffect(() => {
    const parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%SZ");

    const data = logs.map((log) => ({
      time: parseTime(log.timestamp),
      severity: log.severity,
    }));

    const aggregatedData = Array.from(
      d3.rollup(
        data,
        (v) => v.length,
        (d) => d3.timeMinute(d.time)
      ),
      ([time, count]) => ({ time, count })
    );

    if (aggregatedData.length === 0) {
      console.warn("No data available for rendering.");
      return;
    }

    const width = 600;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };

    const svg = d3
      .select("#lineChart")
      .attr("width", width)
      .attr("height", height)
      .style("background-color", "var(--bg-accent)");

    const x = d3
      .scaleTime()
      .domain(d3.extent(aggregatedData, (d) => d.time))
      .range([margin.left, width - margin.right]);

    const y = d3
      .scaleLinear()
      .domain([0, d3.max(aggregatedData, (d) => d.count)])
      .nice()
      .range([height - margin.bottom, margin.top]);

    svg.selectAll("*").remove();

    const line = d3
      .line()
      .x((d) => x(d.time))
      .y((d) => y(d.count));

    svg
      .append("path")
      .data([aggregatedData])
      .attr("fill", "none")
      .attr("stroke", "#53FFD6")
      .attr("stroke-width", 1.5)
      .attr("d", line);

    svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%H:%M")).ticks(width / 80))
      .attr("stroke", "white");

    svg
      .append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .attr("stroke", "white");
  }, [logs]);

  return <svg id="lineChart"></svg>;
};

export default LineChart;
