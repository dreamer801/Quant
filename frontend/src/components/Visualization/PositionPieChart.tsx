'use client';

import ReactECharts from 'echarts-for-react';

interface PositionPieChartProps {
  data: Array<{
    name: string;
    value: number;
  }>;
  title?: string;
  height?: number;
}

export default function PositionPieChart({ data, title, height = 300 }: PositionPieChartProps) {
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: function (params: { name: string; value: number; percent: number }) {
        return `${params.name}: ${params.value.toFixed(2)} (${params.percent.toFixed(1)}%)`;
      },
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'middle',
    },
    title: title
      ? {
          text: title,
          left: 'center',
        }
      : undefined,
    series: [
      {
        name: '持仓分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data: data,
      },
    ],
  };

  return (
    <div style={{ height }}>
      <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}
