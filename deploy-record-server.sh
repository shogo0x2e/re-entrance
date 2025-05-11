RASPBERRY_PI_IP="raspberrypi.lan"

# requirements.txt を export
cd apps/record-server
uv pip freeze > requirements.txt


# リモートでサービスを停止・無効化し、古いサービスファイルを削除
ssh -i ~/.ssh/id_rsa_mq3rpi mq3@$RASPBERRY_PI_IP '
if systemctl is-active record-server &>/dev/null; then
  sudo systemctl stop record-server && sudo systemctl disable record-server
  sudo rm -f /etc/systemd/system/record-server.service
  echo "既存のrecord-serverサービスを停止・無効化しました"
else
  echo "record-serverサービスは既にインストールされていないためスキップします"
fi'

# record-server-recorderサービスの停止・無効化
ssh -i ~/.ssh/id_rsa_mq3rpi mq3@$RASPBERRY_PI_IP '
if systemctl is-active record-server-recorder &>/dev/null; then
  sudo systemctl stop record-server-recorder && sudo systemctl disable record-server-recorder
  sudo rm -f /etc/systemd/system/record-server-recorder.service
  echo "既存のrecord-server-recorderサービスを停止・無効化しました。"
  sudo rm -rf ~/re-entrance-videos/
else
  echo "record-server-recorderサービスは既にインストールされていないためスキップします"
fi'



# リモートのディレクトリを削除 (クリーンインストール用なので一旦コメントアウト)
# ssh -i ~/.ssh/id_rsa_mq3rpi mq3@$RASPBERRY_PI_IP 'rm -rf ~/re-entrance'

# ssh -i ~/.ssh/id_rsa_mq3rpi mq3@$RASPBERRY_PI_IP 'mkdir -p ~/re-entrance/apps/record-server'

# ローカルのディレクトリをリモートにコピー
scp -i ~/.ssh/id_rsa_mq3rpi -r \
  main.py \
  requirements.txt \
  setup.sh \
  pyproject.toml \
  README.md \
  .python-version \
  record.py \
  mq3@$RASPBERRY_PI_IP:~/re-entrance/apps/record-server/

# リモートでセットアップスクリプトを実行
ssh -i ~/.ssh/id_rsa_mq3rpi mq3@$RASPBERRY_PI_IP 'cd ~/re-entrance/apps/record-server && chmod +x setup.sh && ./setup.sh'
