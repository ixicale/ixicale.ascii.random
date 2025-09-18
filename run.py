#!/usr/bin/env python3
"""
ASCII Art Random Generator - Refactored version with modular system

Available args:
    [--random | -r]:       print random ascii art (default)
    [--list | -l]:         print all ascii art names
    [--categories | -c]:   print all categories
    [--stats | -st]:       print system statistics
    [--safe | -s]:         ignore nsfw ascii arts (default)
    [--all | -a]:          include nsfw ascii arts
    [--category CAT]:      filter by specific category
    [--tags TAG1,TAG2]:    filter by tags
    [--search QUERY]:      search ascii arts
    [--name NAME]:         get specific ascii by name
    [--help | -h]:         print this message

New combinable options:
1. Random ASCII from specific category:
    > python run.py --random --category animals
2. Search ASCII arts:
    > python run.py --search "neko"
3. List all categories:
    > python run.py --categories
4. Get ASCII by tags:
    > python run.py --random --tags "cat,cute"
5. System statistics:
    > python run.py --stats
"""

import argparse
import sys
from ascii_manager import ASCIIManager

# Para compatibilidad con versiones anteriores
NSFW_TAGS = ["ahegao", "oppai", "nude", "nsfw", "sexy"]

def print_random_ascii(manager, safe, category=None, tags=None):
    """Imprime un ASCII art aleatorio"""
    ascii_data = manager.get_random_ascii(
        category=category,
        include_nsfw=not safe,
        tags=tags
    )

    if ascii_data and ascii_data.get('content'):
        print(ascii_data['content'])
    else:
        print("❌ No ASCII art found with the specified criteria")

def print_all_names(manager, safe, category=None):
    """Imprime todos los nombres de ASCII arts disponibles"""
    if category:
        ascii_list = manager.list_ascii_in_category(category, include_nsfw=not safe)
        if ascii_list:
            print(f"📁 ASCII arts in category '{category}':")
            for name in ascii_list:
                print(f"  - {name}")
        else:
            print(f"❌ No ASCII arts found in category '{category}'")
    else:
        ascii_list = manager.loader.get_all_ascii_info(include_nsfw=not safe)
        if ascii_list:
            print("📝 Available ASCII arts:")
            for ascii_info in ascii_list:
                print(f"  - {ascii_info['original_name']} ({ascii_info['category']})")
        else:
            print("❌ No ASCII arts found")

def print_categories(manager):
    """Imprime información de todas las categorías"""
    manager.print_categories_summary()

def print_stats(manager):
    """Imprime estadísticas del sistema"""
    stats = manager.get_stats()
    print("📊 ASCII Art System Statistics")
    print("═" * 40)
    print(f"🗂️  Total Categories: {stats['total_categories']}")
    print(f"🎨 Total ASCII Arts: {stats['total_ascii']}")
    print(f"✅ Safe ASCII Arts: {stats['safe_ascii']}")
    print(f"🔞 NSFW ASCII Arts: {stats['nsfw_ascii']}")
    print(f"🏷️  Total Tags: {stats['total_tags']}")
    print(f"📁 Categories: {', '.join(stats['categories'])}")
    print()

    # Mostrar top tags
    all_tags = manager.get_all_tags(include_nsfw=True)
    print(f"🔥 Sample Tags: {', '.join(all_tags[:10])}")
    if len(all_tags) > 10:
        print(f"   ... and {len(all_tags) - 10} more")

def search_ascii(manager, query, safe):
    """Busca ASCII arts por query"""
    results = manager.search_and_get_ascii(query, include_nsfw=not safe)

    if not results:
        print(f"❌ No ASCII arts found for query: '{query}'")
        return

    print(f"🔍 Found {len(results)} ASCII art(s) for '{query}':")
    print("─" * 50)

    for result in results:
        print(f"📄 {result['original_name']} ({result['category']})")
        if result.get('tags'):
            print(f"🏷️  Tags: {', '.join(result['tags'])}")
        print(result['content'])
        print("─" * 50)

def get_ascii_by_name(manager, name, safe):
    """Obtiene un ASCII específico por nombre"""
    ascii_data = manager.get_ascii_by_name(name, include_nsfw=not safe)

    if ascii_data and ascii_data.get('content'):
        print(ascii_data['content'])
    else:
        print(f"❌ ASCII art '{name}' not found")

def parse_tags(tags_str):
    """Parsea string de tags separados por comas"""
    if not tags_str:
        return None
    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]

def main():
    parser = argparse.ArgumentParser(
        description="ASCII Art Random Generator - Modular Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Opciones principales
    parser.add_argument('--random', '-r', action='store_true',
                       help='Print random ASCII art (default)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='Print all ASCII art names')
    parser.add_argument('--categories', '-c', action='store_true',
                       help='Print all categories')
    parser.add_argument('--stats', '-st', action='store_true',
                       help='Print system statistics')

    # Filtros de contenido
    parser.add_argument('--safe', '-s', action='store_true',
                       help='Ignore NSFW ASCII arts (default)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Include NSFW ASCII arts')

    # Filtros específicos
    parser.add_argument('--category', type=str,
                       help='Filter by specific category')
    parser.add_argument('--tags', type=str,
                       help='Filter by tags (comma-separated)')
    parser.add_argument('--search', type=str,
                       help='Search ASCII arts by query')
    parser.add_argument('--name', type=str,
                       help='Get specific ASCII by name')

    args = parser.parse_args()

    # Inicializar manager
    try:
        manager = ASCIIManager()
    except Exception as e:
        print(f"❌ Error initializing ASCII Manager: {e}")
        print("💡 Make sure the ascii_arts directory exists and is properly structured")
        sys.exit(1)

    # Validar sistema
    validation = manager.validate_system()
    if not validation['valid']:
        print("⚠️  Warning: System validation failed")
        print("Errors found:")
        for error in validation['errors']:
            print(f"   - {error}")
        print()

    # Determinar si usar contenido NSFW
    safe = True
    if args.all:
        safe = False

    # Parsear tags
    tags = parse_tags(args.tags) if args.tags else None

    # Validar categoría si se especifica
    if args.category:
        available_categories = manager.loader.get_categories()
        if args.category not in available_categories:
            print(f"❌ Category '{args.category}' not found")
            print(f"📁 Available categories: {', '.join(available_categories)}")
            sys.exit(1)

    # Ejecutar comando principal
    try:
        if args.categories:
            print_categories(manager)
        elif args.stats:
            print_stats(manager)
        elif args.search:
            search_ascii(manager, args.search, safe)
        elif args.name:
            get_ascii_by_name(manager, args.name, safe)
        elif args.list:
            print_all_names(manager, safe, args.category)
        else:
            # Default: random ASCII
            print_random_ascii(manager, safe, args.category, tags)

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()