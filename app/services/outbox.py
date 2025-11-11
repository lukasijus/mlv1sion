# app/services/outbox.py (conceptual code for outbox pattern)
async def append_outbox(db, agg_type, agg_id, payload):
    out = Outbox(aggregate_type=agg_type, aggregate_id=agg_id, payload=payload)
    db.add(out)
    await db.commit()  # still inside same unit of work in real flow


def dispatch_outbox(db, pubsub_client):
    rows = db.query(Outbox).filter_by(dispatched=False).limit(100).all()
    for r in rows:
        pubsub_client.publish(
            topic=f"{r.aggregate_type}.{r.aggregate_id}", message=r.payload
        )
        r.dispatched = True
    db.commit()
