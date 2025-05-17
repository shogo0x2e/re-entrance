```bash
# daemon の実行ログを見る方法
sudo journalctl -u record-server-recorder -n 50 | cat
```

POST /features
```bash
curl -X POST http://localhost:3000/features -H "Content-Type: application/json" -d '{"vector": [1.0, 2.0, 3.0], "timestamp": "2024-03-20T10:00:00Z"}'
```

POST /clips
```bash
curl -X POST http://localhost:3000/clips \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/Users/shogo/Desktop/IMG_9907.mp4;type=video/mp4" \
  -F "metadata={\"recordedAt\":\"2024-03-20T10:00:00Z\",\"duration\":9}" \
  -H "Accept: application/json"
```