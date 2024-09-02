//document.getElementById('generateGraphBtn').addEventListener('click', function () {
//    const crypto = document.getElementById('cryptoSelect').value.toLowerCase();
//    const algorithm = document.getElementById('algorithmSelect').value;
//    const startTime = document.getElementById('startTimeInput').value;
//    const futureTime = document.getElementById('futureTimeInput').value;
//
//    // Fetch the data from the backend
//    fetch(`/get_prediction`, {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json',
//        },
//        body: JSON.stringify({
//            crypto: crypto,
//            algorithm: algorithm,
//            start_time: startTime,
//            future_time: futureTime
//        }),
//    })
//    .then(response => response.json())
//    .then(data => {
//        const trace1 = {
//            x: data.dates,
//            y: data.historical,
//            mode: 'lines',
//            name: 'Historical Data'
//        };
//
//        const trace2 = {
//            x: data.future_dates,
//            y: data.predictions,
//            mode: 'lines',
//            name: 'Predicted Data'
//        };
//
//        const trace3 = {
//            x: data.future_dates,
//            y: data.upper_bound,
//            mode: 'lines',
//            name: 'Upper Bound',
//            line: { dash: 'dot', color: 'rgba(0, 0, 255, 0.5)' }
//        };
//
//        const trace4 = {
//            x: data.future_dates,
//            y: data.lower_bound,
//            mode: 'lines',
//            name: 'Lower Bound',
//            line: { dash: 'dot', color: 'rgba(255, 0, 0, 0.5)' }
//        };
//
//        const layout = {
//            title: `${crypto.charAt(0).toUpperCase() + crypto.slice(1)} Price Prediction`,
//            xaxis: {
//                title: 'Date'
//            },
//            yaxis: {
//                title: 'Price (USD)'
//            }
//        };
//
//        Plotly.newPlot('graphContainer', [trace1, trace2, trace3, trace4], layout);
//    })
//    .catch(error => console.error('Error fetching data:', error));
//});


document.getElementById('generateGraphBtn').addEventListener('click', function () {
    const crypto = document.getElementById('cryptoSelect').value.toLowerCase();
    const algorithm = document.getElementById('algorithmSelect').value;
    const startTime = document.getElementById('startTimeInput').value;
    const futureTime = document.getElementById('futureTimeInput').value;

    // Fetch the data from the backend
    fetch(`/get_prediction`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            crypto: crypto,
            algorithm: algorithm,
            start_time: startTime,
            future_time: futureTime
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Historical data trace
        const trace1 = {
            x: data.historical_dates,
            y: data.historical,
            mode: 'lines',
            name: 'Historical Data'
        };

        // Predicted data trace
        const trace2 = {
            x: data.future_dates,
            y: data.predictions,
            mode: 'lines',
            name: 'Predicted Data'
        };

        // Upper bound of predictions trace
        const trace3 = {
            x: data.future_dates,
            y: data.upper_bound,
            mode: 'lines',
            name: 'Upper Bound',
            line: { dash: 'dot', color: 'rgba(0, 0, 255, 0.5)' }
        };

        // Lower bound of predictions trace
        const trace4 = {
            x: data.future_dates,
            y: data.lower_bound,
            mode: 'lines',
            name: 'Lower Bound',
            line: { dash: 'dot', color: 'rgba(255, 0, 0, 0.5)' }
        };

        const layout = {
            title: `${crypto.charAt(0).toUpperCase() + crypto.slice(1)} Price Prediction`,
            xaxis: {
                title: 'Date'
            },
            yaxis: {
                title: 'Price (USD)'
            }
        };

        // Plot the data using Plotly
        Plotly.newPlot('graphContainer', [trace1, trace2, trace3, trace4], layout);
    })
    .catch(error => console.error('Error fetching data:', error));
});
