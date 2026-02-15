'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Layout, Button } from '@/components/common';
import { StrategyBuilder } from '@/components/StrategyBuilder';
import { StrategyConfig, FactorDefinition } from '@/types';
import { strategyService } from '@/services';

const defaultConfig: StrategyConfig = {
  universe: ['all'],
  filter_conditions: [],
  ranking_rules: [],
  trading_rule: {
    rebalance_frequency: 'weekly',
    max_position_pct: 0.1,
    cash_reserve_pct: 0.05,
    commission_rate: 0.0003,
    slippage: 0,
  },
  top_n: 10,
};

// Mock factors - in production, this would be fetched from API
const mockFactors: FactorDefinition[] = [
  { name: 'pe_ratio', display_name: '市盈率', category: 'valuation', description: '股价/每股收益', unit: '倍', higher_is_better: false },
  { name: 'pb_ratio', display_name: '市净率', category: 'valuation', description: '股价/每股净资产', unit: '倍', higher_is_better: false },
  { name: 'roe', display_name: 'ROE', category: 'quality', description: '净资产收益率', unit: '%', higher_is_better: true },
  { name: 'total_mv', display_name: '总市值', category: 'size', description: '总股本 x 收盘价', unit: '亿元', higher_is_better: false },
  { name: 'turnover_rate', display_name: '换手率', category: 'technical', description: '成交量/流通股本', unit: '%', higher_is_better: false },
];

export default function StrategyPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [config, setConfig] = useState<StrategyConfig>(defaultConfig);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    if (!name.trim()) {
      alert('请输入策略名称');
      return;
    }

    setSaving(true);
    try {
      await strategyService.createStrategy({
        name,
        description,
        config,
      });
      router.push('/strategies');
    } catch (error) {
      console.error('Failed to save strategy:', error);
      alert('保存失败，请重试');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-5xl mx-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900">构建策略</h1>
          <div className="flex gap-3">
            <Button variant="secondary" onClick={() => router.back()}>
              取消
            </Button>
            <Button onClick={handleSave} disabled={saving}>
              {saving ? '保存中...' : '保存策略'}
            </Button>
          </div>
        </div>

        <StrategyBuilder
          name={name}
          description={description}
          config={config}
          factors={mockFactors}
          onNameChange={setName}
          onDescriptionChange={setDescription}
          onConfigChange={setConfig}
        />
      </div>
    </Layout>
  );
}
