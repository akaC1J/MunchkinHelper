#!/usr/bin/env bash
set -e  # завершить при любой ошибке

# 1. Генерация сайта
echo "🚀 Запуск munchkin_builder.py..."
python3 munchkin_builder.py

# 2. Создание директории public (если нет)
mkdir -p public

# 3. Перенос (или копирование) готовых файлов
echo "📦 Перемещение файлов в папку public..."
mv -f index.html public/
cp -f style.css script.js public/

# 4. Завершение
echo "✅ Сайт успешно собран!"
echo "   Файлы: public/index.html, public/style.css, public/script.js"
