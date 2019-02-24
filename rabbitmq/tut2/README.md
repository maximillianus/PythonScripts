## Points in 2nd tutorial
- Use 2 consumers (or workers) to do *round-robin* style dispatching
- turn on message acknowledgement (`basic_ack`, `no_ack=False`) for consumers so we know message is not lost when a consumer died
- add `durable` property to our queue to create durable queue
- turn on **message persistence** so message is not lost
- add `prefetch_count` so round robin will dispatch message to queue which is not busy