// Initialize Charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Global defaults
    Chart.register(ChartDataLabels);
    Chart.defaults.set('plugins.datalabels', {
        display: false
    });
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = '#64748b';
    Chart.defaults.plugins.tooltip.backgroundColor = '#1e293b';
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;

    // 1. Area Chart - Year-Wise Book Analysis
    const ctxArea = document.getElementById('areaChart').getContext('2d');
    
    // Create gradient
    let gradientArea = ctxArea.createLinearGradient(0, 0, 0, 300);
    gradientArea.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
    gradientArea.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    new Chart(ctxArea, {
        type: 'line',
        data: {
            labels: ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
            datasets: [{
                label: 'Books',
                data: [20, 42, 85, 62, 52, 92, 90, 74, 140, 162, 50, 180, 110, 140, 62],
                borderColor: '#3b82f6',
                backgroundColor: gradientArea,
                borderWidth: 2,
                pointBackgroundColor: ['#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#a855f7','#ffffff','#ffffff','#ffffff'],
                pointBorderColor: ['#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#ef4444','#3b82f6','#3b82f6','#3b82f6'],
                pointBorderWidth: [2,2,2,2,2,2,2,2,2,2,2,4,2,2,2],
                pointRadius: [4,4,4,4,4,4,4,4,4,4,4,8,4,4,4],
                pointHoverRadius: 6,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f1f5f9', drawBorder: false },
                    border: { display: false }
                },
                x: {
                    grid: { display: false, drawBorder: false },
                    border: { display: false }
                }
            },
            // Custom plugin to draw the '180' peak label if needed, 
            // but standard tooltips suffice for most interactivity.
        },
        plugins: [{
            id: 'peak_label',
            afterDatasetsDraw: (chart) => {
                const ctx = chart.ctx;
                const meta = chart.getDatasetMeta(0);
                const pt = meta.data[11]; // The '180' point
                
                ctx.save();
                ctx.fillStyle = '#3b82f6';
                ctx.beginPath();
                ctx.roundRect(pt.x - 15, pt.y - 45, 30, 20, 4);
                ctx.fill();
                
                // Little triangle pointing down
                ctx.beginPath();
                ctx.moveTo(pt.x - 5, pt.y - 25);
                ctx.lineTo(pt.x + 5, pt.y - 25);
                ctx.lineTo(pt.x, pt.y - 18);
                ctx.fill();
                
                ctx.fillStyle = 'white';
                ctx.font = '12px Inter';
                ctx.textAlign = 'center';
                ctx.fillText('180', pt.x, pt.y - 31);
                
                // Connecting line
                ctx.beginPath();
                ctx.strokeStyle = '#94a3b8';
                ctx.setLineDash([2, 2]);
                ctx.moveTo(pt.x, pt.y - 18);
                ctx.lineTo(pt.x, pt.y - 10);
                ctx.stroke();
                
                ctx.restore();
            }
        }]
    });

    // 2. Donut Chart - Author Analysis
    const ctxDonut = document.getElementById('donutChart').getContext('2d');
    new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
            labels: ['J.K. Rowling', 'Stephen King', 'Agatha Christie', 'Dan Brown', 'Neil Gaiman'],
            datasets: [{
                data: [30, 25, 20, 15, 10],
                backgroundColor: [
                    '#a855f7', // purple
                    '#3b82f6', // blue
                    '#22c55e', // green
                    '#f97316', // orange
                    '#eab308'  // yellow
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false // We could use a custom HTML legend to match image exactly, but leaving simple for now
                }
            }
        },
        plugins: [{
            id: 'custom_labels',
            afterDraw: (chart) => {
                // Drawing custom labels outside the donut is complex in Chart.js without plugins like chartjs-plugin-datalabels
                // We'll rely on tooltips for the exact data for a cleaner look
            }
        }]
    });

    // 3. Vertical Bar Chart - Genre Distribution
    const ctxBar = document.getElementById('barChart').getContext('2d');
    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: ['Fiction', 'Mystery', 'Romance', 'Sci-Fi', 'Non-Fiction'],
            datasets: [{
                data: [70, 78, 55, 98, 30],
                backgroundColor: '#3b82f6',
                borderRadius: 4,
                barThickness: 24
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                datalabels: {
                    display: true,
                    anchor: 'end',
                    align: 'top',
                    color: '#1e293b',
                    font: { weight: '600' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#f1f5f9', borderDash: [4, 4], drawBorder: false },
                    border: { display: false }
                },
                x: {
                    grid: { display: false, drawBorder: false },
                    border: { display: false }
                }
            }
        }
    });

    // 4. Horizontal Bar Chart - Rating Distribution
    const ctxHBar = document.getElementById('horizontalBarChart').getContext('2d');
    new Chart(ctxHBar, {
        type: 'bar',
        data: {
            labels: ['Rating 1-2 Stars', 'Rating 2-3 Stars', 'Rating 3-4 Stars', 'Rating 4-5 Stars'],
            datasets: [{
                data: [5, 15, 40, 40],
                backgroundColor: '#3b82f6',
                borderRadius: 4,
                barThickness: 16
            }]
        },
        options: {
            indexAxis: 'y', // Makes it horizontal
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                datalabels: {
                    display: true,
                    anchor: 'end',
                    align: 'right',
                    color: '#1e293b',
                    font: { weight: '600' },
                    formatter: (value) => value + '%'
                }
            },
            scales: {
                x: {
                    display: false,
                    max: 100
                },
                y: {
                    grid: { display: false, drawBorder: false },
                    border: { display: false }
                }
            }
        }
    });

    // 5. Populate Table Data
    const tableData = [
        { title: "The Silent Patient", genre: "Mystery", author: "Alex Michaelides", rating: "4.90", reviews: "125,432", year: "2019" },
        { title: "Project Hail Mary", genre: "Sci-Fi", author: "Andy Weir", rating: "4.85", reviews: "105,678", year: "2021" },
        { title: "Educated", genre: "Non-Fiction", author: "Tara Westover", rating: "4.80", reviews: "98,765", year: "2018" },
        { title: "Dune", genre: "Sci-Fi", author: "Frank Herbert", rating: "4.75", reviews: "85,432", year: "1965" },
        { title: "Lessons in Chemistry", genre: "Fiction", author: "Bonnie Garmus", rating: "4.70", reviews: "72,100", year: "2022" }
    ];

    const tbody = document.querySelector('#insightsTable tbody');
    tableData.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-weight: 500;">${row.title}</td>
            <td>${row.genre}</td>
            <td>${row.author}</td>
            <td>${row.rating}</td>
            <td>${row.reviews}</td>
            <td>${row.year}</td>
        `;
        tbody.appendChild(tr);
    });
});
