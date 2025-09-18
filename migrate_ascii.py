#!/usr/bin/env python3
"""
Script para migrar ASCII arts del formato actual a archivos individuales organizados
"""
import os
import json
from run import ASCII_ART, NSFW_TAGS

# Mapeo de ASCII arts a categorías
CATEGORY_MAPPING = {
    # Animals
    'animals': [
        'animals 001', 'animals 002', 'animals 003',
        'neko 001', 'neko 002', 'neko 003', 'neko 004', 'neko 005', 'neko 006', 'neko 007', 'neko 008',
        'pokemon 001'
    ],

    # Emotions
    'emotions': [
        'stare 001', 'stare 002', 'stare 003', 'stare 004', 'stare 005',
        'smile 001', 'smile 002', 'smile 003',
        'love 001', 'love 002', 'love 003',
        'embarrassed 001',
        'amazed 001',
        'shoked 001', 'shoked 002', 'shoked 003',
        'scream 001', 'scream 002',
        'hype 001',
        'smug 001',
        'bravery 001'
    ],

    # People
    'people': [
        'girl 001', 'girl 002', 'girl 003', 'girl 004', 'girl 005', 'girl 006',
        'gigachad 001'
    ],

    # NSFW
    'nsfw': [
        'oppai 001',
        'ahegao 001', 'ahegao 002', 'ahegao 003',
        'nude 001'
    ],

    # Misc
    'misc': [
        'sus 001', 'sus 002', 'sus 003',
        'evil 001',
        'fancy 001',
        'pray 001',
        'shrek'
    ]
}

def get_category_for_ascii(ascii_name):
    """Encuentra la categoría de un ASCII art"""
    for category, ascii_list in CATEGORY_MAPPING.items():
        if ascii_name in ascii_list:
            return category
    return 'misc'  # default category

def sanitize_filename(name):
    """Convierte nombre a formato válido para archivo"""
    return name.replace(' ', '_').replace('/', '_').lower()

def is_nsfw(ascii_name):
    """Determina si un ASCII art es NSFW"""
    return any(tag in ascii_name.lower() for tag in NSFW_TAGS)

def migrate_ascii_arts():
    """Migra todos los ASCII arts a archivos individuales"""

    # Crear estructura de metadatos para cada categoría
    category_metadata = {}

    for ascii_name, ascii_content in ASCII_ART.items():
        category = get_category_for_ascii(ascii_name)
        filename = sanitize_filename(ascii_name)

        # Crear directorio si no existe
        category_dir = f"ascii_arts/{category}"
        os.makedirs(category_dir, exist_ok=True)

        # Escribir archivo ASCII
        ascii_file_path = f"{category_dir}/{filename}.txt"
        with open(ascii_file_path, 'w', encoding='utf-8') as f:
            f.write(ascii_content)

        # Actualizar metadatos de categoría
        if category not in category_metadata:
            category_metadata[category] = {
                "category": category,
                "nsfw": category == 'nsfw',
                "description": get_category_description(category),
                "files": []
            }

        # Generar tags automáticamente
        tags = generate_tags(ascii_name, category)

        category_metadata[category]["files"].append({
            "name": filename,
            "original_name": ascii_name,
            "tags": tags,
            "nsfw": is_nsfw(ascii_name)
        })

    # Escribir archivos de metadatos
    for category, metadata in category_metadata.items():
        metadata_path = f"ascii_arts/{category}/metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ Migración completada:")
    for category, metadata in category_metadata.items():
        print(f"   - {category}: {len(metadata['files'])} archivos")

def get_category_description(category):
    """Retorna descripción de la categoría"""
    descriptions = {
        'animals': 'Cute and adorable animal ASCII arts',
        'emotions': 'ASCII arts expressing various emotions and reactions',
        'people': 'ASCII arts of people, characters and personas',
        'nsfw': 'Not safe for work ASCII arts (18+)',
        'misc': 'Miscellaneous ASCII arts that don\'t fit other categories'
    }
    return descriptions.get(category, 'Various ASCII arts')

def generate_tags(ascii_name, category):
    """Genera tags automáticamente basado en el nombre y categoría"""
    tags = [category]

    # Tags basados en el nombre
    name_lower = ascii_name.lower()

    # Mapeo de palabras clave a tags
    tag_mapping = {
        'neko': ['cat', 'cute', 'kawaii'],
        'pokemon': ['pokemon', 'cute', 'anime'],
        'stare': ['stare', 'intense', 'eyes'],
        'smile': ['smile', 'happy', 'positive'],
        'love': ['love', 'romance', 'heart'],
        'girl': ['girl', 'anime', 'kawaii'],
        'sus': ['sus', 'among_us', 'meme'],
        'gigachad': ['gigachad', 'chad', 'meme'],
        'evil': ['evil', 'dark', 'scary'],
        'ahegao': ['ahegao', 'lewd'],
        'oppai': ['oppai', 'lewd'],
        'nude': ['nude', 'lewd'],
        'embarrassed': ['embarrassed', 'shy', 'blush'],
        'amazed': ['amazed', 'surprised', 'wow'],
        'shoked': ['shocked', 'surprised', 'wow'],
        'scream': ['scream', 'scared', 'horror'],
        'hype': ['hype', 'excited', 'energy'],
        'smug': ['smug', 'confident', 'cocky'],
        'bravery': ['brave', 'courage', 'strong'],
        'shrek': ['shrek', 'ogre', 'meme'],
        'fancy': ['fancy', 'elegant', 'classy'],
        'pray': ['pray', 'religious', 'spiritual']
    }

    for keyword, keyword_tags in tag_mapping.items():
        if keyword in name_lower:
            tags.extend(keyword_tags)

    # Remover duplicados y retornar
    return list(set(tags))

if __name__ == "__main__":
    migrate_ascii_arts()