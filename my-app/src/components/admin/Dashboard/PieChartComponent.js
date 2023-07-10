import React from 'react';
import { Pie } from 'react-chartjs-2';

const PieChartComponent = ({ dataSize,storageSize, title, labels, colors, h1 }) => {


  // Construct chart data
  const chartData = {
    labels,
    datasets: [
      {
        label: title,
        data: [storageSize, dataSize], // Pass the values to your data array
        backgroundColor: colors,
        borderColor: colors.map(color => color.replace('0.2', '1')),
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className='pie_chart'>
      <h3 className='title_statistics'>{h1}</h3>
      <Pie
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
        }}
      />
    </div>
  );
};

export default PieChartComponent;
