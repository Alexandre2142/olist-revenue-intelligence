USE olist_revenue_intelligence;

-- ============================================
-- 1) STATE-LEVEL VALUE VS FRICTION
-- ============================================

SELECT
    customer_state,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    ROUND(100 * AVG(is_late), 2) AS late_rate,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay_days
FROM fact_order_items
GROUP BY customer_state
ORDER BY revenue DESC;


-- ============================================
-- 2) CATEGORY-LEVEL VALUE VS FRICTION
-- ============================================

SELECT
    product_category_name_english AS product_category,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_unique_id) AS customers,
    ROUND(100 * AVG(is_late), 2) AS late_rate,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay_days
FROM fact_order_items
GROUP BY product_category_name_english
ORDER BY revenue DESC;


-- ============================================
-- 3) HIGH-VALUE FRAGILE STATES
-- States with both strong revenue and elevated friction
-- ============================================

WITH state_value_friction AS (
    SELECT
        customer_state,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        100 * AVG(is_late) AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay_days
    FROM fact_order_items
    GROUP BY customer_state
),
state_benchmarks AS (
    SELECT
        AVG(revenue) AS avg_state_revenue,
        AVG(late_rate) AS avg_state_late_rate
    FROM state_value_friction
)

SELECT
    s.customer_state,
    ROUND(s.revenue, 2) AS revenue,
    s.orders,
    ROUND(s.late_rate, 2) AS late_rate,
    ROUND(s.avg_delivery_delay_days, 2) AS avg_delivery_delay_days
FROM state_value_friction s
CROSS JOIN state_benchmarks b
WHERE s.revenue > b.avg_state_revenue
  AND s.late_rate > b.avg_state_late_rate
ORDER BY s.revenue DESC, s.late_rate DESC;


-- ============================================
-- 4) HIGH-VALUE FRAGILE CATEGORIES
-- Categories with both strong revenue and elevated friction
-- ============================================

WITH category_value_friction AS (
    SELECT
        product_category_name_english AS product_category,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        100 * AVG(is_late) AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay_days
    FROM fact_order_items
    GROUP BY product_category_name_english
),
category_benchmarks AS (
    SELECT
        AVG(revenue) AS avg_category_revenue,
        AVG(late_rate) AS avg_category_late_rate
    FROM category_value_friction
)

SELECT
    c.product_category,
    ROUND(c.revenue, 2) AS revenue,
    c.orders,
    ROUND(c.late_rate, 2) AS late_rate,
    ROUND(c.avg_delivery_delay_days, 2) AS avg_delivery_delay_days
FROM category_value_friction c
CROSS JOIN category_benchmarks b
WHERE c.revenue > b.avg_category_revenue
  AND c.late_rate > b.avg_category_late_rate
ORDER BY c.revenue DESC, c.late_rate DESC;