============================================
実践ガイド
============================================

Fess で実現するナレッジ活用戦略
================================

ゴール指向で学ぶエンタープライズサーチ実践ガイド。
ユースケース起点で、Fess の導入から AI 活用までを全23回で解説します。

**基礎編（初心者向け）**

- :doc:`articles/guide-01` - 企業における情報検索の必要性と散在する情報の活用課題を解説
- :doc:`articles/guide-02` - Docker Composeで数分でFessを起動し検索を体験するクイックスタート
- :doc:`articles/guide-03` - 既存Webサイトへの検索ウィジェット埋め込み3パターンを紹介
- :doc:`articles/guide-04` - ファイルサーバーやクラウドストレージなど複数ソースの横断検索を構築
- :doc:`articles/guide-05` - ロールやラベルを使った部門別・権限別の検索結果フィルタリング

**実践ソリューション編（中級者向け）**

- :doc:`articles/guide-06` - Git・Wiki・チケットなど開発系ナレッジを統合検索する環境を構築
- :doc:`articles/guide-07` - Google Drive・SharePoint・Boxをまとめて検索する設定と運用
- :doc:`articles/guide-08` - 検索ログ分析に基づくチューニングの改善サイクルを実践
- :doc:`articles/guide-09` - 日本語・英語・中国語文書を正しく検索するアナライザー設定
- :doc:`articles/guide-10` - 本番環境の監視・バックアップ・障害対策のベストプラクティス
- :doc:`articles/guide-11` - REST APIを使ったCRM・社内システムとの連携パターン集
- :doc:`articles/guide-12` - Salesforce・データベースなどSaaSデータのインデックス化手順

**アーキテクチャ・スケーリング編（上級者向け）**

- :doc:`articles/guide-13` - 1つのFessインスタンスで複数組織にサービスするテナント設計
- :doc:`articles/guide-14` - シングルサーバーからクラスター構成への段階的スケーリング戦略
- :doc:`articles/guide-15` - SSO（OIDC/SAML）連携とゼロトラスト環境でのアクセス制御設計
- :doc:`articles/guide-16` - Fess設定のコード管理とCI/CDパイプラインによるデプロイ自動化
- :doc:`articles/guide-17` - カスタムデータソースプラグインとIngestパイプラインの実装方法

**AI・次世代検索編（上級者向け）**

- :doc:`articles/guide-18` - キーワード検索からベクトル検索・セマンティック検索への進化を概説
- :doc:`articles/guide-19` - RAGを活用した社内文書ベースの質問応答システムの構築手順
- :doc:`articles/guide-20` - MCPサーバーとしてFessをClaude等の外部AIツールと統合
- :doc:`articles/guide-21` - ベクトル埋め込みによるテキスト・画像の横断マルチモーダル検索
- :doc:`articles/guide-22` - 検索ログをOpenSearch Dashboardsで可視化し情報活用を分析

**総括**

- :doc:`articles/guide-23` - 全23回の要素を統合した全社ナレッジ基盤のリファレンスアーキテクチャ

ユースケース・活用事例
====================

- :doc:`articles/use-cases` - 業種別・規模別の活用事例とユースケース
- :doc:`articles/comparison` - Fess と他の検索ソリューション（Elasticsearch、Solr 等）の比較

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-03
   articles/guide-04
   articles/guide-05
   articles/guide-06
   articles/guide-07
   articles/guide-08
   articles/guide-09
   articles/guide-10
   articles/guide-11
   articles/guide-12
   articles/guide-13
   articles/guide-14
   articles/guide-15
   articles/guide-16
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-22
   articles/guide-23
   articles/use-cases
   articles/comparison
