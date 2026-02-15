'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Layout } from '@/components/common';
import { EquityCurveChart, TradeTable } from '@/components/Visualization';
import { BacktestResult } from '@/types';
import { backtestService } from '@/services';

export default function BacktestResultPage() {
  const params = useParams();
  const [result, setResult] = useState<BacktestResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResult();
  }, [params.id]);

  const loadResult = async () => {
    try {
      const data = await backtestService.getResult(params.id as string);
      setResult(data);
    } catch (error) {
      console.error('Failed to load result:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="max-w-6xl mx-auto p-6">
          <p className="text-center text-gray-500">加载中...</p>
        </div>
      </Layout>
    );
  }

  if (!result) {
    return (
      <Layout>
        <div className="max-w-6xl mx-auto p-6">
          <p className="text-center text-gray-500">未找到回测结果</p>
        </div>
      </Layout>
    );
  }

  const metrics = [
    { label: '总收益率', value: `${((result.total_return || 0) * 100).toFixed(2)}%` },
    { label: '年化收益', value: `${((result.annual_return || 0) * 100).toFixed(2)}%` },
    { label: '最大回撤', value: `${((result.max_drawdown || 0) * 100).toFixed(2)}%` },
    { label: '夏普比率', value: (result.sharpe_ratio || 0).toFixed(2) },
    { label: '胜率', value: `${((result.win_rate || 0) * 100).toFixed(1)}%` },
    { label: '盈亏比', value: (result.profit_loss_ratio || 0).toFixed(2) },
  ];

  return (
    <Layout>
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">回测结果</h1>

        {/* Metrics Cards */}
        <div className="grid grid-cols-3 md:grid-cols-6 gap-4 mb-6">
          {metrics.map((metric) => (
            <div key={metric.label} className="bg-white p-4 rounded-lg border border-gray-100">
              <p className="text-sm text-gray-500">{metric.label}</p>
              <p className="text-xl font-semibold text-gray-900 mt-1">{metric.value}</p>
            </div>
          ))}
        </div>

        {/* Info */}
        <div className="bg-white p-4 rounded-lg border border-gray-100 mb-6">
          <div className="flex gap-8 text-sm">
            <span>
              <span className="text-gray-500">策略 ID:</span>{' '}
              <span className="font-medium">{result.strategy_id}</span>
            </span>
            <span>
              <span className="text-gray-500">回测区间:</span>{' '}
              <span className="font-medium">
                {result.start_date} ~ {result.end_date}
              </span>
            </span>
            <span>
              <span className="text-gray-500">初始资金:</span>{' '}
              <span className="font-medium">
                {(result.initial_capital || 0).toLocaleString()} 元
              </span>
            </span>
          </div>
        </div>

        {/* Equity Curve */}
        <div className="bg-white p-6 rounded-lg border border-gray-100 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">净值曲线</h2>
          <EquityCurveChart
            strategyData={result.net_value_series || []}
            height={400}
          />
        </div>

        {/* Trades Table */}
        <div className="bg-white p-6 rounded-lg border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">交易明细</h2>
          <TradeTable trades={result.trades || []} />
        </div>
      </div>
    </Layout>
  );
}
