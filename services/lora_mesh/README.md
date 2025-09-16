# LoRa Mesh Voice Store & Forward

- **Clip cap**: 20s (enforced for LoRa path)
- **Priority**: HIGH/NORMAL/LOW → mapped to RQ queues
- **Retry**: exponential backoff (future)
- **Edge gateway**: uploads clip to backend `/ptt/message` with priority LOW
- **Guard app**: records clip, retries if network down (queue locally)

Pseudo-code for edge gateway:

```python
def send_clip(path, group, sender):
    # analyze duration; if >20s: reject
    # enqueue LOW priority to backend
    # persist until 200 OK, then delete local copy
```
