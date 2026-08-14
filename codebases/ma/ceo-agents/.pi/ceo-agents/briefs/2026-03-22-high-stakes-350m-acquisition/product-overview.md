# Product Overview — Cloudvault

## What We Are
Cloudvault is an enterprise data infrastructure platform that provides real-time data lineage, impact analysis, and data reliability monitoring for companies running complex data pipelines across cloud environments.

## Core Product
- **Real-time data lineage engine:** Automatically maps every data transformation from source to dashboard across Snowflake, Databricks, BigQuery, Redshift, and 40+ connectors. Sub-second propagation tracking.
- **Impact analysis:** Before you change a column, table, or pipeline, see exactly what dashboards, ML models, and downstream consumers will break. Used by data teams to prevent incidents before deploying changes.
- **Data reliability monitoring:** Anomaly detection on data freshness, volume, schema drift, and distribution shifts. Alerts data engineers before stakeholders notice.

## Core Differentiator
Column-level lineage at runtime, not just static parsing. We instrument query engines directly (Snowflake query history, Spark execution plans, dbt manifest parsing) to build a live dependency graph that updates in real-time. Competitors parse SQL statically — they miss dynamic queries, temporary tables, and UDFs. Our graph has 40x more edges than the next best tool.

## Key IP
- Lineage graph engine: proprietary graph database optimized for real-time DAG traversal at billion-edge scale
- Query instrumentation SDK: zero-config agents for Snowflake, Databricks, BigQuery, Redshift
- Impact scoring algorithm: predicts which downstream consumers are most affected by upstream changes
- 3 patents filed (2 granted): runtime lineage extraction, incremental graph updates, cross-platform lineage stitching

## Pricing
- Starter: $2K/month (up to 500 tables, 5 users)
- Professional: $8K/month (up to 5,000 tables, 25 users, impact analysis)
- Enterprise: custom ($15K–$50K/month, unlimited tables, SSO, dedicated support, SLAs)

## Competitive Landscape
- **Atlan:** Well-funded ($105M raised), strong catalog play, lineage is a feature not the core — static parsing, no runtime instrumentation
- **Alation:** Public company, enterprise catalog — lineage is bolt-on, weak on real-time
- **AWS Glue DataBrew lineage:** Preview feature, basic DAG visualization, no impact analysis, no cross-platform — but free for AWS customers
- **Monte Carlo:** Data reliability focused, lineage is secondary — we compete on reliability monitoring but our lineage is 10x deeper
