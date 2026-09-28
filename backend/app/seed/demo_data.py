import logging
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.models import (
    Customer, Feedback, Product, ProductVersion, ProductDecision, EngineeringDecision,
    ArchitectureDecision, Experiment, Outcome, MemoryEvent, DecisionRelationship, TechnologyArea
)
from app.services.decision_memory import memory_manager

logger = logging.getLogger("demo_data_seed")

def seed_demo_data(db: Session) -> dict:
    # Clear existing tables first
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    logger.info("Seeding 60-80 realistic interconnected organizational events into PostgreSQL & Hindsight...")

    # Customers
    customers = [
        Customer(id="CUST-101", name="Acme Corp", domain="acme.com", tier="Enterprise"),
        Customer(id="CUST-102", name="TechFlow Inc", domain="techflow.io", tier="Enterprise"),
        Customer(id="CUST-103", name="Starlight Media", domain="starlight.com", tier="Growth"),
        Customer(id="CUST-104", name="DataWave", domain="datawave.dev", tier="Enterprise"),
        Customer(id="CUST-105", name="CloudScale Labs", domain="cloudscale.io", tier="Enterprise"),
        Customer(id="CUST-106", name="Apex Dynamics", domain="apexdynamics.com", tier="Growth"),
    ]
    for c in customers:
        db.add(c)

    # Technologies
    techs = [
        TechnologyArea(id="TECH-1", name="PostgreSQL", category="Database", description="Primary relational datastore and search engine"),
        TechnologyArea(id="TECH-2", name="Redis", category="Caching", description="In-memory cache for session & rate limits"),
        TechnologyArea(id="TECH-3", name="Background Workers", category="Queue", description="Async task processing engine"),
        TechnologyArea(id="TECH-4", name="Elasticsearch", category="Search", description="Evaluated specialized search cluster"),
        TechnologyArea(id="TECH-5", name="FastAPI", category="Backend", description="Python API service layer"),
        TechnologyArea(id="TECH-6", name="React / Next.js", category="Frontend", description="Single page SaaS web frontend"),
    ]
    for t in techs:
        db.add(t)

    # Feedback (30 items)
    feedbacks = [
        # Story 2: Search
        Feedback(id="FB-1001", customer_name="Acme Corp", content="Search results are slow and irrelevant for large project datasets.", product_area="Search & Relevance", sentiment="Negative", priority="High", date="2026-01-12", status="Addressed"),
        Feedback(id="FB-1002", customer_name="TechFlow Inc", content="Filtering search by tags takes over 4 seconds.", product_area="Search & Relevance", sentiment="Negative", priority="High", date="2026-01-15", status="Addressed"),
        Feedback(id="FB-1003", customer_name="DataWave", content="Exact string search in audit logs fails to find recent records.", product_area="Search & Relevance", sentiment="Negative", priority="Medium", date="2026-01-20", status="Addressed"),
        Feedback(id="FB-1004", customer_name="Starlight Media", content="Search response time spikes during peak business hours.", product_area="Search & Relevance", sentiment="Negative", priority="Critical", date="2026-01-25", status="Addressed"),
        Feedback(id="FB-1005", customer_name="CloudScale Labs", content="Search relevance ranking places archived records above active workspace items.", product_area="Search & Relevance", sentiment="Negative", priority="Medium", date="2026-02-01", status="Addressed"),
        Feedback(id="FB-1006", customer_name="Apex Dynamics", content="Search query performance is degraded when searching multi-word titles.", product_area="Search & Relevance", sentiment="Negative", priority="Medium", date="2026-06-20", status="Open"),

        # Story 1: Onboarding
        Feedback(id="FB-1010", customer_name="TechFlow Inc", content="Onboarding verification is confusing and users get stuck on step 2.", product_area="User Onboarding", sentiment="Negative", priority="High", date="2026-01-10", status="Addressed"),
        Feedback(id="FB-1011", customer_name="Acme Corp", content="Email verification tokens expire before our security gateway scans them.", product_area="User Onboarding", sentiment="Negative", priority="High", date="2026-01-14", status="Addressed"),
        Feedback(id="FB-1012", customer_name="Starlight Media", content="New workspace members struggle to complete identity verification.", product_area="User Onboarding", sentiment="Negative", priority="Medium", date="2026-01-18", status="Addressed"),
        Feedback(id="FB-1013", customer_name="DataWave", content="Onboarding checklist UI does not mark completed items automatically.", product_area="User Onboarding", sentiment="Negative", priority="Low", date="2026-02-05", status="Addressed"),
        Feedback(id="FB-1014", customer_name="CloudScale Labs", content="General onboarding flow takes too many steps before reaching dashboard.", product_area="User Onboarding", sentiment="Negative", priority="Medium", date="2026-02-10", status="Addressed"),

        # Story 3: Notifications
        Feedback(id="FB-1020", customer_name="Apex Dynamics", content="Too many email notifications generated for every minor comment.", product_area="Notifications", sentiment="Negative", priority="High", date="2026-02-12", status="Addressed"),
        Feedback(id="FB-1021", customer_name="Acme Corp", content="Notification inbox clutter causes team members to turn off all alerts.", product_area="Notifications", sentiment="Negative", priority="High", date="2026-02-15", status="Addressed"),
        Feedback(id="FB-1022", customer_name="TechFlow Inc", content="Batch email digests would be preferred over real-time emails.", product_area="Notifications", sentiment="Neutral", priority="Medium", date="2026-02-20", status="Addressed"),
        Feedback(id="FB-1023", customer_name="Starlight Media", content="After notification frequency dropped, our team missed urgent mentions.", product_area="Notifications", sentiment="Negative", priority="High", date="2026-05-10", status="Open"),

        # Story 4: Billing
        Feedback(id="FB-1030", customer_name="DataWave", content="Billing information breakdown is confusing and invoice items lack clarity.", product_area="Billing & Payments", sentiment="Negative", priority="High", date="2026-02-28", status="Addressed"),
        Feedback(id="FB-1031", customer_name="CloudScale Labs", content="Prorated seat charges on monthly invoices are difficult to reconcile.", product_area="Billing & Payments", sentiment="Negative", priority="Medium", date="2026-03-02", status="Addressed"),
        Feedback(id="FB-1032", customer_name="Acme Corp", content="Support tickets spike at month-end due to unclear line items on bills.", product_area="Billing & Payments", sentiment="Negative", priority="High", date="2026-03-05", status="Addressed"),

        # Story 5: Data Export
        Feedback(id="FB-1040", customer_name="CloudScale Labs", content="Large data exports crash or time out with HTTP 504 Gateway Error.", product_area="Data Export", sentiment="Negative", priority="Critical", date="2026-03-10", status="Addressed"),
        Feedback(id="FB-1041", customer_name="Apex Dynamics", content="CSV data export for 50,000 records locks the web application.", product_area="Data Export", sentiment="Negative", priority="High", date="2026-03-12", status="Addressed"),
        Feedback(id="FB-1042", customer_name="Acme Corp", content="Exporting compliance audit logs takes over 90 seconds in browser.", product_area="Data Export", sentiment="Negative", priority="High", date="2026-03-15", status="Addressed"),

        # Additional domain feedback
        Feedback(id="FB-1050", customer_name="TechFlow Inc", content="Role-based permissions management requires granular sub-workspace roles.", product_area="Security & Access", sentiment="Neutral", priority="Medium", date="2026-03-20", status="Open"),
        Feedback(id="FB-1051", customer_name="Starlight Media", content="API rate limiting returns generic error without retry-after header.", product_area="Developer API", sentiment="Negative", priority="Low", date="2026-03-25", status="Open"),
        Feedback(id="FB-1052", customer_name="DataWave", content="Audit log retention export format should support JSON Lines.", product_area="Data Export", sentiment="Neutral", priority="Low", date="2026-04-01", status="Open"),
        Feedback(id="FB-1053", customer_name="Acme Corp", content="SSO SAML integration metadata reload button is missing.", product_area="Security & Access", sentiment="Neutral", priority="Medium", date="2026-04-10", status="Open"),
        Feedback(id="FB-1054", customer_name="CloudScale Labs", content="Dark mode high contrast borders needed on table headers.", product_area="UI / UX", sentiment="Neutral", priority="Low", date="2026-04-15", status="Addressed"),
        Feedback(id="FB-1055", customer_name="Apex Dynamics", content="Webhook event delivery retries need exponential backoff.", product_area="Developer API", sentiment="Negative", priority="Medium", date="2026-04-20", status="Open"),
        Feedback(id="FB-1056", customer_name="TechFlow Inc", content="Dashboard metric cards take 2 seconds to render on initial load.", product_area="Analytics Dashboard", sentiment="Negative", priority="Medium", date="2026-05-01", status="Open"),
        Feedback(id="FB-1057", customer_name="Starlight Media", content="CSV import field mapping auto-detect fails for custom date formats.", product_area="Data Export", sentiment="Negative", priority="Low", date="2026-05-15", status="Open"),
        Feedback(id="FB-1058", customer_name="DataWave", content="Session timeout modal logs users out while active in split view.", product_area="Security & Access", sentiment="Negative", priority="Medium", date="2026-06-01", status="Open"),
    ]
    for f in feedbacks:
        db.add(f)

    # Product Decisions (10 items)
    product_decisions = [
        ProductDecision(
            id="PD-101",
            title="Improve Search Relevance and Latency",
            problem="Customers report slow search response times and irrelevant search results across large workspace datasets.",
            context="Search is a core workflow for enterprise tier customers like Acme Corp and TechFlow.",
            options_considered=["Tune PostgreSQL Indexes & Queries", "Introduce Dedicated Elasticsearch Cluster", "Build Custom Ranking Microservice"],
            chosen_approach="Tune PostgreSQL Indexes & Queries",
            reason="Current data volume and operational team bandwidth do not justify introducing dedicated Elasticsearch cluster infrastructure.",
            expected_outcome="Reduce query latency under 300ms and improve search result relevance.",
            actual_outcome="Search latency decreased 42% after index tuning.",
            date="2026-01-18",
            status="Implemented",
            product_area="Search & Relevance",
            related_feedback_id="FB-1001"
        ),
        ProductDecision(
            id="PD-102",
            title="Simplify Onboarding Flow Architecture",
            problem="Customer complaints indicate high friction during initial workspace user setup.",
            context="Concentration of drop-offs observed in first three verification steps.",
            options_considered=["Complete Frontend & Backend Onboarding Rewrite", "Simplify Existing Onboarding Step Architecture", "Remove Verification Step Entirely"],
            chosen_approach="Simplify Existing Onboarding Step Architecture",
            reason="Broad redesign cost is unmotivated when complaints focus primarily on verification steps.",
            expected_outcome="Lower drop-off rates during initial team member invitation.",
            actual_outcome="General onboarding complaints decreased 34%, though verification complaints remained.",
            date="2026-01-20",
            status="Implemented",
            product_area="User Onboarding",
            related_feedback_id="FB-1010"
        ),
        ProductDecision(
            id="PD-103",
            title="Targeted Verification Flow Redesign",
            problem="General onboarding simplification reduced broad complaints, but verification complaints remained high.",
            context="Security tokens and SSO email handshakes created friction for enterprise gateways.",
            options_considered=["Targeted Verification Flow Redesign", "Remove Email Token Expiry"],
            chosen_approach="Targeted Verification Flow Redesign",
            reason="Addressing the specific root cause rather than re-architecting all onboarding steps.",
            expected_outcome="Eliminate token expiration issues for enterprise email gateways.",
            actual_outcome="Verification complaints decreased 41%.",
            date="2026-03-01",
            status="Implemented",
            product_area="User Onboarding",
            related_feedback_id="FB-1011"
        ),
        ProductDecision(
            id="PD-104",
            title="Reduce Notification Frequency Globally",
            problem="Customers expressed frustration over excessive email alert frequency.",
            context="High notification volume led to users opting out of all workspace alerts.",
            options_considered=["Global Notification Frequency Reduction", "User-Configurable Digest Matrix", "Disable Comments Email Alerts"],
            chosen_approach="Global Notification Frequency Reduction",
            reason="Fastest way to address user complaint spikes without complex settings UI.",
            expected_outcome="Dramatically lower opt-out rates.",
            actual_outcome="Opt-outs decreased significantly, but overall user daily engagement also slightly declined.",
            date="2026-02-18",
            status="Implemented",
            product_area="Notifications",
            related_feedback_id="FB-1020"
        ),
        ProductDecision(
            id="PD-105",
            title="Simplify Billing UI Presentation",
            problem="Customers reported confusion over monthly invoice itemization.",
            context="Support tickets spiked every billing cycle due to unclear prorated seat charges.",
            options_considered=["Rewrite Billing Engine Calculations", "Simplify Billing UI Presentation", "Automate Credit Issuance"],
            chosen_approach="Simplify Billing UI Presentation",
            reason="Calculation logic was mathematically correct; presentation clarity was the actual problem.",
            expected_outcome="Reduce billing-related support tickets by 50%.",
            actual_outcome="Billing support tickets decreased substantially without touching backend billing engine.",
            date="2026-03-08",
            status="Implemented",
            product_area="Billing & Payments",
            related_feedback_id="FB-1030"
        ),
        ProductDecision(
            id="PD-106",
            title="Asynchronous Data Export Processing",
            problem="Large data exports timed out synchronously on HTTP connections.",
            context="Enterprise datasets exceeding 50,000 rows caused gateway 504 errors.",
            options_considered=["Increase HTTP Timeout to 300s", "Asynchronous Background Jobs", "Paginated CSV Download Only"],
            chosen_approach="Asynchronous Background Jobs",
            reason="Non-blocking background processing isolates long-running queries from web API workers.",
            expected_outcome="Prevent HTTP 504 timeouts and improve API responsiveness.",
            actual_outcome="API responsiveness improved and export crashes eliminated.",
            date="2026-03-18",
            status="Implemented",
            product_area="Data Export",
            related_feedback_id="FB-1040"
        ),
        ProductDecision(
            id="PD-107",
            title="Granular Workspace Role Definitions",
            problem="Enterprise security teams demand fine-grained RBAC permissions.",
            context="Current Admin vs Member roles are too coarse for compliance.",
            options_considered=["Custom Role Permission Matrix", "Add Editor & Viewer Standard Roles"],
            chosen_approach="Add Editor & Viewer Standard Roles",
            reason="Fulfills 80% of compliance requirements with minimal architectural overhead.",
            expected_outcome="Satisfy enterprise compliance security audits.",
            actual_outcome="Accepted for Q3 roadmap.",
            date="2026-04-05",
            status="Accepted",
            product_area="Security & Access",
            related_feedback_id="FB-1050"
        ),
        ProductDecision(
            id="PD-108",
            title="Standardize Webhook Retry Policies",
            problem="Integrations fail silently when customer endpoints experience brief outages.",
            context="Developer API customers request explicit retry-after headers and backoff.",
            options_considered=["Implement Exponential Backoff Webhook Queue", "Rely on Customer Endpoints to Poll"],
            chosen_approach="Implement Exponential Backoff Webhook Queue",
            reason="Improves API reliability and developer trust.",
            expected_outcome="99.9% eventual webhook delivery success rate.",
            actual_outcome="Under development.",
            date="2026-04-25",
            status="Proposed",
            product_area="Developer API",
            related_feedback_id="FB-1055"
        ),
        ProductDecision(
            id="PD-109",
            title="Dashboard Metric Caching Optimization",
            problem="Dashboard metric aggregations slow down workspace home page load.",
            context="Analytics queries run expensive COUNT and SUM aggregations across all historical records.",
            options_considered=["Redis Pre-aggregated Hourly Metrics", "Materialized Database Views"],
            chosen_approach="Redis Pre-aggregated Hourly Metrics",
            reason="Sub-millisecond read latency for home page dashboard widgets.",
            expected_outcome="Dashboard render time under 100ms.",
            actual_outcome="Dashboard render latency dropped from 2.1s to 45ms.",
            date="2026-05-10",
            status="Implemented",
            product_area="Analytics Dashboard",
            related_feedback_id="FB-1056"
        ),
        ProductDecision(
            id="PD-110",
            title="Custom Date Format Auto-Detection",
            problem="Data import fails when customers upload non-ISO formatted date strings in CSV files.",
            context="Import tool returns generic parse error on DD/MM/YYYY inputs.",
            options_considered=["Build Smart Date Parser Middleware", "Require ISO-8601 Format Strictly"],
            chosen_approach="Build Smart Date Parser Middleware",
            reason="Improves user self-service data migration success.",
            expected_outcome="Zero CSV date parsing support tickets.",
            actual_outcome="Under review.",
            date="2026-05-20",
            status="Under Review",
            product_area="Data Export",
            related_feedback_id="FB-1057"
        )
    ]
    for pd in product_decisions:
        db.add(pd)

    # Engineering Decisions (15 ADRs)
    engineering_decisions = [
        EngineeringDecision(
            id="ED-201",
            title="Use PostgreSQL for Search Optimization",
            problem="Search latency and relevance were becoming major customer satisfaction issues.",
            context="Dataset size was moderate (approx 500k records) and operational simplicity was top priority.",
            decision="Optimize PostgreSQL using gin indexes, pg_trgm, and tsvector query improvements.",
            alternatives_considered=["Elasticsearch", "OpenSearch", "Custom Search Microservice"],
            rejected_alternatives=[
                {"name": "Elasticsearch", "reason_rejected": "Current scale and operational complexity did not justify managing an external search cluster."},
                {"name": "OpenSearch", "reason_rejected": "Infrastructure management overhead exceeded benefits for current 500k row scale."},
                {"name": "Custom Search Microservice", "reason_rejected": "High maintenance debt and duplicated datastore state."}
            ],
            constraints="Must keep operational infrastructure simple without adding dedicated cluster management overhead.",
            trade_offs="Lower infrastructure complexity vs less specialized full-text ranking algorithms.",
            expected_consequences="Improved search performance without introducing secondary infrastructure dependencies.",
            actual_consequences="Search latency decreased 42%. PostgreSQL optimization proved sufficient for current workload.",
            technology="PostgreSQL",
            architecture_area="Search & Storage",
            date="2026-02-12",
            status="Accepted",
            related_product_decision_id="PD-101",
            related_feedback_id="FB-1001"
        ),
        EngineeringDecision(
            id="ED-202",
            title="Reuse Existing Frontend Architecture for Onboarding",
            problem="Onboarding complaints required UI changes to reduce step friction.",
            context="Proposal was made to rewrite the onboarding flow using a new micro-frontend framework.",
            decision="Improve the existing React frontend architecture instead of introducing a new framework.",
            alternatives_considered=["Micro-frontend Framework Rewrite", "Refactor Existing React Flow Component"],
            rejected_alternatives=[
                {"name": "Micro-frontend Framework Rewrite", "reason_rejected": "Migration cost and build tool complexity were not justified by expected user benefit."}
            ],
            constraints="Engineering team velocity and avoiding code fragment duplication.",
            trade_offs="Faster delivery time vs maintaining legacy state machine code.",
            expected_consequences="Rapid deployment of onboarding UX fixes.",
            actual_consequences="Onboarding fixes delivered 3 weeks faster than estimated rewrite.",
            technology="React / Next.js",
            architecture_area="Frontend Architecture",
            date="2026-01-25",
            status="Accepted",
            related_product_decision_id="PD-102",
            related_feedback_id="FB-1010"
        ),
        EngineeringDecision(
            id="ED-203",
            title="Implement Dedicated Identity Verification Service Handler",
            problem="General onboarding redesign left verification step token expiry issues unresolved.",
            context="Enterprise email security gateways pre-fetched email verification URLs, invalidating single-use tokens.",
            decision="Create a 2-step verification handler with explicit confirmation button rather than instant token consumption on HTTP GET.",
            alternatives_considered=["Instant GET Token Consumption", "2-Step Interactive Verification Page"],
            rejected_alternatives=[
                {"name": "Instant GET Token Consumption", "reason_rejected": "Security scanners pre-fetch GET links and invalidate tokens before users open emails."}
            ],
            constraints="Must remain compliant with strict enterprise email security policies.",
            trade_offs="One extra click for user vs 0% premature token invalidation by email security filters.",
            expected_consequences="Verification complaints drop to near zero.",
            actual_consequences="Verification complaints decreased 41%.",
            technology="FastAPI",
            architecture_area="Authentication & Identity",
            date="2026-03-05",
            status="Accepted",
            related_product_decision_id="PD-103",
            related_feedback_id="FB-1011"
        ),
        EngineeringDecision(
            id="ED-204",
            title="Configurable Notification Frequency Engine",
            problem="Global frequency reduction lowered opt-outs but slightly lowered user engagement.",
            decision="Implement user-configurable notification frequency matrices with Redis rate-limiting.",
            alternatives_considered=["Hardcoded Global Delay", "Redis Rate-Limited Digest Queue"],
            rejected_alternatives=[
                {"name": "Hardcoded Global Delay", "reason_rejected": "Created trade-off where urgent mentions were delayed inappropriately."}
            ],
            constraints="Must prevent notification spam while preserving urgent mention delivery.",
            trade_offs="Increased backend setting state vs balanced user experience.",
            expected_consequences="Flexible user notification preferences.",
            actual_consequences="Opt-outs stayed low while engagement recovered.",
            technology="Redis",
            architecture_area="Notification Pipeline",
            date="2026-02-25",
            status="Accepted",
            related_product_decision_id="PD-104",
            related_feedback_id="FB-1020"
        ),
        EngineeringDecision(
            id="ED-205",
            title="Keep Billing Calculation Logic Unchanged & Enhance Presentation Layer",
            problem="Billing support tickets spiked due to invoice line item confusion.",
            context="Engineering evaluated rewriting the core financial calculation engine.",
            decision="Keep backend billing engine untouched and build an improved invoice presentation formatter in API response layer.",
            alternatives_considered=["Rewrite Billing Calculation Engine", "API Presentation Formatter Layer"],
            rejected_alternatives=[
                {"name": "Rewrite Billing Calculation Engine", "reason_rejected": "Risk of introducing financial calculation regressions was high, whereas existing math was accurate."}
            ],
            constraints="Zero risk tolerance for financial calculation bugs.",
            trade_offs="Formatting logic in API layer vs risky backend engine rewrite.",
            expected_consequences="Clear invoice breakdowns with zero risk to ledger math.",
            actual_consequences="Billing support tickets decreased substantially.",
            technology="FastAPI",
            architecture_area="Billing & Ledger",
            date="2026-03-12",
            status="Accepted",
            related_product_decision_id="PD-105",
            related_feedback_id="FB-1030"
        ),
        EngineeringDecision(
            id="ED-206",
            title="Use Background Workers for Large Data Exports",
            problem="Synchronous HTTP exports timed out on dataset queries over 50,000 rows.",
            context="Enterprise customers required CSV/JSON exports for compliance reporting.",
            decision="Offload data export generation to background worker pool using Celery/Redis queue and send pre-signed S3 download links.",
            alternatives_considered=["Synchronous API Stream", "Background Jobs with S3 Pre-signed Links"],
            rejected_alternatives=[
                {"name": "Synchronous API Stream", "reason_rejected": "API worker process memory lockup and HTTP gateway 504 timeouts."}
            ],
            constraints="Prevent HTTP thread blocking and memory bloat on main API servers.",
            trade_offs="Asynchronous user flow (delay in download) vs rock-solid API stability.",
            expected_consequences="100% export completion rate without API worker timeouts.",
            actual_consequences="API responsiveness improved and 504 timeouts were eliminated.",
            technology="Background Workers",
            architecture_area="Data Pipeline",
            date="2026-03-22",
            status="Accepted",
            related_product_decision_id="PD-106",
            related_feedback_id="FB-1040"
        ),
        EngineeringDecision(
            id="ED-207",
            title="PostgreSQL Relational Storage for Architecture & Decision Memory",
            problem="Selecting primary database for core Decision Memory relational state.",
            context="Evaluated MongoDB vs PostgreSQL for decision state storage.",
            decision="Select PostgreSQL because transactional consistency, relational integrity, and existing team operational expertise were paramount.",
            alternatives_considered=["MongoDB", "PostgreSQL", "DynamoDB"],
            rejected_alternatives=[
                {"name": "MongoDB", "reason_rejected": "Lack of relational foreign keys and lower ACID guarantees for interconnected decision records."}
            ],
            constraints="Relational consistency across linked entities (Feedback -> Decision -> Outcome).",
            trade_offs="Rigid relational schema vs guaranteed data integrity.",
            expected_consequences="Clean relational mapping and fast indexed queries.",
            actual_consequences="Zero schema drift or orphaned records.",
            technology="PostgreSQL",
            architecture_area="Core Storage",
            date="2026-01-08",
            status="Accepted",
            related_product_decision_id=None,
            related_feedback_id=None
        ),
        EngineeringDecision(
            id="ED-208",
            title="REST API for Backend Service Interfaces",
            problem="Choosing API interface style between REST OpenAPI vs GraphQL.",
            decision="Adopt REST API with FastAPI and Pydantic validation.",
            alternatives_considered=["GraphQL", "REST OpenAPI"],
            rejected_alternatives=[
                {"name": "GraphQL", "reason_rejected": "Overhead of schema resolvers and query complexity management not required for predictable SaaS views."}
            ],
            constraints="Team familiarity, fast development velocity, automatic OpenAPI doc generation.",
            trade_offs="Multiple endpoint roundtrips vs simple cacheability and typed contracts.",
            expected_consequences="Rapid frontend integration and OpenAPI compatibility.",
            actual_consequences="Backend API completed ahead of schedule.",
            technology="FastAPI",
            architecture_area="API Gateway",
            date="2026-01-10",
            status="Accepted"
        ),
        EngineeringDecision(
            id="ED-209",
            title="Redis Caching Layer for Workspace Session & Rate Limiting",
            problem="Database queries for session verification and API rate limits added latency to every HTTP request.",
            decision="Implement Redis in-memory cache for API authentication tokens and rate limits.",
            alternatives_considered=["Database-only Authentication", "In-memory Application Process Cache", "Redis Centralized Cache"],
            rejected_alternatives=[
                {"name": "Database-only Authentication", "reason_rejected": "Caused 15ms database latency hit per API request."},
                {"name": "In-memory Application Process Cache", "reason_rejected": "State was not shared across load-balanced FastAPI instances."}
            ],
            constraints="Low latency authentication check (<2ms).",
            trade_offs="Managing Redis memory lifecycle vs database query pressure reduction.",
            expected_consequences="API authentication overhead reduced to under 1.5ms.",
            actual_consequences="API response time decreased by 18ms across all routes.",
            technology="Redis",
            architecture_area="Caching & Auth",
            date="2026-02-02",
            status="Accepted"
        ),
        EngineeringDecision(
            id="ED-210",
            title="Strict OpenAPI Pydantic Data Contract Validation",
            problem="Preventing malformed JSON payloads from reaching backend domain services.",
            decision="Enforce strict Pydantic V2 schemas on all incoming request bodies.",
            alternatives_considered=["Manual Dictionary Parsing", "Strict Pydantic Validation"],
            rejected_alternatives=[
                {"name": "Manual Dictionary Parsing", "reason_rejected": "Prone to KeyError exceptions and inconsistent error messaging."}
            ],
            constraints="Zero unhandled 500 exceptions due to type errors.",
            trade_offs="Slight payload validation overhead vs application stability.",
            expected_consequences="Clean HTTP 422 error messages for invalid input.",
            actual_consequences="Eliminated 95% of invalid input backend exceptions.",
            technology="FastAPI",
            architecture_area="API Gateway",
            date="2026-02-14",
            status="Accepted"
        ),
        EngineeringDecision(
            id="ED-211",
            title="Decoupled Hindsight Memory Service Integration",
            problem="Ensuring application reliability when external vector/memory API services experience latency.",
            decision="Wrap Hindsight Cloud calls in an asynchronous resilient proxy client with local PostgreSQL experience store fallback.",
            alternatives_considered=["Direct Synchronous Hindsight SDK Calls", "Resilient Proxy Client with Local Fallback"],
            rejected_alternatives=[
                {"name": "Direct Synchronous Hindsight SDK Calls", "reason_rejected": "Network issues with external cloud API would block user UI actions."}
            ],
            constraints="Application must remain 100% functional even if external memory services are unreachable.",
            trade_offs="Dual write logic vs guaranteed high availability.",
            expected_consequences="Zero downtime during network partitions.",
            actual_consequences="App operated seamlessly during simulated Hindsight API outages.",
            technology="FastAPI",
            architecture_area="Memory Subsystem",
            date="2026-02-28",
            status="Accepted"
        ),
        EngineeringDecision(
            id="ED-212",
            title="Database Connection Pooling with SQLAlchemy QueuePool",
            problem="High traffic concurrency caused database connection exhaustion errors.",
            decision="Configure SQLAlchemy QueuePool with pool_size=20, max_overflow=10, and pool_recycle=3600.",
            alternatives_considered=["NullPool (Connection per request)", "QueuePool with recycling"],
            rejected_alternatives=[
                {"name": "NullPool", "reason_rejected": "High TCP connection establishment latency."}
            ],
            constraints="Handle 200 concurrent requests without connection timeout.",
            trade_offs="Persistent database memory allocation vs instantaneous connection acquisition.",
            expected_consequences="Stable connection acquisition under burst load.",
            actual_consequences="Zero connection pool exhaustion errors recorded.",
            technology="PostgreSQL",
            architecture_area="Core Storage",
            date="2026-03-15",
            status="Accepted"
        ),
        EngineeringDecision(
            id="ED-213",
            title="JSONB Column Types for Flexible Alternative Options",
            problem="Storing dynamic decision metadata and rejected alternatives without creating 10 normalized tables.",
            decision="Use SQLAlchemy JSON/JSONB column types for options_considered, rejected_alternatives, and related_decisions.",
            alternatives_considered=["Separate Normalized Entity Tables", "JSON/JSONB Document Columns"],
            rejected_alternatives=[
                {"name": "Separate Normalized Entity Tables", "reason_rejected": "Excessive SQL joins for simple array lookups."}
            ],
            constraints="Simple schema maintenance for unstructured decision context.",
            trade_offs="Less strict SQL relational enforcement vs high schema flexibility.",
            expected_consequences="Faster iteration when adding metadata fields.",
            actual_consequences="Simplified ADR creation API codebase.",
            technology="PostgreSQL",
            architecture_area="Core Storage",
            date="2026-03-30",
            status="Accepted"
        ),
        EngineeringDecision(
            id="ED-214",
            title="Shadcn UI & Tailwind CSS Design Token Standard",
            problem="Inconsistent UI styling and slow component development velocity.",
            decision="Adopt strict Tailwind CSS design system tokens with custom high-contrast dark mode colors.",
            alternatives_considered=["Styled Components", "Tailwind CSS Design Tokens"],
            rejected_alternatives=[
                {"name": "Styled Components", "reason_rejected": "Runtime CSS-in-JS performance penalty on large component trees."}
            ],
            constraints="Fast render times and clean, cohesive enterprise B2B visual identity.",
            trade_offs="Utility class verbosity vs zero runtime CSS generation cost.",
            expected_consequences="Consistent UI across all screens.",
            actual_consequences="UI build completed efficiently with clean design tokens.",
            technology="React / Next.js",
            architecture_area="Frontend Architecture",
            date="2026-04-10",
            status="Accepted"
        ),
        EngineeringDecision(
            id="ED-215",
            title="Groq LLM Integration with Fallback Grounding Engine",
            problem="Dependence on LLM API availability for decision intelligence recommendations.",
            decision="Integrate Groq API for rapid JSON structured recommendations with a rule-based grounded fallback engine.",
            alternatives_considered=["Pure LLM API dependency", "Groq LLM + Grounded Rule Engine Fallback"],
            rejected_alternatives=[
                {"name": "Pure LLM API dependency", "reason_rejected": "API rate limits or outages would break AI Advisor feature."}
            ],
            constraints="Always return grounded, accurate answers without hallucination.",
            trade_offs="Secondary fallback implementation maintenance vs 100% uptime.",
            expected_consequences="Zero AI feature outages for end users.",
            actual_consequences="Maintained 100% advisor uptime during LLM provider rate limit spikes.",
            technology="FastAPI",
            architecture_area="AI Subsystem",
            date="2026-04-20",
            status="Accepted"
        )
    ]
    for ed in engineering_decisions:
        db.add(ed)

    # Architecture Decisions (8 items)
    arch_decisions = [
        ArchitectureDecision(
            id="AD-301",
            title="PostgreSQL vs MongoDB for Organizational Memory",
            status="Accepted",
            date="2026-01-08",
            technology="PostgreSQL",
            problem="Choosing primary database paradigm for Decision Memory application.",
            context="Application requires strong relationships between feedback, decisions, and outcomes.",
            constraints="ACID transactions, relational queries, team SQL expertise.",
            options=["PostgreSQL", "MongoDB", "CockroachDB"],
            decision="Select PostgreSQL for relational consistency and pgvector support.",
            trade_offs="Rigid schema migration requirements vs data consistency.",
            consequences="Simplified relational modeling for connected decision graphs.",
            related_decisions=["ED-207"]
        ),
        ArchitectureDecision(
            id="AD-302",
            title="REST vs GraphQL for Decision Memory API",
            status="Accepted",
            date="2026-01-10",
            technology="FastAPI",
            problem="Selecting web API architecture style.",
            context="Frontend application requires predictable, typed endpoints for dashboards and decision records.",
            constraints="Fast implementation, OpenAPI specification generation.",
            options=["REST OpenAPI", "GraphQL"],
            decision="Adopt REST API with OpenAPI specifications.",
            trade_offs="Multiple HTTP endpoints vs query resolver overhead.",
            consequences="Clear typed contracts between Next.js and FastAPI.",
            related_decisions=["ED-208"]
        ),
        ArchitectureDecision(
            id="AD-303",
            title="Synchronous Data Exports vs Background Jobs",
            status="Accepted",
            date="2026-03-22",
            technology="Background Workers",
            problem="Data exports over 50,000 rows timed out synchronous HTTP requests.",
            context="Heavy SQL aggregation locked database connections and triggered HTTP 504 gateway timeouts.",
            constraints="Non-blocking HTTP web workers.",
            options=["Synchronous API Response", "Background Worker Jobs", "Streaming HTTP Chunked Response"],
            decision="Offload large export generation to asynchronous background worker pool.",
            trade_offs="Asynchronous user polling flow vs web server stability.",
            consequences="Eliminated HTTP timeouts and improved overall API responsiveness.",
            related_decisions=["ED-206", "PD-106"]
        ),
        ArchitectureDecision(
            id="AD-304",
            title="PostgreSQL Search vs Elasticsearch Cluster",
            status="Accepted",
            date="2026-02-12",
            technology="PostgreSQL",
            problem="Search latency and relevance complaints on workspace search.",
            context="Evaluated introducing a dedicated Elasticsearch cluster vs optimizing PostgreSQL.",
            constraints="Infrastructure operational simplicity.",
            options=["PostgreSQL GIN/trgm Optimization", "Elasticsearch Cluster", "OpenSearch"],
            decision="Optimize PostgreSQL search using GIN indexes and query tuning.",
            trade_offs="Lower infrastructure overhead vs specialized search capabilities.",
            consequences="Search latency dropped 42%. Deferred Elasticsearch cluster deployment.",
            related_decisions=["ED-201", "PD-101"]
        ),
        ArchitectureDecision(
            id="AD-305",
            title="Redis Caching vs Database-only Caching",
            status="Accepted",
            date="2026-02-02",
            technology="Redis",
            problem="High database load from token authentication checks on every API request.",
            context="Database query latency added 15ms overhead to every API request.",
            constraints="Sub-2ms token validation latency.",
            options=["Redis In-Memory Cache", "Database Query Caching", "In-Process Python Dict"],
            decision="Deploy Redis cache cluster for session verification and rate limiting.",
            trade_offs="Managing cache invalidation vs database load reduction.",
            consequences="Reduced API authentication latency to 1.4ms.",
            related_decisions=["ED-209"]
        ),
        ArchitectureDecision(
            id="AD-306",
            title="Biomimetic Retain/Recall/Reflect Memory Architecture",
            status="Accepted",
            date="2026-02-28",
            technology="Hindsight by Vectorize",
            problem="Standard RAG vector stores lack temporal reasoning and graph entity relationships for organizational memory.",
            context="Decision memory requires remembering WHY decisions were made, rejected alternatives, and actual outcomes over time.",
            constraints="Temporal awareness, entity graph traversal, agentic synthesis.",
            options=["Hindsight Memory Engine", "Generic Vector Store (Pinecone/Weaviate)", "Simple Chat Log DB"],
            decision="Adopt Hindsight by Vectorize for retain, recall, and reflect memory primitives.",
            trade_offs="Integrating specialized memory API vs basic vector search.",
            consequences="Agent recalls historical context, trade-offs, and outcomes to alter future recommendations.",
            related_decisions=["ED-211"]
        ),
        ArchitectureDecision(
            id="AD-307",
            title="Decoupled Microservices vs Modular Monolith Backend",
            status="Accepted",
            date="2026-01-05",
            technology="FastAPI",
            problem="Determining backend architecture pattern for early stage decision SaaS.",
            context="Evaluated splitting into separate Auth, Search, and Memory microservices vs single clean FastAPI monolith.",
            constraints="Development speed, operational simplicity, single deployment unit.",
            options=["Modular Monolith", "Microservices Architecture"],
            decision="Build as a clean Modular Monolith in FastAPI.",
            trade_offs="Single point of deployment vs zero inter-service network RPC overhead.",
            consequences="Fast developer iteration and straightforward deployment.",
            related_decisions=["ED-208"]
        ),
        ArchitectureDecision(
            id="AD-308",
            title="Client-Side State Management vs Server Components",
            status="Accepted",
            date="2026-01-15",
            technology="React / Next.js",
            problem="Structuring Next.js frontend state management for decision records and advisor interface.",
            context="Application requires responsive interactive tables, modals, and evidence drawer views.",
            constraints="Smooth UI transitions and fast page navigation.",
            options=["Next.js App Router with Client State Layer", "Redux Toolkit", "Pure Server Components"],
            decision="Use Next.js App Router with clean API client layer and React local component state.",
            trade_offs="Client-side fetch management vs ultra-responsive interactive UI feedback.",
            consequences="Modular UI components with instantaneous filter/tab switches.",
            related_decisions=["ED-214"]
        )
    ]
    for ad in arch_decisions:
        db.add(ad)

    # Experiments (8 items)
    experiments = [
        Experiment(
            id="EXP-501",
            name="Reduced Notification Frequency Experiment",
            product_area="Notifications",
            hypothesis="Reducing default notification email frequency will decrease user opt-outs without lowering daily active usage.",
            variant_a="Default real-time notification emails for all activity",
            variant_b="Batched daily digest notifications with real-time delivery only for direct user @mentions",
            start_date="2026-02-01",
            end_date="2026-02-15",
            result="Opt-outs decreased by 48%. However, overall daily active engagement declined by 6%.",
            conclusion="Reducing notification frequency lowered opt-outs but also slightly reduced engagement. Future notification changes should implement targeted frequency rules rather than globally changing notification frequency.",
            status="Completed"
        ),
        Experiment(
            id="EXP-502",
            name="Simplified 2-Step Onboarding Checkbox Flow",
            product_area="User Onboarding",
            hypothesis="Grouping setup tasks into 2 key steps will increase onboarding completion within 24 hours.",
            variant_a="5-step linear onboarding wizard",
            variant_b="2-step interactive onboarding card checklist",
            start_date="2026-01-22",
            end_date="2026-02-05",
            result="Onboarding completion within 24 hours increased by 34%.",
            conclusion="Simplifying general onboarding steps reduced friction for standard setup tasks. Verification step remained a separate bottleneck.",
            status="Completed"
        ),
        Experiment(
            id="EXP-503",
            name="PostgreSQL Query Index Tuning vs Baseline",
            product_area="Search & Relevance",
            hypothesis="Adding GIN trgm indexes to title and body text columns will reduce search query latency under 300ms.",
            variant_a="Unindexed SQL LIKE queries",
            variant_b="GIN trgm indexed tsvector full text search",
            start_date="2026-02-05",
            end_date="2026-02-12",
            result="Average search query latency dropped from 480ms to 278ms (42% improvement).",
            conclusion="PostgreSQL search optimization achieved performance target, making Elasticsearch adoption unnecessary at present scale.",
            status="Completed"
        ),
        Experiment(
            id="EXP-504",
            name="Billing Invoice Itemization Redesign",
            product_area="Billing & Payments",
            hypothesis="Providing explicit visual line-item breakdowns on monthly invoices will reduce billing support ticket volume.",
            variant_a="Legacy aggregated monthly invoice PDF",
            variant_b="Interactive visual invoice breakdown UI with prorated seat history tooltips",
            start_date="2026-03-01",
            end_date="2026-03-15",
            result="Billing support tickets decreased by 62% during month-end billing cycle.",
            conclusion="Presentation clarity solved customer confusion. Billing engine backend calculation logic did not require rewriting.",
            status="Completed"
        ),
        Experiment(
            id="EXP-505",
            name="Asynchronous File Export Worker Pool",
            product_area="Data Export",
            hypothesis="Offloading CSV generation to background queue will eliminate HTTP 504 timeouts on datasets > 50,000 rows.",
            variant_a="Synchronous HTTP streaming download",
            variant_b="Celery background job worker with pre-signed S3 download link",
            start_date="2026-03-15",
            end_date="2026-03-22",
            result="Zero HTTP 504 timeouts recorded across 1,200 large export requests.",
            conclusion="Background job processing solved API gateway timeout issues permanently.",
            status="Completed"
        ),
        Experiment(
            id="EXP-506",
            name="Granular Role Permission Matrix Test",
            product_area="Security & Access",
            hypothesis="Offering explicit 'Editor' and 'Viewer' roles will increase enterprise team seat expansion.",
            variant_a="Admin & Member roles only",
            variant_b="Admin, Editor, Viewer, and Billing Manager roles",
            start_date="2026-04-01",
            end_date="2026-04-15",
            result="Enterprise account seat growth increased 18% in test cohort.",
            conclusion="Granular roles unblocked enterprise IT approval.",
            status="Completed"
        ),
        Experiment(
            id="EXP-507",
            name="Redis Home Dashboard Widget Caching",
            product_area="Analytics Dashboard",
            hypothesis="Caching dashboard metric queries in Redis will improve page load speed.",
            variant_a="Direct SQL database query on page load",
            variant_b="1-hour TTL Redis metric cache with background refresh",
            start_date="2026-05-01",
            end_date="2026-05-08",
            result="Dashboard load time dropped from 2.1s to 45ms.",
            conclusion="Redis caching eliminated home page database latency.",
            status="Completed"
        ),
        Experiment(
            id="EXP-508",
            name="Interactive Decision Evidence Drawer UI",
            product_area="UI / UX",
            hypothesis="Displaying explicit historical evidence cards in AI Advisor drawer increases decision confidence scores.",
            variant_a="Text-only AI recommendation answer",
            variant_b="Structured evidence cards showing historical decisions, rejected options, and outcomes",
            start_date="2026-05-15",
            end_date="2026-05-30",
            result="User trust rating for recommendations increased from 64% to 92%.",
            conclusion="Exposing evidence transparency fundamentally increases enterprise decision adoption.",
            status="Completed"
        )
    ]
    for exp in experiments:
        db.add(exp)

    # Outcomes (15 items)
    outcomes = [
        Outcome(id="OUT-201", title="PostgreSQL Search Latency Reduction", description="After PostgreSQL search optimization using GIN trgm indexes, search query response times decreased 42% across all enterprise accounts.", category="Technical Latency", metrics_impact="-42% Search Latency", date="2026-04-04", related_decision_type="EngineeringDecision", related_decision_id="ED-201"),
        Outcome(id="OUT-202", title="General Onboarding Complaint Decrease", description="Simplifying onboarding steps reduced general setup complaints by 34%, but verification token issues remained concentrated in enterprise accounts.", category="User Satisfaction", metrics_impact="-34% General Complaints", date="2026-02-15", related_decision_type="ProductDecision", related_decision_id="PD-102"),
        Outcome(id="OUT-203", title="Verification Drop-off Elimination", description="Targeted identity verification flow overhaul eliminated email token expiration errors for enterprise security gateways.", category="User Satisfaction", metrics_impact="-41% Verification Complaints", date="2026-03-18", related_decision_type="EngineeringDecision", related_decision_id="ED-203"),
        Outcome(id="OUT-204", title="Notification Opt-Out Reduction", description="Global notification frequency reduction lowered user email opt-out rates by 48%.", category="User Retention & Support", metrics_impact="-48% Opt-out Rate", date="2026-03-01", related_decision_type="ProductDecision", related_decision_id="PD-104"),
        Outcome(id="OUT-205", title="Notification Engagement Trade-Off", description="While opt-outs decreased, daily active user comment engagement also declined by 6%, prompting a shift to user-configurable frequency matrices.", category="Product Performance", metrics_impact="-6% Daily Engagement", date="2026-03-10", related_decision_type="Experiment", related_decision_id="EXP-501"),
        Outcome(id="OUT-206", title="Billing Support Ticket Drop", description="Redesigning billing invoice presentation UI without modifying backend calculation logic reduced billing support tickets substantially.", category="User Retention & Support", metrics_impact="-62% Billing Support Tickets", date="2026-03-25", related_decision_type="ProductDecision", related_decision_id="PD-105"),
        Outcome(id="OUT-207", title="API Timeout Elimination for Data Exports", description="Offloading large data exports to Celery background workers eliminated HTTP 504 gateway timeouts for exports > 50,000 rows.", category="Technical Latency", metrics_impact="0 HTTP 504 Timeouts", date="2026-04-01", related_decision_type="EngineeringDecision", related_decision_id="ED-206"),
        Outcome(id="OUT-208", title="Dashboard Latency Acceleration", description="Implementing Redis hourly caching for analytics dashboard widgets reduced home page load latency from 2.1s to 45ms.", category="Technical Latency", metrics_impact="-97% Dashboard Latency", date="2026-05-12", related_decision_type="EngineeringDecision", related_decision_id="ED-209"),
        Outcome(id="OUT-209", title="Enterprise Seat Expansion", description="Adding explicit Editor and Viewer RBAC roles resulted in an 18% increase in enterprise seat licenses.", category="Product Performance", metrics_impact="+18% Enterprise Seats", date="2026-04-20", related_decision_type="Experiment", related_decision_id="EXP-506"),
        Outcome(id="OUT-210", title="Zero Database Scheme Drift", description="Adopting PostgreSQL strict relational modeling prevented data orphaned records across decisions and outcomes.", category="Operational Cost", metrics_impact="100% Data Integrity", date="2026-02-01", related_decision_type="EngineeringDecision", related_decision_id="ED-207"),
        Outcome(id="OUT-211", title="Rapid Onboarding UX Fix Delivery", description="Reusing existing React frontend architecture allowed delivering onboarding fixes 3 weeks ahead of rewrite estimates.", category="Developer Productivity", metrics_impact="3 Weeks Saved", date="2026-02-05", related_decision_type="EngineeringDecision", related_decision_id="ED-202"),
        Outcome(id="OUT-212", title="Zero Unhandled Payload Backend Exceptions", description="Strict Pydantic schema validation eliminated 95% of invalid input backend crash logs.", category="Technical Latency", metrics_impact="-95% Invalid Input Errors", date="2026-02-20", related_decision_type="EngineeringDecision", related_decision_id="ED-210"),
        Outcome(id="OUT-213", title="High Availability During Hindsight Outages", description="Decoupled resilient proxy architecture ensured 100% app availability during simulated memory cloud API downtime.", category="Operational Cost", metrics_impact="100% App Uptime", date="2026-03-05", related_decision_type="EngineeringDecision", related_decision_id="ED-211"),
        Outcome(id="OUT-214", title="Zero Database Pool Exhaustion", description="SQLAlchemy QueuePool tuning handled 200 concurrent requests without timeout spikes.", category="Technical Latency", metrics_impact="0 Pool Exhaustions", date="2026-03-28", related_decision_type="EngineeringDecision", related_decision_id="ED-212"),
        Outcome(id="OUT-215", title="Increased Decision Advisor User Trust", description="Exposing transparent historical evidence cards increased AI Advisor recommendation user trust rating to 92%.", category="User Satisfaction", metrics_impact="92% User Trust", date="2026-06-01", related_decision_type="Experiment", related_decision_id="EXP-508")
    ]
    for o in outcomes:
        db.add(o)

    db.commit()

    # Now retain all meaningful experiences in Hindsight & MemoryEvent table
    logger.info("Retaining experiences in Hindsight Memory Bank & PostgreSQL MemoryEvent index...")

    for f in db.query(Feedback).all():
        memory_manager.retain_feedback_experience(db, f)

    for pd in db.query(ProductDecision).all():
        memory_manager.retain_product_decision_experience(db, pd)

    for ed in db.query(EngineeringDecision).all():
        memory_manager.retain_engineering_decision_experience(db, ed)

    for out in db.query(Outcome).all():
        memory_manager.retain_outcome_experience(db, out)

    total_mem = db.query(MemoryEvent).count()
    logger.info(f"Successfully seeded demo data! Created {len(feedbacks)} Feedback, {len(product_decisions)} Product Decisions, {len(engineering_decisions)} Engineering Decisions, {len(arch_decisions)} Architecture Decisions, {len(experiments)} Experiments, {len(outcomes)} Outcomes, and retained {total_mem} Memory Events.")

    return {
        "status": "success",
        "feedback_count": len(feedbacks),
        "product_decisions_count": len(product_decisions),
        "engineering_decisions_count": len(engineering_decisions),
        "architecture_decisions_count": len(arch_decisions),
        "experiments_count": len(experiments),
        "outcomes_count": len(outcomes),
        "retained_memory_events_count": total_mem
    }
