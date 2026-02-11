# backend/services/security/audit.py
async def log_action(user_id, action, resource_id, details):
    entry = AuditLog(
        timestamp=datetime.utcnow(),
        user_id=user_id,
        action=action,
        resource_id=resource_id,
        details=details,
        ip_address=request.client.host
    )
    db.add(entry)
    db.commit()
