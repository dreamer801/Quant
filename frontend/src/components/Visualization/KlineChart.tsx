'use client';

import ReactECharts from 'echarts-for-react';
import { DailyQuote } from '@/types';

interface KlineChartProps {
  data: DailyQuote[];
  height?: number;
}

export default function KlineChart({ data, height = 400 }: KlineChartProps) {
  const dates = data.map((d) => d.trade_date);
  const ohlc = data.map((d) => [d.open, d.close, d.low, d.high]);
  const volumes = data.map((d) => d.volume);

  // Calculate moving averages
  const calculateMA = (data: (number | null)[], dayCount: number) => {
    const result = [];
    for (let i = 0; i < data.length; i++) {
      if (i < dayCount - 1) {
        result.push('-');
        continue;
      }
      let sum = 0;
      let count = 0;
      for (let j = 0; j < dayCount; j++) {
        const val = data[i - j];
        if (val !== null) {
          sum += val;
          count++;
        }
      }
      result.push(count === dayCount ? (sum / dayCount).toFixed(2) : '-');
    }
    return result;
  };

  const closes = data.map((d) => d.close);
  const ma5 = calculateMA(closes, 5);
  const ma20 = calculateMA(closes, 20);

  const option = {
    animation: false,
    legend: {
      bottom: 10,
      left: 'center',
      data: ['K线', 'MA5', 'MA20'],
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ccc',
      borderWidth: 1,
      formatter: function (params: unknown[]) {
        const p = params as Array<{ seriesName: string; data: unknown; axisValue: string }>;
        const klineData = p.find((item) => item.seriesName === 'K线');
        if (!klineData) return '';
        const d = klineData.data as number[];
        return `
          <div style="font-size: 12px;">
            <div style="font-weight: bold;">${klineData.axisValue}</div>
            <div>开盘: ${d[0]?.toFixed(2) ?? '-'}</div>
            <div>收盘: ${d[1]?.toFixed(2) ?? '-'}</div>
            <div>最低: ${d[2]?.toFixed(2) ?? '-'}</div>
            <div>最高: ${d[3]?.toFixed(2) ?? '-'}</div>
          </div>
        `;
      },
    },
    axisPointer: {
      link: [{ xAxisIndex: 'all' }],
    },
    grid: [
      {
        left: '10%',
        right: '8%',
        height: '50%',
      },
      {
        left: '10%',
        right: '8%',
        top: '65%',
        height: '20%',
      },
    ],
    xAxis: [
      {
        type: 'category',
        data: dates,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
      },
      {
        type: 'category',
        gridIndex: 1,
        data: dates,
        boundaryGap: false,
        axisLine: { onZero: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        min: 'dataMin',
        max: 'dataMax',
      },
    ],
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true,
        },
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
      },
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 50,
        end: 100,
      },
      {
        show: true,
        xAxisIndex: [0, 1],
        type: 'slider',
        top: '90%',
        start: 50,
        end: 100,
      },
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: ohlc,
        itemStyle: {
          color: '#ef4444',
          color0: '#22c55e',
          borderColor: '#ef4444',
          borderColor0: '#22c55e',
        },
      },
      {
        name: 'MA5',
        type: 'line',
        data: ma5,
        smooth: true,
        lineStyle: {
          width: 1,
        },
        symbol: 'none',
      },
      {
        name: 'MA20',
        type: 'line',
        data: ma20,
        smooth: true,
        lineStyle: {
          width: 1,
        },
        symbol: 'none',
      },
      {
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        itemStyle: {
          color: function (params: { dataIndex: number }) {
            const idx = params.dataIndex;
            if (idx === 0) return '#999';
            return ohlc[idx][1] >= ohlc[idx][0] ? '#ef4444' : '#22c55e';
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
