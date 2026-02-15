'use client';

import ReactECharts from 'echarts-for-react';

interface MonthlyReturnHeatmapProps {
  data: Record<string, Record<string, number>>;
  height?: number;
}

export default function MonthlyReturnHeatmap({ data, height = 300 }: MonthlyReturnHeatmapProps) {
  const years = Object.keys(data).sort();
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];

  const heatmapData: Array<[number, number, number]> = [];
  years.forEach((year, yearIndex) => {
    months.forEach((_, monthIndex) => {
      const monthKey = String(monthIndex + 1).padStart(2, '0');
      const value = data[year]?.[monthKey] ?? 0;
      heatmapData.push([monthIndex, yearIndex, value]);
    });
  });

  const option = {
    tooltip: {
      position: 'top',
      formatter: function (params: { data: [number, number, number] }) {
        const [monthIdx, yearIdx, value] = params.data;
        return `${years[yearIdx]}年${months[monthIdx]}: ${(value * 100).toFixed(2)}%`;
      },
    },
    grid: {
      left: '10%',
      right: '10%',
      top: '10%',
      bottom: '15%',
    },
    xAxis: {
      type: 'category',
      data: months,
      splitArea: {
        show: true,
      },
      axisLabel: {
        fontSize: 10,
      },
    },
    yAxis: {
      type: 'category',
      data: years,
      splitArea: {
        show: true,
      },
    },
    visualMap: {
      min: -0.2,
      max: 0.2,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#ef4444', '#fee2e2', '#ffffff', '#dcfce7', '#22c55e'],
      },
      formatter: function (value: number) {
        return (value * 100).toFixed(0) + '%';
      },
    },
    series: [
      {
        name: '月度收益',
        type: 'heatmap',
        data: heatmapData,
        label: {
          show: true,
          fontSize: 10,
          formatter: function (params: { data: [number, number, number] }) {
            const value = params.data[2];
            return (value * 100).toFixed(1) + '%';
          },
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };

  return (
    <div style={{ height }}>
      <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}
