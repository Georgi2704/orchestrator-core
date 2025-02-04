from more_itertools import first

from orchestrator.db import ProcessTable


def show_process(p: ProcessTable) -> dict:
    subscription = first(p.subscriptions, None)
    if subscription:
        product_id = subscription.product_id
        customer_id = subscription.customer_id
    else:
        product_id = None
        customer_id = None

    return {
        "id": p.pid,
        "workflow_name": p.workflow,
        "product": product_id,
        "customer": customer_id,
        "assignee": p.assignee,
        "status": p.last_status,
        "failed_reason": p.failed_reason,
        "traceback": p.traceback,
        "step": p.last_step,
        "created_by": p.created_by,
        "started": p.started_at,
        "last_modified": p.last_modified_at,
        "subscriptions": [
            # explicit conversion using excluded_keys to prevent eager loaded subscriptions (when loaded for form domain models)
            # to cause circular reference errors
            s.subscription.__json__(excluded_keys={"instances", "customer_descriptions", "processes", "product"})
            for s in p.process_subscriptions
        ],
        "is_task": p.is_task,
    }
