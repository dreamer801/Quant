'use client';

import { RankingRule, FactorDefinition } from '@/types';
import { Button, Select } from '@/components/common';
import Input from '@/components/common/Input';

interface RankingRuleBuilderProps {
  rules: RankingRule[];
  onChange: (rules: RankingRule[]) => void;
  factors: FactorDefinition[];
}

export default function RankingRuleBuilder({
  rules,
  onChange,
  factors,
}: RankingRuleBuilderProps) {
  const addRule = () => {
    const newRule: RankingRule = {
      factor_name: factors[0]?.name || '',
      ascending: false,
      weight: rules.length === 0 ? 1 : 0,
    };
    onChange([...rules, newRule]);
  };

  const removeRule = (index: number) => {
    const newRules = rules.filter((_, i) => i !== index);
    // Normalize weights
    if (newRules.length > 0) {
      const totalWeight = newRules.reduce((sum, r) => sum + r.weight, 0);
      if (totalWeight !== 1) {
        const normalizedWeight = 1 / newRules.length;
        newRules.forEach((r) => (r.weight = normalizedWeight));
      }
    }
    onChange(newRules);
  };

  const updateRule = (index: number, updates: Partial<RankingRule>) => {
    const newRules = [...rules];
    newRules[index] = { ...newRules[index], ...updates };
    onChange(newRules);
  };

  const factorOptions = factors.map((f) => ({
    value: f.name,
    label: f.display_name,
  }));

  const sortOptions = [
    { value: 'desc', label: '降序 (从大到小)' },
    { value: 'asc', label: '升序 (从小到大)' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">排名规则</h3>
        <Button onClick={addRule} size="sm">
          添加规则
        </Button>
      </div>

      {rules.length === 0 && (
        <p className="text-sm text-gray-500">暂无排名规则，点击&nbsp;&quot;添加规则&quot;&nbsp;开始设置</p>
      )}

      {rules.map((rule, index) => (
        <div key={index} className="bg-gray-50 p-4 rounded-lg">
          <div className="flex items-center gap-3">
            {/* Factor selector */}
            <div className="flex-1">
              <Select
                label="因子"
                options={factorOptions}
                value={rule.factor_name}
                onChange={(e) => updateRule(index, { factor_name: e.target.value })}
              />
            </div>

            {/* Sort direction */}
            <div className="w-40">
              <Select
                label="排序方向"
                options={sortOptions}
                value={rule.ascending ? 'asc' : 'desc'}
                onChange={(e) => updateRule(index, { ascending: e.target.value === 'asc' })}
              />
            </div>

            {/* Weight */}
            {rules.length > 1 && (
              <div className="w-24">
                <Input
                  type="number"
                  label="权重"
                  min={0}
                  max={1}
                  step={0.1}
                  value={rule.weight}
                  onChange={(e) => updateRule(index, { weight: parseFloat(e.target.value) })}
                />
              </div>
            )}

            {/* Remove button */}
            <Button
              variant="danger"
              size="sm"
              onClick={() => removeRule(index)}
              className="mt-6"
            >
              删除
            </Button>
          </div>
        </div>
      ))}

      {rules.length > 1 && (
        <p className="text-sm text-gray-500">
          权重总和: {rules.reduce((sum, r) => sum + r.weight, 0).toFixed(2)}
          (建议总和为 1.0)
        </p>
      )}
    </div>
  );
}
