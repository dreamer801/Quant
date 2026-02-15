/**
 * Strategy Types
 */

export type Operator = '>' | '>=' | '<' | '<=' | '==' | '!=' | 'between';
export type LogicOperator = 'and' | 'or';
export type RebalanceFrequency = 'daily' | 'weekly' | 'monthly' | 'custom';

export interface FilterCondition {
  factor_name: string;
  operator: Operator;
  value: number | [number, number];
  logic_op?: LogicOperator;
}

export interface RankingRule {
  factor_name: string;
  ascending: boolean;
  weight: number;
}

export interface TradingRule {
  rebalance_frequency: RebalanceFrequency;
  max_position_pct: number;
  cash_reserve_pct: number;
  commission_rate: number;
  slippage: number;
}

export interface StrategyConfig {
  universe: string[];
  filter_conditions: FilterCondition[];
  ranking_rules: RankingRule[];
  trading_rule: TradingRule;
  top_n: number;
}

export interface Strategy {
  id: string;
  name: string;
  description?: string;
  config: StrategyConfig;
  created_at: string;
  updated_at: string;
}

export interface StrategyCreate {
  name: string;
  description?: string;
  config: StrategyConfig;
}

export interface StrategyUpdate {
  name?: string;
  description?: string;
  config?: StrategyConfig;
}

export interface FactorDefinition {
  name: string;
  display_name: string;
  category: string;
  description: string;
  unit: string;
  higher_is_better: boolean;
}
