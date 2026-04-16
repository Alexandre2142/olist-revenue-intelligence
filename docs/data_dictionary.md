# Data Dictionary

Initial retained features for late-delivery prediction:

| Column | Role | Notes |
| --- | --- | --- |
| order_id | Identifier | Kept outside model features. |
| is_late | Target | Binary target, 1 means late delivery. |
| order_revenue | Feature | Order-level revenue. |
| n_items | Feature | Number of items in the order. |
| n_sellers | Feature | Number of sellers involved. |
| n_categories | Feature | Number of product categories. |
| customer_state | Feature | Customer Brazilian state code. |
| estimated_delivery_days | Feature | Expected delivery window available before delivery outcome. |
| purchase_month | Feature | Month of purchase. |
| purchase_dayofweek | Feature | Day of week, Monday as 0. |
| purchase_hour | Feature | Purchase hour. |
| is_weekend | Feature | Weekend purchase indicator. |
| order_revenue_per_item | Feature | Revenue divided by item count. |

Review-based, actual-delivery, and post-outcome fields are excluded from model features to reduce leakage.

