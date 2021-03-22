$(document).ready(function (e) {

    $.ajax({
        type: "POST",
        url: "/",
        dataType: "json",
        success: function (result) {
            console.log(result)
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: result['series'],
                    datasets: [{
                        label: '# of Success',
                        data: result['success'],
                        backgroundColor: [
                            'rgba(52, 255, 15, 0.7)',
                            'rgba(52, 255, 15, 0.7)',
                            'rgba(52, 255, 15, 0.7)',
                        ],
                        borderColor: [
                            'rgba(255, 19, 67, 0.7)',
                            'rgba(255, 19, 67, 0.7)',
                            'rgba(255, 19, 67, 0.7)',
                        ],
                        borderWidth: 1
                    },
                    {
                        label: '# of Error',
                        data: result['error'],
                        backgroundColor: [
                            'rgba(255, 19, 67, 0.7)',
                            'rgba(255, 19, 67, 0.7)',
                            'rgba(255, 19, 67, 0.7)',
                        ],
                        borderColor: [
                            'rgba(255, 19, 67, 0.7)',
                            'rgba(255, 19, 67, 0.7)',
                            'rgba(255, 19, 67, 0.7)',
                        ],
                        borderWidth: 1
                    }
                ]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        },
        error: function (err) {
            console.log(err)
        }
    })
});