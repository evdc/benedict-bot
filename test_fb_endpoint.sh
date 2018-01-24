export url=localhost:5000
# export url=https://sleepy-inlet-12197.herokuapp.com

curl "${url}/?hub.mode=subscribe&hub.challenge=1312499193&hub.verify_token=Q1W2E3R4T5"

curl -XPOST "{$url}" -H "Content-Type: application/json" -d '{"entry": [{"id": "128995024567079", "time": 1516765077025, "messaging": [{"message": {"text": "Hello world!", "seq": 324729, "mid": "mid.$cAAB1UabM_AxnV1QXaFhJg7cWo34b"}, "recipient": {"id": "128995024567079"}, "timestamp": 1516761960296, "sender": {"id": "1845441168823830"}}]}], "object": "page"}'