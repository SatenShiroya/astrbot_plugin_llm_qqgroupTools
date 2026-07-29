def unwrap_event(event):
    """Return the real AstrBot message event from either an event or ContextWrapper.

    AstrBot v4.26+ may pass a ContextWrapper into LLM tools. The actual
    message event is stored at ``context.event``; older versions pass the
    event directly.
    """
    return getattr(getattr(event, "context", None), "event", event)
