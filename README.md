# Re:entrance

![Re:entrance](https://img.shields.io/badge/Project-Re:entrance-brightgreen)
![Event](https://img.shields.io/badge/Event-大宮祭2025-blue)
![Date](https://img.shields.io/badge/Date-20250518-orange)

## 📝 概要

**Re:entrance**は、来場者の入場時の映像を記録し、出口で遅延表示することで意外性のある体験を提供するインタラクティブインスタレーションです。大宮祭（2025年5月18日）のために開発されています。

## 🎬 体験の流れ

```
入場 → 頭上カメラで撮影 → 顔認識カメラで個人識別 → データ記録
  ↓
出口で顔再認識 → 入場時データ照合 → 入場映像検索 → TouchDesignerで処理 → 映像表示
```

1. **入場時**: 来場者が入口を通過すると、頭上カメラが様子を撮影し、顔認識カメラが個人を識別
2. **処理**: システムが個人識別情報とタイムスタンプを記録
3. **退場時**: 出口で再度顔認識を行い、入場時のデータと照合
4. **表示**: 入場時前後20秒の映像をTouchDesignerで処理し、出口付近の装置に表示

## 🖥️ システム構成

### ハードウェア

- **カメラ**
  - 頭上カメラ（個人所有のWebカメラ）
  - 顔認識カメラ（Logicool WebCam C920n）
- **サーバー**: LAN内に設置
- **表示装置**: 出口付近に設置
  - 顔認識カメラ (Logicool WebCam C922)
- **接続機器**: 10m USB延長ケーブル

### ソフトウェア

- **顔認識**: MediaPipe Face Detection API
- **映像処理**: OpenCV / FFmpeg
- **データ管理**: SQLite / Redis
- **映像出力**: TouchDesigner

## 🛠️ 技術スタック

| 分野 | 技術 |
|------|------|
| 顔認識 | MediaPipe |
| 映像処理 | OpenCV, FFmpeg |
| サーバー | WebSocket, HTTP |
| データベース | SQLite / Redis |
| 映像出力 | TouchDesigner |

## ⚙️ セットアップ

### 前提条件

- Python 3.8以上
- Node.js 14以上
- TouchDesigner 2022以上

### インストール

```bash
# リポジトリのクローン
git clone https://github.com/your-username/re-entrance.git
cd re-entrance

# 依存関係のインストール
# WIP
```

### 設定

WIP

### 実行

```bash
# サーバーの起動
# WIP
```

## 📅 スケジュール

WIP

## 🔍 技術的課題と対策

- **顔認識精度**: MediaPipeの高度な顔認識機能と複数特徴点の組み合わせで対応
- **システム遅延**: GPU活用、バッファリング戦略、非同期処理で最適化
- **データ管理**: 匿名化処理、イベント後のデータ削除、閉じたネットワーク内での運用

## 📋 運用手順

WIP

---

© 2025 shogo0x2e
