```bash
# daemon の実行ログを見る方法
sudo journalctl -u record-server-recorder -n 50 | cat
```

POST /features
```bash
curl -X POST http://localhost:3000/features -H "Content-Type: application/json" -d '{"vector": [1.0, 2.0, 3.0], "timestamp": "2024-03-20T10:00:00Z"}'
```