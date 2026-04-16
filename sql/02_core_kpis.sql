USE olist_revenue_intelligence;

-- ============================================
-- 02_core_kpis.sql
-- Core business KPIs for fact_order_items
-- ============================================

SELECT
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    COUNT(*) AS total_items_sold
FROM fact_order_items;
