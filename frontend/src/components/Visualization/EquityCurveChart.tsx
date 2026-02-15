'use client';

import ReactECharts from 'echarts-for-react';
import { NetValuePoint } from '@/types';

interface EquityCurveChartProps {
  strategyData: NetValuePoint[];
  benchmarkData?: NetValuePoint[];
  height?: number;
}

export default function EquityCurveChart({
  strategyData,
  benchmarkData,
  height = 400,
}: EquityCurveChartProps) {
  const dates = strategyData.map((d) => d.date);
  const strategyValues = strategyData.map((d) => d.net_value);
  const benchmarkValues = benchmarkData?.map((d) => d.net_value) || [];

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ccc',
      borderWidth: 1,
      formatter: function (params: unknown[]) {
        const p = params as Array<{ seriesName: string; data: number; axisValue: string }>;
        let html = `<div style="font-size: 12px;"><div style="font-weight: bold;">${p[0]?.axisValue}</div>`;
        p.forEach((item) => {
          html += `<div>${item.seriesName}: ${(item.data * 100).toFixed(2)}%</div>`;
        });
        html += '</div>';
        return html;
      },
    },
    legend: {
      data: benchmarkValues.length > 0 ? ['策略净值', '基准净值'] : ['策略净值'],
      bottom: 10,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dates,
      boundaryGap: false,
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: function (value: number) {
          return (value * 100).toFixed(0) + '%';
        },
      },
    },
    series: [
      {
        name: '策略净值',
        type: 'line',
        data: strategyValues,
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#3b82f6',
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.05)' },
            ],
          },
        },
        symbol: 'none',
      },
      ...(benchmarkValues.length > 0
        ? [
            {
              name: '基准净值',
              type: 'line' as const,
              data: benchmarkValues,
              smooth: true,
              lineStyle: {
                width: 2,
                color: '#94a3b8',
                type: 'dashed' as const,
              },
              symbol: 'none',
            },
          ]
        : []),
    ],
  };

  return (
    <div style={{ height }}>
      <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}
