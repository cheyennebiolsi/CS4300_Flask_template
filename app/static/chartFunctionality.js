function toggleLegendQuery(source, chartName) {
    chartName.data.datasets[0].hidden = !(source.checked);
    rescaleSuggestionChart(chartName);
    chartName.update();
};

function toggleLegendSuggestion(source, chartName) {
    chartName.data.datasets[1].hidden = !(source.checked);
    rescaleSuggestionChart(chartName);
    chartName.update();
};
function rescaleSuggestionChart(chartName) {
    if ((chartName.data.datasets[0].hidden) && (chartName.data.datasets[1].hidden)) {
        return;
    } else if (!(chartName.data.datasets[0].hidden) && (chartName.data.datasets[1].hidden)) {
        var maxVal = Math.max.apply(Math, chartName.data.datasets[0].data);
    } else if ((chartName.data.datasets[0].hidden) && (!(chartName.data.datasets[1].hidden))) {
        var maxVal = Math.max.apply(Math, chartName.data.datasets[1].data);
    } else {
        var maxVal = Math.max.apply(Math, chartName.data.datasets[0].data.concat(chartName.data.datasets[1].data));
    }
    maxVal = maxVal + 0.1;
    chartName.options.scale.ticks.max = Math.min(1.0, (Math.floor(maxVal * 10))/10);
};
