USE olist_revenue_intelligence;

-- ============================================
-- 04_geographic_performance.sql
-- Geographic performance by customer state
-- ============================================

SELECT
    customer_state,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    COUNT(*) AS items_sold,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM fact_order_items
GROUP BY customer_state
ORDER BY revenue DESC;
