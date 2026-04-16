USE olist_revenue_intelligence;

-- ============================================
-- 1) STATE SEGMENTATION BASE
-- ============================================

WITH state_value_friction AS (
    SELECT
        customer_state,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(DISTINCT customer_unique_id) AS customers,
        AVG(is_late) * 100 AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay
    FROM fact_order_items
    GROUP BY customer_state
),
global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
state_segmentation AS (
    SELECT
        s.customer_state,
        ROUND(s.revenue, 2) AS revenue,
        s.orders,
        s.customers,
        ROUND(s.late_rate, 2) AS late_rate,
        ROUND(s.avg_delivery_delay, 2) AS avg_delivery_delay,
        ROUND(100 * s.revenue / SUM(s.revenue) OVER (), 2) AS revenue_share_pct,
        CASE
            WHEN (100 * s.revenue / SUM(s.revenue) OVER ()) > 2 THEN 'High value'
            ELSE 'Lower value'
        END AS market_value_level,
        CASE
            WHEN s.late_rate > g.global_late_rate THEN 'High friction'
            ELSE 'Lower friction'
        END AS market_friction_level
    FROM state_value_friction s
    CROSS JOIN global_benchmark g
)

SELECT
    customer_state,
    revenue,
    orders,
    customers,
    late_rate,
    avg_delivery_delay,
    revenue_share_pct,
    market_value_level,
    market_friction_level,
    CASE
        WHEN market_value_level = 'High value' AND market_friction_level = 'Lower friction' THEN 'Core healthy market'
        WHEN market_value_level = 'High value' AND market_friction_level = 'High friction' THEN 'Core fragile market'
        WHEN market_value_level = 'Lower value' AND market_friction_level = 'Lower friction' THEN 'Secondary healthy market'
        WHEN market_value_level = 'Lower value' AND market_friction_level = 'High friction' THEN 'Secondary fragile market'
    END AS market_segment_label
FROM state_segmentation
ORDER BY revenue_share_pct DESC, late_rate DESC;


-- ============================================
-- 2) SEGMENT SUMMARY
-- ============================================

WITH state_value_friction AS (
    SELECT
        customer_state,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        AVG(is_late) * 100 AS late_rate
    FROM fact_order_items
    GROUP BY customer_state
),
global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
state_segmentation AS (
    SELECT
        s.customer_state,
        s.revenue,
        s.orders,
        CASE
            WHEN (100 * s.revenue / SUM(s.revenue) OVER ()) > 2 THEN 'High value'
            ELSE 'Lower value'
        END AS market_value_level,
        CASE
            WHEN s.late_rate > g.global_late_rate THEN 'High friction'
            ELSE 'Lower friction'
        END AS market_friction_level
    FROM state_value_friction s
    CROSS JOIN global_benchmark g
),
labeled_segments AS (
    SELECT
        customer_state,
        revenue,
        orders,
        CASE
            WHEN market_value_level = 'High value' AND market_friction_level = 'Lower friction' THEN 'Core healthy market'
            WHEN market_value_level = 'High value' AND market_friction_level = 'High friction' THEN 'Core fragile market'
            WHEN market_value_level = 'Lower value' AND market_friction_level = 'Lower friction' THEN 'Secondary healthy market'
            WHEN market_value_level = 'Lower value' AND market_friction_level = 'High friction' THEN 'Secondary fragile market'
        END AS market_segment_label
    FROM state_segmentation
)

SELECT
    market_segment_label,
    COUNT(*) AS n_states,
    ROUND(SUM(revenue), 2) AS total_revenue,
    SUM(orders) AS total_orders,
    ROUND(100 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2) AS revenue_share_pct
FROM labeled_segments
GROUP BY market_segment_label
ORDER BY total_revenue DESC;


-- ============================================
-- 3) CORE MARKETS
-- ============================================

WITH state_value_friction AS (
    SELECT
        customer_state,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        AVG(is_late) * 100 AS late_rate
    FROM fact_order_items
    GROUP BY customer_state
),
global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
state_segmentation AS (
    SELECT
        s.customer_state,
        s.revenue,
        s.orders,
        s.late_rate,
        ROUND(100 * s.revenue / SUM(s.revenue) OVER (), 2) AS revenue_share_pct,
        CASE
            WHEN (100 * s.revenue / SUM(s.revenue) OVER ()) > 2 THEN 'High value'
            ELSE 'Lower value'
        END AS market_value_level,
        CASE
            WHEN s.late_rate > g.global_late_rate THEN 'High friction'
            ELSE 'Lower friction'
        END AS market_friction_level
    FROM state_value_friction s
    CROSS JOIN global_benchmark g
)

SELECT
    customer_state,
    ROUND(revenue, 2) AS revenue,
    orders,
    ROUND(late_rate, 2) AS late_rate,
    revenue_share_pct,
    CASE
        WHEN market_value_level = 'High value' AND market_friction_level = 'Lower friction' THEN 'Core healthy market'
        WHEN market_value_level = 'High value' AND market_friction_level = 'High friction' THEN 'Core fragile market'
        WHEN market_value_level = 'Lower value' AND market_friction_level = 'Lower friction' THEN 'Secondary healthy market'
        WHEN market_value_level = 'Lower value' AND market_friction_level = 'High friction' THEN 'Secondary fragile market'
    END AS market_segment_label
FROM state_segmentation
WHERE market_value_level = 'High value'
ORDER BY revenue DESC;


-- ============================================
-- 4) FRAGILE MARKETS
-- ============================================

WITH state_value_friction AS (
    SELECT
        customer_state,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        AVG(is_late) * 100 AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay
    FROM fact_order_items
    GROUP BY customer_state
),
global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
state_segmentation AS (
    SELECT
        s.customer_state,
        s.revenue,
        s.orders,
        s.late_rate,
        s.avg_delivery_delay,
        ROUND(100 * s.revenue / SUM(s.revenue) OVER (), 2) AS revenue_share_pct,
        CASE
            WHEN (100 * s.revenue / SUM(s.revenue) OVER ()) > 2 THEN 'High value'
            ELSE 'Lower value'
        END AS market_value_level,
        CASE
            WHEN s.late_rate > g.global_late_rate THEN 'High friction'
            ELSE 'Lower friction'
        END AS market_friction_level
    FROM state_value_friction s
    CROSS JOIN global_benchmark g
)

SELECT
    customer_state,
    ROUND(revenue, 2) AS revenue,
    orders,
    ROUND(late_rate, 2) AS late_rate,
    ROUND(avg_delivery_delay, 2) AS avg_delivery_delay,
    revenue_share_pct,
    CASE
        WHEN market_value_level = 'High value' AND market_friction_level = 'Lower friction' THEN 'Core healthy market'
        WHEN market_value_level = 'High value' AND market_friction_level = 'High friction' THEN 'Core fragile market'
        WHEN market_value_level = 'Lower value' AND market_friction_level = 'Lower friction' THEN 'Secondary healthy market'
        WHEN market_value_level = 'Lower value' AND market_friction_level = 'High friction' THEN 'Secondary fragile market'
    END AS market_segment_label
FROM state_segmentation
WHERE market_friction_level = 'High friction'
ORDER BY revenue_share_pct DESC, late_rate DESC;