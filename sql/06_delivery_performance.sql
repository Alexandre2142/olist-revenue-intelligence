USE olist_revenue_intelligence;

-- ============================================
-- 1) OVERALL DELIVERY PERFORMANCE
-- ============================================

SELECT
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay_days,
    ROUND(AVG(estimated_vs_actual_days), 2) AS avg_estimated_vs_actual_days,
    ROUND(100 * AVG(is_late), 2) AS late_delivery_rate_pct
FROM fact_order_items;


-- ============================================
-- 2) DELIVERY DELAY DECOMPOSITION
-- ============================================

SELECT
    ROUND(
        AVG(DATEDIFF(order_delivered_carrier_date, order_purchase_timestamp)),
        2
    ) AS avg_dispatch_delay_days,
    ROUND(
        AVG(DATEDIFF(order_delivered_customer_date, order_delivered_carrier_date)),
        2
    ) AS avg_carrier_to_customer_days
FROM fact_order_items;


-- ============================================
-- 3) LATE DELIVERY PERFORMANCE BY STATE
-- ============================================

SELECT
    customer_state,
    ROUND(100 * AVG(is_late), 2) AS late_rate,
    COUNT(DISTINCT order_id) AS orders
FROM fact_order_items
GROUP BY customer_state
ORDER BY late_rate DESC, orders DESC;


-- ============================================
-- 4) DELIVERY PERFORMANCE BY CATEGORY
-- ============================================

SELECT
    product_category_name_english AS product_category,
    ROUND(100 * AVG(is_late), 2) AS late_rate,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(order_item_id) AS items_sold
FROM fact_order_items
GROUP BY product_category_name_english
ORDER BY late_rate DESC, revenue DESC;


-- ============================================
-- 5) DELIVERY FRICTION BY STATE
-- ============================================

SELECT
    customer_state,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    ROUND(100 * AVG(is_late), 2) AS late_rate,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay
FROM fact_order_items
GROUP BY customer_state
ORDER BY revenue DESC;