 #!/bin/bash

# エラーが発生したら即座に終了
set -e

echo "=== record-server のセットアップを開始します ==="

# 必要なパッケージのインストール
echo "必要なパッケージをインストールしています..."
sudo apt update
sudo apt install -y python3-venv python3-pip

# 仮想環境のセットアップ
echo "Python仮想環境をセットアップしています..."
python3 -m venv .venv
source .venv/bin/activate

# 依存関係のインストール
echo "依存関係をインストールしています..."
pip install -r requirements.txt

# systemdサービスの設定
echo "systemdサービスを設定しています..."
sudo tee /etc/systemd/system/record-server.service << EOF
[Unit]
Description=Record Server
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/.venv/bin"
ExecStart=$(pwd)/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# サービスの有効化と起動
echo "サービスを起動しています..."
sudo systemctl daemon-reload
sudo systemctl enable record-server
sudo systemctl start record-server

echo "=== セットアップが完了しました ==="
echo "サービスの状態を確認するには: sudo systemctl status record-server"