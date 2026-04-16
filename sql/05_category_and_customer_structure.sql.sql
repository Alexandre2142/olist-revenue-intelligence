USE olist_revenue_intelligence;

-- ============================================
-- 1) CATEGORY PERFORMANCE
-- ============================================

SELECT
    product_category_name_english AS product_category,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(order_item_id) AS items_sold,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT order_id), 2) AS avg_revenue_per_order
FROM fact_order_items
GROUP BY product_category_name_english
ORDER BY revenue DESC;


-- ============================================
-- 2) CUSTOMER REVENUE STRUCTURE
-- ============================================

WITH customer_summary AS (
    SELECT
        customer_unique_id,
        ROUND(SUM(total_revenue), 2) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(order_item_id) AS items_sold,
        ROUND(SUM(total_revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value
    FROM fact_order_items
    GROUP BY customer_unique_id
)

SELECT
    customer_unique_id,
    revenue,
    orders,
    items_sold,
    avg_order_value
FROM customer_summary
ORDER BY revenue DESC;


-- ============================================
-- 3) CUSTOMER STRUCTURE SUMMARY
-- Portfolio structure at customer level
-- ============================================

WITH customer_summary AS (
    SELECT
        customer_unique_id,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(order_item_id) AS items_sold
    FROM fact_order_items
    GROUP BY customer_unique_id
)

SELECT
    COUNT(*) AS total_customers,
    ROUND(AVG(revenue), 2) AS avg_revenue_per_customer,
    ROUND(AVG(orders), 2) AS avg_orders_per_customer,
    ROUND(AVG(items_sold), 2) AS avg_items_per_customer,
    SUM(CASE WHEN orders = 1 THEN 1 ELSE 0 END) AS single_order_customers,
    SUM(CASE WHEN orders > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(100 * SUM(CASE WHEN orders = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS single_order_customer_pct,
    ROUND(100 * SUM(CASE WHEN orders > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_customer_pct,
    MAX(orders) AS max_orders_by_customer,
    ROUND(MAX(revenue), 2) AS max_revenue_by_customer
FROM customer_summary;