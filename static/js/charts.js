document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('viciousCycleChart').getContext('2d');

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'Inattività',
                'Declino Cognitivo',
                'Isolamento Sociale',
                'Problemi di Salute',
                'Costi Sociali',
                'Qualità della Vita'
            ],
            datasets: [{
                label: 'Impatto del Ciclo Vizioso',
                data: [85, 75, 80, 70, 65, 60],
                fill: true,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgb(59, 130, 246)',
                pointBackgroundColor: 'rgb(59, 130, 246)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(59, 130, 246)'
            }]
        },
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
});