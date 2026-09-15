# Editzaar AI Blogger CMS & Telegram Bot 🚀

Automated AI Publishing engine for [Editzaar Blogs](https://blog.editzaar.in/) powered by **Google Gemini AI**, **Live Web Search Grounding**, and **Blogger API v3**.

## Features
- 🤖 **Operable from Telegram**: Send any topic, film name, software question, or plugin idea to @EditzaarPublisherBot.
- 🌐 **Live Web Grounding**: Real-time multi-query web research for latest facts, software updates, and trends.
- 🎨 **Dynamic 3D Typography Thumbnails**: High-CTR 16:9 studio graphic thumbnails rendered automatically and embedded via Base64.
- 📝 **Humanized Masterclass Articles**: 1,200 to 1,800+ word structured articles with HTML comparison tables, exact parameters, and pro creator advice.
- 🎯 **Strict SEO Adherence**: Single tag categorization, India geo-location, and <145 char search descriptions.
- 🛡️ **Deduplication Engine**: Guaranteed single-instance drafting on Blogger.

## Deploying to 24/7 Cloud (Render.com / Railway)

1. Connect this repository to [Render.com](https://render.com/).
2. Create a **Background Worker** (or **Web Service**).
3. Set **Build Command**: pip install -r requirements.txt
4. Set **Start Command**: python telegram_bot.py
5. Deploy!
