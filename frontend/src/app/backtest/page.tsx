'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Layout, Button, Select } from '@/components/common';
import Input from '@/components/common/Input';
import { backtestService } from '@/services';

export default function BacktestPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const preselectedStrategyId = searchParams.get('strategy_id');

  const [strategyId, setStrategyId] = useState(preselectedStrategyId || '');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [initialCapital, setInitialCapital] = useState('1000000');
  const [benchmark, setBenchmark] = useState('000300.SH');
  const [running, setRunning] = useState(false);

  const handleRunBacktest = async () => {
    if (!strategyId || !startDate || !endDate) {
      alert('请填写所有必填项');
      return;
    }

    setRunning(true);
    try {
      const result = await backtestService.runBacktest({
        strategy_id: strategyId,
        start_date: startDate,
        end_date: endDate,
        initial_capital: parseFloat(initialCapital),
        benchmark,
      });
      router.push(`/backtest/results/${result.id}`);
    } catch (error) {
      console.error('Backtest failed:', error);
      alert('回测失败，请检查参数后重试');
    } finally {
      setRunning(false);
    }
  };

  const benchmarkOptions = [
    { value: '000300.SH', label: '沪深300' },
    { value: '000016.SH', label: '上证50' },
    { value: '000905.SH', label: '中证500' },
    { value: '000001.SH', label: '上证指数' },
  ];

  return (
    <Layout>
      <div className="max-w-3xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">回测配置</h1>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 space-y-6">
          {/* Strategy ID */}
          <Input
            label="策略 ID"
            value={strategyId}
            onChange={(e) => setStrategyId(e.target.value)}
            placeholder="输入策略 ID"
          />

          {/* Date Range */}
          <div className="grid grid-cols-2 gap-4">
            <Input
              type="date"
              label="开始日期"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
            <Input
              type="date"
              label="结束日期"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>

          {/* Initial Capital */}
          <Input
            type="number"
            label="初始资金"
            value={initialCapital}
            onChange={(e) => setInitialCapital(e.target.value)}
          />

          {/* Benchmark */}
          <Select
            label="基准指数"
            options={benchmarkOptions}
            value={benchmark}
            onChange={(e) => setBenchmark(e.target.value)}
          />

          {/* Run Button */}
          <div className="pt-4">
            <Button onClick={handleRunBacktest} disabled={running} size="lg">
              {running ? '回测运行中...' : '开始回测'}
            </Button>
          </div>
        </div>
      </div>
    </Layout>
  );
}
