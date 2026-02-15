'use client';

import { TradingRule, RebalanceFrequency } from '@/types';
import { Select } from '@/components/common';
import Input from '@/components/common/Input';

interface TradingRuleBuilderProps {
  rule: TradingRule;
  onChange: (rule: TradingRule) => void;
}

const frequencyOptions = [
  { value: 'daily', label: '每日' },
  { value: 'weekly', label: '每周' },
  { value: 'monthly', label: '每月' },
];

export default function TradingRuleBuilder({ rule, onChange }: TradingRuleBuilderProps) {
  const updateRule = (updates: Partial<TradingRule>) => {
    onChange({ ...rule, ...updates });
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-medium text-gray-900">交易规则</h3>

      <div className="bg-gray-50 p-4 rounded-lg">
        <div className="grid grid-cols-2 gap-4">
          {/* Rebalance frequency */}
          <Select
            label="调仓频率"
            options={frequencyOptions}
            value={rule.rebalance_frequency}
            onChange={(e) =>
              updateRule({ rebalance_frequency: e.target.value as RebalanceFrequency })
            }
          />

          {/* Max position percentage */}
          <Input
            type="number"
            label="单只股票最大持仓比例"
            min={0.01}
            max={1}
            step={0.01}
            value={rule.max_position_pct}
            onChange={(e) => updateRule({ max_position_pct: parseFloat(e.target.value) })}
          />

          {/* Cash reserve percentage */}
          <Input
            type="number"
            label="现金保留比例"
            min={0}
            max={1}
            step={0.01}
            value={rule.cash_reserve_pct}
            onChange={(e) => updateRule({ cash_reserve_pct: parseFloat(e.target.value) })}
          />

          {/* Commission rate */}
          <Input
            type="number"
            label="手续费率"
            min={0}
            max={0.01}
            step={0.0001}
            value={rule.commission_rate}
            onChange={(e) => updateRule({ commission_rate: parseFloat(e.target.value) })}
          />
        </div>
      </div>
    </div>
  );
}
