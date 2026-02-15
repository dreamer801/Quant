'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Layout, Button } from '@/components/common';
import { Strategy } from '@/types';
import { strategyService } from '@/services';

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStrategies();
  }, []);

  const loadStrategies = async () => {
    try {
      const data = await strategyService.getStrategies();
      setStrategies(data);
    } catch (error) {
      console.error('Failed to load strategies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除这个策略吗？')) return;

    try {
      await strategyService.deleteStrategy(id);
      setStrategies(strategies.filter((s) => s.id !== id));
    } catch (error) {
      console.error('Failed to delete strategy:', error);
      alert('删除失败，请重试');
    }
  };

  return (
    <Layout>
      <div className="max-w-5xl mx-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900">策略管理</h1>
          <Link href="/strategy">
            <Button>新建策略</Button>
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-500">加载中...</p>
          </div>
        ) : strategies.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg border border-gray-100">
            <p className="text-gray-500 mb-4">暂无策略</p>
            <Link href="/strategy">
              <Button>创建第一个策略</Button>
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">
            {strategies.map((strategy) => (
              <div
                key={strategy.id}
                className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {strategy.name}
                    </h3>
                    {strategy.description && (
                      <p className="text-sm text-gray-600 mt-1">{strategy.description}</p>
                    )}
                    <p className="text-xs text-gray-400 mt-2">
                      创建于 {new Date(strategy.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <Link href={`/backtest?strategy_id=${strategy.id}`}>
                      <Button size="sm">回测</Button>
                    </Link>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(strategy.id)}
                    >
                      删除
                    </Button>
                  </div>
                </div>

                <div className="mt-4 flex gap-4 text-sm text-gray-600">
                  <span>筛选条件: {strategy.config.filter_conditions.length} 个</span>
                  <span>排名规则: {strategy.config.ranking_rules.length} 个</span>
                  <span>持仓数量: {strategy.config.top_n}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
