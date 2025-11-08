#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор статического сайта для базы знаний Манчкин
Новая версия: без категорий, группировка по тегам, поддержка карт и уникальные ID.

Использование:
    python build.py
"""

from jinja2 import Template
import hashlib


def parse_rules(filename='munchkin_rules.txt'):
    """Парсит файл правил и возвращает список словарей"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    rules = []
    blocks = [b.strip() for b in content.split('===') if b.strip()]

    for block in blocks:
        rule = {}
        lines = block.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('ВОПРОС:'):
                rule['title'] = line.replace('ВОПРОС:', '').strip()
            elif line.startswith('РЕШЕНИЕ:'):
                text = line.replace('РЕШЕНИЕ:', '').strip()
                text = text.replace('\\n', '<br>')
                rule['decision'] = text
            elif line.startswith('ССЫЛКИ:'):
                links_str = line.replace('ССЫЛКИ:', '').strip()
                rule['links'] = []
                for link in links_str.split(','):
                    link = link.strip()
                    if '|' in link:
                        text, url = link.split('|', 1)
                        rule['links'].append({'text': text.strip(), 'url': url.strip()})
            elif line.startswith('ТЕГИ:'):
                tags_str = line.replace('ТЕГИ:', '').strip()
                rule['tags'] = [t.strip() for t in tags_str.split(',') if t.strip()]
            elif line.startswith('КАРТЫ:'):
                cards_str = line.replace('КАРТЫ:', '').strip()
                rule['cards'] = [c.strip() for c in cards_str.split(',') if c.strip()]

        if 'title' in rule:
            # Генерация уникального ID на основе названия и решения
            base = rule.get('title', '') + rule.get('decision', '')
            rule['id'] = hashlib.md5(base.encode('utf-8')).hexdigest()[:8]
            rules.append(rule)

    return rules


def group_by_tags(rules):
    """Группирует правила только по тегам"""
    grouped = {}
    for rule in rules:
        for tag in rule.get('tags', []):
            grouped.setdefault(tag, []).append(rule)
    return grouped


def generate_html(rules, template_file='template.html', output_file='index.html'):
    """Генерирует HTML из шаблона"""
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    template = Template(template_content)

    # Группируем по тегам и картам
    grouped = group_by_tags(rules)
    categories = sorted(grouped.keys())

    html = template.render(
        rules=rules,
        grouped=grouped,
        categories=categories
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Сгенерирован {output_file}")
    print(f"  Всего уникальных правил: {len(rules)}")
    print(f"  Категорий (тегов + карт): {len(categories)}")


def main():
    print("Генерация сайта Манчкин...")

    rules = parse_rules('munchkin_rules.txt')
    generate_html(rules, 'munchkin_template.html', 'index.html')

    print("\nГотово! Открой index.html в браузере")


if __name__ == '__main__':
    main()
