'use client';

import { useEffect, useState } from 'react';
import { Layout, Button } from '@/components/common';
import { Stock } from '@/types';
import { stockService } from '@/services';

export default function DataPage() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadStocks();
  }, []);

  const loadStocks = async () => {
    try {
      const data = await stockService.getStocks();
      setStocks(data);
    } catch (error) {
      console.error('Failed to load stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await stockService.refreshData();
      await loadStocks();
    } catch (error) {
      console.error('Failed to refresh data:', error);
    } finally {
      setRefreshing(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900">数据中心</h1>
          <Button onClick={handleRefresh} disabled={refreshing}>
            {refreshing ? '刷新中...' : '刷新数据'}
          </Button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-6 rounded-lg border border-gray-100">
            <p className="text-sm text-gray-500">股票总数</p>
            <p className="text-3xl font-semibold text-gray-900 mt-2">
              {stocks.length.toLocaleString()}
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg border border-gray-100">
            <p className="text-sm text-gray-500">数据源</p>
            <p className="text-3xl font-semibold text-gray-900 mt-2">AkShare</p>
          </div>
          <div className="bg-white p-6 rounded-lg border border-gray-100">
            <p className="text-sm text-gray-500">行情数据</p>
            <p className="text-3xl font-semibold text-gray-900 mt-2">--</p>
          </div>
          <div className="bg-white p-6 rounded-lg border border-gray-100">
            <p className="text-sm text-gray-500">财务数据</p>
            <p className="text-3xl font-semibold text-gray-900 mt-2">--</p>
          </div>
        </div>

        {/* Stock List */}
        <div className="bg-white rounded-lg border border-gray-100">
          <div className="p-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">股票列表</h2>
          </div>
          {loading ? (
            <div className="p-12 text-center text-gray-500">加载中...</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      代码
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      名称
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      行业
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      市场
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {stocks.slice(0, 50).map((stock) => (
                    <tr key={stock.ts_code} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {stock.ts_code}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {stock.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {stock.industry || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {stock.market || '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {stocks.length > 50 && (
                <div className="p-4 text-center text-sm text-gray-500">
                  显示前 50 条，共 {stocks.length} 条
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
