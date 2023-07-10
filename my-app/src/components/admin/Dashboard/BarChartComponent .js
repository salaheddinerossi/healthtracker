import React from 'react';
import { Bar } from 'react-chartjs-2';

const BarChartComponent = ({ data, title, labels, colors,h1 }) => {
  const chartData = {
    labels,
    datasets: [
      {
        label: title,
        data,
        backgroundColor: colors,
        borderColor: colors.map(color => color.replace('0.2', '1')),
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className='bar_chart'>
        <h3 className='title_statistics'>{h1}</h3>
      <Bar
        data={chartData}
        options={{
          title: {
            display: true,
            text: title,
            fontSize: 20,
          },
          legend: {
            display: true,
            position: 'right',
          },
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                },
              },
            ],
          },
        }}
      />
    </div>
  );
};

export default BarChartComponent;
