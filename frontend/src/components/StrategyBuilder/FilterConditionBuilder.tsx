'use client';

import { FilterCondition, Operator, LogicOperator, FactorDefinition } from '@/types';
import { Button, Select } from '@/components/common';
import Input from '@/components/common/Input';

interface FilterConditionBuilderProps {
  conditions: FilterCondition[];
  onChange: (conditions: FilterCondition[]) => void;
  factors: FactorDefinition[];
}

const operatorOptions = [
  { value: '>', label: '大于' },
  { value: '>=', label: '大于等于' },
  { value: '<', label: '小于' },
  { value: '<=', label: '小于等于' },
  { value: '==', label: '等于' },
  { value: '!=', label: '不等于' },
  { value: 'between', label: '介于' },
];

const logicOptions = [
  { value: 'and', label: '且 (AND)' },
  { value: 'or', label: '或 (OR)' },
];

export default function FilterConditionBuilder({
  conditions,
  onChange,
  factors,
}: FilterConditionBuilderProps) {
  const addCondition = () => {
    const newCondition: FilterCondition = {
      factor_name: factors[0]?.name || '',
      operator: '>' as Operator,
      value: 0,
      logic_op: conditions.length > 0 ? 'and' as LogicOperator : undefined,
    };
    onChange([...conditions, newCondition]);
  };

  const removeCondition = (index: number) => {
    const newConditions = conditions.filter((_, i) => i !== index);
    // Update logic_op for first condition
    if (newConditions.length > 0 && newConditions[0].logic_op) {
      newConditions[0] = { ...newConditions[0], logic_op: undefined };
    }
    onChange(newConditions);
  };

  const updateCondition = (index: number, updates: Partial<FilterCondition>) => {
    const newConditions = [...conditions];
    newConditions[index] = { ...newConditions[index], ...updates };
    onChange(newConditions);
  };

  const factorOptions = factors.map((f) => ({
    value: f.name,
    label: f.display_name,
  }));

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">筛选条件</h3>
        <Button onClick={addCondition} size="sm">
          添加条件
        </Button>
      </div>

      {conditions.length === 0 && (
        <p className="text-sm text-gray-500">暂无筛选条件，点击&nbsp;&quot;添加条件&quot;&nbsp;开始设置</p>
      )}

      {conditions.map((condition, index) => (
        <div key={index} className="bg-gray-50 p-4 rounded-lg">
          <div className="flex items-start gap-3">
            {/* Logic operator for non-first conditions */}
            {index > 0 && (
              <div className="w-24">
                <Select
                  options={logicOptions}
                  value={condition.logic_op || 'and'}
                  onChange={(e) =>
                    updateCondition(index, { logic_op: e.target.value as LogicOperator })
                  }
                />
              </div>
            )}

            {/* Factor selector */}
            <div className="flex-1">
              <Select
                label="因子"
                options={factorOptions}
                value={condition.factor_name}
                onChange={(e) => updateCondition(index, { factor_name: e.target.value })}
              />
            </div>

            {/* Operator selector */}
            <div className="w-32">
              <Select
                label="运算符"
                options={operatorOptions}
                value={condition.operator}
                onChange={(e) => updateCondition(index, { operator: e.target.value as Operator })}
              />
            </div>

            {/* Value input(s) */}
            <div className="w-32">
              {condition.operator === 'between' ? (
                <div className="flex gap-2">
                  <Input
                    type="number"
                    label="最小值"
                    value={Array.isArray(condition.value) ? condition.value[0] : 0}
                    onChange={(e) =>
                      updateCondition(index, {
                        value: [
                          parseFloat(e.target.value),
                          Array.isArray(condition.value) ? condition.value[1] : 0,
                        ] as [number, number],
                      })
                    }
                  />
                  <Input
                    type="number"
                    label="最大值"
                    value={Array.isArray(condition.value) ? condition.value[1] : 0}
                    onChange={(e) =>
                      updateCondition(index, {
                        value: [
                          Array.isArray(condition.value) ? condition.value[0] : 0,
                          parseFloat(e.target.value),
                        ] as [number, number],
                      })
                    }
                  />
                </div>
              ) : (
                <Input
                  type="number"
                  label="值"
                  value={typeof condition.value === 'number' ? condition.value : 0}
                  onChange={(e) =>
                    updateCondition(index, { value: parseFloat(e.target.value) })
                  }
                />
              )}
            </div>

            {/* Remove button */}
            <Button
              variant="danger"
              size="sm"
              onClick={() => removeCondition(index)}
              className="mt-6"
            >
              删除
            </Button>
          </div>
        </div>
      ))}
    </div>
  );
}
