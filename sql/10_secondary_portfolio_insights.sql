USE olist_revenue_intelligence;

-- ============================================
-- 1) CATEGORY ROLE PROFILE
-- ============================================

SELECT
    product_category_name_english AS product_category,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(order_item_id) AS items_sold,
    ROUND(100 * AVG(is_late), 2) AS late_rate,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT order_id), 2) AS avg_revenue_per_order,
    ROUND(100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER (), 2) AS revenue_share_pct
FROM fact_order_items
GROUP BY product_category_name_english
ORDER BY revenue DESC;


-- ============================================
-- 2) CATEGORY SEGMENTATION
-- High value: revenue share > 3%
-- High friction: late rate > global late rate
-- ============================================

WITH global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
category_profile AS (
    SELECT
        product_category_name_english AS product_category,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(order_item_id) AS items_sold,
        AVG(is_late) * 100 AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay,
        SUM(total_revenue) / COUNT(DISTINCT order_id) AS avg_revenue_per_order,
        100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER () AS revenue_share_pct
    FROM fact_order_items
    GROUP BY product_category_name_english
)

SELECT
    c.product_category,
    ROUND(c.revenue, 2) AS revenue,
    c.orders,
    c.items_sold,
    ROUND(c.late_rate, 2) AS late_rate,
    ROUND(c.avg_delivery_delay, 2) AS avg_delivery_delay,
    ROUND(c.avg_revenue_per_order, 2) AS avg_revenue_per_order,
    ROUND(c.revenue_share_pct, 2) AS revenue_share_pct,
    CASE
        WHEN c.revenue_share_pct > 3 THEN 'High value'
        ELSE 'Lower value'
    END AS category_value_level,
    CASE
        WHEN c.late_rate > g.global_late_rate THEN 'High friction'
        ELSE 'Lower friction'
    END AS category_friction_level,
    CASE
        WHEN c.revenue_share_pct > 3 AND c.late_rate <= g.global_late_rate THEN 'Core healthy category'
        WHEN c.revenue_share_pct > 3 AND c.late_rate > g.global_late_rate THEN 'Core fragile category'
        WHEN c.revenue_share_pct <= 3 AND c.late_rate <= g.global_late_rate THEN 'Secondary healthy category'
        WHEN c.revenue_share_pct <= 3 AND c.late_rate > g.global_late_rate THEN 'Secondary fragile category'
    END AS category_segment_label
FROM category_profile c
CROSS JOIN global_benchmark g
ORDER BY c.revenue DESC;


-- ============================================
-- 3) CATEGORY SEGMENT SUMMARY
-- ============================================

WITH global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
category_profile AS (
    SELECT
        product_category_name_english AS product_category,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        AVG(is_late) * 100 AS late_rate,
        100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER () AS revenue_share_pct
    FROM fact_order_items
    GROUP BY product_category_name_english
),
category_segmentation AS (
    SELECT
        product_category,
        revenue,
        orders,
        CASE
            WHEN revenue_share_pct > 3 AND late_rate <= g.global_late_rate THEN 'Core healthy category'
            WHEN revenue_share_pct > 3 AND late_rate > g.global_late_rate THEN 'Core fragile category'
            WHEN revenue_share_pct <= 3 AND late_rate <= g.global_late_rate THEN 'Secondary healthy category'
            WHEN revenue_share_pct <= 3 AND late_rate > g.global_late_rate THEN 'Secondary fragile category'
        END AS category_segment_label
    FROM category_profile
    CROSS JOIN global_benchmark g
)

SELECT
    category_segment_label,
    COUNT(*) AS n_categories,
    ROUND(SUM(revenue), 2) AS total_revenue,
    SUM(orders) AS total_orders,
    ROUND(100 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2) AS revenue_share_pct
FROM category_segmentation
GROUP BY category_segment_label
ORDER BY total_revenue DESC;


-- ============================================
-- 4) FRAGILE CATEGORIES
-- ============================================

WITH global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
category_profile AS (
    SELECT
        product_category_name_english AS product_category,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(order_item_id) AS items_sold,
        AVG(is_late) * 100 AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay,
        SUM(total_revenue) / COUNT(DISTINCT order_id) AS avg_revenue_per_order,
        100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER () AS revenue_share_pct
    FROM fact_order_items
    GROUP BY product_category_name_english
),
category_segmentation AS (
    SELECT
        c.*,
        CASE
            WHEN c.revenue_share_pct > 3 AND c.late_rate <= g.global_late_rate THEN 'Core healthy category'
            WHEN c.revenue_share_pct > 3 AND c.late_rate > g.global_late_rate THEN 'Core fragile category'
            WHEN c.revenue_share_pct <= 3 AND c.late_rate <= g.global_late_rate THEN 'Secondary healthy category'
            WHEN c.revenue_share_pct <= 3 AND c.late_rate > g.global_late_rate THEN 'Secondary fragile category'
        END AS category_segment_label
    FROM category_profile c
    CROSS JOIN global_benchmark g
)

SELECT
    product_category,
    ROUND(revenue, 2) AS revenue,
    orders,
    items_sold,
    ROUND(late_rate, 2) AS late_rate,
    ROUND(avg_delivery_delay, 2) AS avg_delivery_delay,
    ROUND(avg_revenue_per_order, 2) AS avg_revenue_per_order,
    ROUND(revenue_share_pct, 2) AS revenue_share_pct,
    category_segment_label
FROM category_segmentation
WHERE category_segment_label IN ('Core fragile category', 'Secondary fragile category')
ORDER BY revenue_share_pct DESC, late_rate DESC;


-- ============================================
-- 5) SELLER PROFILE
-- ============================================

SELECT
    seller_id,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(order_item_id) AS items_sold,
    ROUND(100 * AVG(is_late), 2) AS late_rate,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT order_id), 2) AS avg_revenue_per_order,
    ROUND(100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER (), 2) AS revenue_share_pct
FROM fact_order_items
GROUP BY seller_id
ORDER BY revenue DESC;


-- ============================================
-- 6) SELLER CONCENTRATION
-- ============================================

WITH seller_profile AS (
    SELECT
        seller_id,
        SUM(total_revenue) AS revenue,
        100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER () AS revenue_share_pct,
        ROW_NUMBER() OVER (ORDER BY SUM(total_revenue) DESC) AS revenue_rank
    FROM fact_order_items
    GROUP BY seller_id
)

SELECT
    COUNT(*) AS total_sellers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN revenue_rank <= 10 THEN revenue_share_pct ELSE 0 END), 2) AS top_10_seller_revenue_pct,
    ROUND(SUM(CASE WHEN revenue_rank <= 50 THEN revenue_share_pct ELSE 0 END), 2) AS top_50_seller_revenue_pct,
    ROUND(SUM(CASE WHEN revenue_rank <= 100 THEN revenue_share_pct ELSE 0 END), 2) AS top_100_seller_revenue_pct
FROM seller_profile;


-- ============================================
-- 7) SELLER SEGMENTATION
-- High value: revenue share > 0.3%
-- High friction: late rate > global late rate
-- ============================================

WITH global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
seller_profile AS (
    SELECT
        seller_id,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(order_item_id) AS items_sold,
        AVG(is_late) * 100 AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay,
        SUM(total_revenue) / COUNT(DISTINCT order_id) AS avg_revenue_per_order,
        100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER () AS revenue_share_pct
    FROM fact_order_items
    GROUP BY seller_id
)

SELECT
    s.seller_id,
    ROUND(s.revenue, 2) AS revenue,
    s.orders,
    s.items_sold,
    ROUND(s.late_rate, 2) AS late_rate,
    ROUND(s.avg_delivery_delay, 2) AS avg_delivery_delay,
    ROUND(s.avg_revenue_per_order, 2) AS avg_revenue_per_order,
    ROUND(s.revenue_share_pct, 2) AS revenue_share_pct,
    CASE
        WHEN s.revenue_share_pct > 0.3 THEN 'High value'
        ELSE 'Lower value'
    END AS seller_value_level,
    CASE
        WHEN s.late_rate > g.global_late_rate THEN 'High friction'
        ELSE 'Lower friction'
    END AS seller_friction_level,
    CASE
        WHEN s.revenue_share_pct > 0.3 AND s.late_rate <= g.global_late_rate THEN 'Core healthy seller'
        WHEN s.revenue_share_pct > 0.3 AND s.late_rate > g.global_late_rate THEN 'Core fragile seller'
        WHEN s.revenue_share_pct <= 0.3 AND s.late_rate <= g.global_late_rate THEN 'Secondary healthy seller'
        WHEN s.revenue_share_pct <= 0.3 AND s.late_rate > g.global_late_rate THEN 'Secondary fragile seller'
    END AS seller_segment_label
FROM seller_profile s
CROSS JOIN global_benchmark g
ORDER BY s.revenue DESC;


-- ============================================
-- 8) SELLER SEGMENT SUMMARY
-- ============================================

WITH global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
seller_profile AS (
    SELECT
        seller_id,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        AVG(is_late) * 100 AS late_rate,
        100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER () AS revenue_share_pct
    FROM fact_order_items
    GROUP BY seller_id
),
seller_segmentation AS (
    SELECT
        seller_id,
        revenue,
        orders,
        CASE
            WHEN revenue_share_pct > 0.3 AND late_rate <= g.global_late_rate THEN 'Core healthy seller'
            WHEN revenue_share_pct > 0.3 AND late_rate > g.global_late_rate THEN 'Core fragile seller'
            WHEN revenue_share_pct <= 0.3 AND late_rate <= g.global_late_rate THEN 'Secondary healthy seller'
            WHEN revenue_share_pct <= 0.3 AND late_rate > g.global_late_rate THEN 'Secondary fragile seller'
        END AS seller_segment_label
    FROM seller_profile
    CROSS JOIN global_benchmark g
)

SELECT
    seller_segment_label,
    COUNT(*) AS n_sellers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    SUM(orders) AS total_orders,
    ROUND(100 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2) AS revenue_share_pct
FROM seller_segmentation
GROUP BY seller_segment_label
ORDER BY total_revenue DESC;


-- ============================================
-- 9) FRAGILE SELLERS
-- ============================================

WITH global_benchmark AS (
    SELECT
        AVG(is_late) * 100 AS global_late_rate
    FROM fact_order_items
),
seller_profile AS (
    SELECT
        seller_id,
        SUM(total_revenue) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(order_item_id) AS items_sold,
        AVG(is_late) * 100 AS late_rate,
        AVG(delivery_delay_days) AS avg_delivery_delay,
        SUM(total_revenue) / COUNT(DISTINCT order_id) AS avg_revenue_per_order,
        100 * SUM(total_revenue) / SUM(SUM(total_revenue)) OVER () AS revenue_share_pct
    FROM fact_order_items
    GROUP BY seller_id
),
seller_segmentation AS (
    SELECT
        s.*,
        CASE
            WHEN s.revenue_share_pct > 0.3 AND s.late_rate <= g.global_late_rate THEN 'Core healthy seller'
            WHEN s.revenue_share_pct > 0.3 AND s.late_rate > g.global_late_rate THEN 'Core fragile seller'
            WHEN s.revenue_share_pct <= 0.3 AND s.late_rate <= g.global_late_rate THEN 'Secondary healthy seller'
            WHEN s.revenue_share_pct <= 0.3 AND s.late_rate > g.global_late_rate THEN 'Secondary fragile seller'
        END AS seller_segment_label
    FROM seller_profile s
    CROSS JOIN global_benchmark g
)

SELECT
    seller_id,
    ROUND(revenue, 2) AS revenue,
    orders,
    items_sold,
    ROUND(late_rate, 2) AS late_rate,
    ROUND(avg_delivery_delay, 2) AS avg_delivery_delay,
    ROUND(avg_revenue_per_order, 2) AS avg_revenue_per_order,
    ROUND(revenue_share_pct, 2) AS revenue_share_pct,
    seller_segment_label
FROM seller_segmentation
WHERE seller_segment_label IN ('Core fragile seller', 'Secondary fragile seller')
ORDER BY revenue_share_pct DESC, late_rate DESC;