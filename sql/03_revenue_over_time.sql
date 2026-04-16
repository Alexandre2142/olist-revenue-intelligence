USE olist_revenue_intelligence;

-- ============================================
-- 03_revenue_over_time.sql
-- Revenue evolution over time
-- ============================================

SELECT
    order_month,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    COUNT(*) AS items_sold,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM fact_order_items
GROUP BY order_month
ORDER BY order_month;
