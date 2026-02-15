'use client';

import { StrategyConfig, FactorDefinition } from '@/types';
import { FilterCondition, RankingRule, TradingRule } from '@/types';
import FilterConditionBuilder from './FilterConditionBuilder';
import RankingRuleBuilder from './RankingRuleBuilder';
import TradingRuleBuilder from './TradingRuleBuilder';
import Input from '@/components/common/Input';

interface StrategyBuilderProps {
  name: string;
  description: string;
  config: StrategyConfig;
  factors: FactorDefinition[];
  onNameChange: (name: string) => void;
  onDescriptionChange: (description: string) => void;
  onConfigChange: (config: StrategyConfig) => void;
}

export default function StrategyBuilder({
  name,
  description,
  config,
  factors,
  onNameChange,
  onDescriptionChange,
  onConfigChange,
}: StrategyBuilderProps) {
  const updateFilters = (filter_conditions: FilterCondition[]) => {
    onConfigChange({ ...config, filter_conditions });
  };

  const updateRanking = (ranking_rules: RankingRule[]) => {
    onConfigChange({ ...config, ranking_rules });
  };

  const updateTradingRule = (trading_rule: TradingRule) => {
    onConfigChange({ ...config, trading_rule });
  };

  const updateTopN = (top_n: number) => {
    onConfigChange({ ...config, top_n });
  };

  return (
    <div className="space-y-6">
      {/* Basic Info */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">基本信息</h2>
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="策略名称"
            value={name}
            onChange={(e) => onNameChange(e.target.value)}
            placeholder="输入策略名称"
          />
          <Input
            label="策略描述"
            value={description}
            onChange={(e) => onDescriptionChange(e.target.value)}
            placeholder="输入策略描述（可选）"
          />
        </div>
      </div>

      {/* Filter Conditions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <FilterConditionBuilder
          conditions={config.filter_conditions}
          onChange={updateFilters}
          factors={factors}
        />
      </div>

      {/* Ranking Rules */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <RankingRuleBuilder
          rules={config.ranking_rules}
          onChange={updateRanking}
          factors={factors}
        />
      </div>

      {/* Trading Rules */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <TradingRuleBuilder rule={config.trading_rule} onChange={updateTradingRule} />
      </div>

      {/* Top N */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <Input
          type="number"
          label="持仓股票数量 (Top N)"
          min={1}
          max={100}
          value={config.top_n}
          onChange={(e) => updateTopN(parseInt(e.target.value))}
        />
      </div>
    </div>
  );
}
