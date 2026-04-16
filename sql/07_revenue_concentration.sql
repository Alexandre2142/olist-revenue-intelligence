USE olist_revenue_intelligence;

-- ============================================
-- 1) CUSTOMER REVENUE CONCENTRATION
-- ============================================

WITH customer_revenue AS (
    SELECT
        customer_unique_id,
        SUM(total_revenue) AS revenue
    FROM fact_order_items
    GROUP BY customer_unique_id
),
customer_ranked AS (
    SELECT
        customer_unique_id,
        revenue,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) AS revenue_rank
    FROM customer_revenue
)

SELECT
    COUNT(*) AS total_customers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 10 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_10_customer_revenue_pct,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 50 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_50_customer_revenue_pct,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 100 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_100_customer_revenue_pct
FROM customer_ranked;


-- ============================================
-- 2) CATEGORY REVENUE CONCENTRATION
-- ============================================

WITH category_revenue AS (
    SELECT
        product_category_name_english AS product_category,
        SUM(total_revenue) AS revenue
    FROM fact_order_items
    GROUP BY product_category_name_english
),
category_ranked AS (
    SELECT
        product_category,
        revenue,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) AS revenue_rank
    FROM category_revenue
)

SELECT
    COUNT(*) AS total_categories,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 5 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_5_category_revenue_pct,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 10 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_10_category_revenue_pct,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 20 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_20_category_revenue_pct
FROM category_ranked;


-- ============================================
-- 3) STATE REVENUE CONCENTRATION
-- ============================================

WITH state_revenue AS (
    SELECT
        customer_state,
        SUM(total_revenue) AS revenue
    FROM fact_order_items
    GROUP BY customer_state
),
state_ranked AS (
    SELECT
        customer_state,
        revenue,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) AS revenue_rank
    FROM state_revenue
)

SELECT
    COUNT(*) AS total_states,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 1 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_1_state_revenue_pct,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 3 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_3_state_revenue_pct,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 5 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_5_state_revenue_pct,
    ROUND(100 * SUM(CASE WHEN revenue_rank <= 10 THEN revenue ELSE 0 END) / SUM(revenue), 2) AS top_10_state_revenue_pct
FROM state_ranked;


-- ============================================
-- 4) OPTIONAL DETAIL - TOP REVENUE STATES
-- ============================================

WITH state_revenue AS (
    SELECT
        customer_state,
        ROUND(SUM(total_revenue), 2) AS revenue
    FROM fact_order_items
    GROUP BY customer_state
)

SELECT
    customer_state,
    revenue
FROM state_revenue
ORDER BY revenue DESC
LIMIT 10;


-- ============================================
-- 5) OPTIONAL DETAIL - TOP REVENUE CATEGORIES
-- ============================================

WITH category_revenue AS (
    SELECT
        product_category_name_english AS product_category,
        ROUND(SUM(total_revenue), 2) AS revenue
    FROM fact_order_items
    GROUP BY product_category_name_english
)

SELECT
    product_category,
    revenue
FROM category_revenue
ORDER BY revenue DESC
LIMIT 10;