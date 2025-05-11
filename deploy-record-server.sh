RASPBERRY_PI_IP="raspberrypi.lan"

# 公開鍵を使用してSSH接続
ssh -i ~/.ssh/id_rsa_mq3rpi mq3@$RASPBERRY_PI_IP 'rm -rf ~/re-entrance'

# ローカルのディレクトリをリモートにコピー
scp -i ~/.ssh/id_rsa_mq3rpi -r ./ mq3@$RASPBERRY_PI_IP:~/re-entrance

# リモートでセットアップスクリプトを実行
ssh -i ~/.ssh/id_rsa_mq3rpi mq3@$RASPBERRY_PI_IP 'cd ~/re-entrance/apps/record-server && chmod +x setup.sh && ./setup.sh'
