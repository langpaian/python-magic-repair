"""图鉴与徽章：把法则变成看得见的收藏。"""
from datetime import datetime


def badge_svg(law_name: str, solved_date: str | None = None, accent: str = "#d4af37") -> str:
    """用 Python 生成一枚法则徽章（SVG）。"""
    date = solved_date or datetime.now().strftime("%Y-%m-%d")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="360" viewBox="0 0 300 360">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1a1030"/>
      <stop offset="100%" stop-color="#0d0a1f"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f5d98a"/>
      <stop offset="100%" stop-color="#c49a3c"/>
    </linearGradient>
  </defs>
  <rect width="300" height="360" rx="18" fill="url(#bg)"/>
  <path d="M150 40 L250 90 L250 190 Q250 250 150 310 Q50 250 50 190 L50 90 Z"
        fill="none" stroke="url(#gold)" stroke-width="3"/>
  <text x="150" y="175" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#f5d98a">已化解</text>
  <text x="150" y="225" text-anchor="middle" font-family="Georgia,serif" font-size="19" fill="#e8e0ff">{law_name}</text>
  <text x="150" y="338" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#8a7fb8">{date}</text>
</svg>'''
