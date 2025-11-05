# スタイルガイド - Minimal Shop

## 📖 はじめに

このスタイルガイドは、Minimal Shopアプリケーションの一貫したデザインとコーディングスタイルを維持するためのリファレンスです。

## 🎨 カラーシステム

### CSS変数（カスタムプロパティ）

プロジェクト全体で使用するカラー変数:

```css
:root {
  /* プライマリーカラー */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-light: #3b82f6;
  
  /* セカンダリーカラー */
  --color-secondary: #10b981;
  --color-secondary-hover: #059669;
  
  /* ニュートラルカラー */
  --color-text: #1f2937;
  --color-text-secondary: #6b7280;
  --color-border: #e5e7eb;
  --color-background: #f9fafb;
  --color-surface: #ffffff;
  
  /* ステータスカラー */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
}
```

### カラー使用例

#### テキスト
- **本文**: `color: var(--color-text);`
- **補足情報**: `color: var(--color-text-secondary);`
- **リンク**: `color: var(--color-primary);`

#### 背景
- **ページ背景**: `background-color: var(--color-background);`
- **カード背景**: `background-color: var(--color-surface);`

#### ボーダー
- **境界線**: `border: 1px solid var(--color-border);`

## 📏 スペーシング

### スペーシング変数

```css
:root {
  --space-xs: 0.25rem;   /* 4px */
  --space-sm: 0.5rem;    /* 8px */
  --space-md: 1rem;      /* 16px */
  --space-lg: 1.5rem;    /* 24px */
  --space-xl: 2rem;      /* 32px */
  --space-2xl: 3rem;     /* 48px */
}
```

### 使用ガイドライン

- **コンポーネント内の余白**: `--space-sm` または `--space-md`
- **セクション間の余白**: `--space-lg` または `--space-xl`
- **ページレベルの余白**: `--space-2xl`

## 🔤 タイポグラフィ

### フォントサイズ

```css
:root {
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 2rem;      /* 32px */
}
```

### フォントウェイト

```css
:root {
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

### 行間

```css
:root {
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.6;
}
```

### タイポグラフィ使用例

```html
<!-- ページタイトル -->
<h1 class="text-3xl font-bold">ページタイトル</h1>

<!-- セクションタイトル -->
<h2 class="text-2xl font-semibold">セクションタイトル</h2>

<!-- 本文 -->
<p class="text-base">本文テキスト</p>

<!-- 補足テキスト -->
<small class="text-sm text-secondary">補足情報</small>
```

## 🔘 コンポーネント

### ボタン

#### プライマリボタン
```html
<button class="btn btn--primary">プライマリアクション</button>
```

スタイル:
```css
.btn {
  padding: var(--space-sm) var(--space-lg);
  border-radius: 0.375rem;
  font-weight: var(--font-weight-medium);
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn--primary {
  background-color: var(--color-primary);
  color: white;
  border: none;
}

.btn--primary:hover {
  background-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

#### セカンダリボタン
```html
<button class="btn btn--secondary">セカンダリアクション</button>
```

スタイル:
```css
.btn--secondary {
  background-color: var(--color-surface);
  color: var(--color-primary);
  border: 1px solid var(--color-border);
}

.btn--secondary:hover {
  background-color: var(--color-background);
  border-color: var(--color-primary);
}
```

### カード

#### 基本カード
```html
<div class="card">
  <div class="card__header">
    <h3 class="card__title">カードタイトル</h3>
  </div>
  <div class="card__body">
    <p>カードの内容</p>
  </div>
</div>
```

スタイル:
```css
.card {
  background-color: var(--color-surface);
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  padding: var(--space-lg);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card__header {
  margin-bottom: var(--space-md);
}

.card__title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
}

.card__body {
  color: var(--color-text-secondary);
}
```

### ナビゲーションバー

```html
<nav class="navbar">
  <div class="navbar__container">
    <div class="navbar__brand">
      <a href="/" class="navbar__logo">Minimal Shop</a>
    </div>
    <div class="navbar__menu">
      <a href="/products/" class="navbar__link">商品一覧</a>
      <a href="/admin/" class="navbar__link">管理画面</a>
    </div>
  </div>
</nav>
```

スタイル:
```css
.navbar {
  background-color: var(--color-surface);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar__container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-md) var(--space-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar__logo {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  text-decoration: none;
}

.navbar__menu {
  display: flex;
  gap: var(--space-lg);
}

.navbar__link {
  color: var(--color-text);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: color 0.3s ease;
}

.navbar__link:hover {
  color: var(--color-primary);
}
```

## 📱 レスポンシブデザイン

### ブレークポイント

```css
/* モバイル（デフォルト）: < 640px */

/* タブレット */
@media (min-width: 640px) {
  /* タブレット用スタイル */
}

/* デスクトップ */
@media (min-width: 1024px) {
  /* デスクトップ用スタイル */
}
```

### レスポンシブグリッド例

```css
.product-grid {
  display: grid;
  gap: var(--space-lg);
  /* モバイル: 1カラム */
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .product-grid {
    /* タブレット: 2カラム */
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .product-grid {
    /* デスクトップ: 3カラム */
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## 🎭 アニメーション

### トランジション

基本のトランジション:
```css
.element {
  transition: all 0.3s ease;
}
```

### ホバーエフェクト

#### カードのホバー
```css
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

#### ボタンのホバー
```css
.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

## 🧩 ユーティリティクラス

### テキストユーティリティ

```css
/* テキストサイズ */
.text-xs { font-size: var(--font-size-xs); }
.text-sm { font-size: var(--font-size-sm); }
.text-base { font-size: var(--font-size-base); }
.text-lg { font-size: var(--font-size-lg); }
.text-xl { font-size: var(--font-size-xl); }
.text-2xl { font-size: var(--font-size-2xl); }
.text-3xl { font-size: var(--font-size-3xl); }

/* フォントウェイト */
.font-normal { font-weight: var(--font-weight-normal); }
.font-medium { font-weight: var(--font-weight-medium); }
.font-semibold { font-weight: var(--font-weight-semibold); }
.font-bold { font-weight: var(--font-weight-bold); }

/* テキストカラー */
.text-primary { color: var(--color-text); }
.text-secondary { color: var(--color-text-secondary); }
.text-accent { color: var(--color-primary); }
```

### スペーシングユーティリティ

```css
/* マージン */
.m-0 { margin: 0; }
.m-sm { margin: var(--space-sm); }
.m-md { margin: var(--space-md); }
.m-lg { margin: var(--space-lg); }

/* パディング */
.p-0 { padding: 0; }
.p-sm { padding: var(--space-sm); }
.p-md { padding: var(--space-md); }
.p-lg { padding: var(--space-lg); }
```

## 📋 コーディング規約

### HTML

1. **セマンティックHTML**: 適切なHTML5タグを使用
   ```html
   <header>, <nav>, <main>, <section>, <article>, <footer>
   ```

2. **クラス命名**: BEM命名規則を推奨
   ```html
   <div class="block__element--modifier">
   ```

3. **アクセシビリティ**: alt属性、ARIAラベルの適切な使用

### CSS

1. **カスタムプロパティ**: 色やサイズはCSS変数で管理
   ```css
   color: var(--color-primary);
   ```

2. **コメント**: 各セクションにわかりやすいコメントを追加
   ```css
   /* ===================================
      コンポーネント: ボタン
      ================================ */
   ```

3. **単位**: 
   - フォントサイズ: `rem`
   - スペーシング: `rem`
   - ボーダー: `px`

## ✅ チェックリスト

新しいコンポーネントを追加する際:

- [ ] デザインコンセプトに沿っているか
- [ ] CSS変数を使用しているか
- [ ] レスポンシブ対応しているか
- [ ] アクセシビリティを考慮しているか
- [ ] コメントを適切に記述しているか
- [ ] ブラウザ互換性を確認したか

## 🔗 関連ドキュメント

- [デザインコンセプト](./DESIGN_CONCEPT.md)
- [Django公式ドキュメント](https://docs.djangoproject.com/)

---

**作成日**: 2025-11-05  
**バージョン**: 1.0  
**担当**: GitHub Copilot Agent
