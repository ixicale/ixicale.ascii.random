#!/usr/bin/env python3
"""
ASCII Manager - Gestor principal para ASCII arts con funcionalidades avanzadas
"""
import random
from typing import Dict, List, Optional
from ascii_loader import ASCIILoader

class ASCIIManager:
    """Gestor principal para operaciones con ASCII arts"""

    def __init__(self, base_path: str = "ascii_arts"):
        self.loader = ASCIILoader(base_path)

    def get_random_ascii(self, category: Optional[str] = None,
                        include_nsfw: bool = False,
                        tags: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Retorna un ASCII art aleatorio con filtros opcionales

        Args:
            category: Categoría específica (opcional)
            include_nsfw: Incluir contenido NSFW
            tags: Lista de tags para filtrar (opcional)
        """
        if tags:
            ascii_list = self.loader.get_ascii_by_tags(tags, include_nsfw)
        elif category:
            ascii_list = self.loader.get_category_ascii(category, include_nsfw)
        else:
            ascii_list = self.loader.get_all_ascii_info(include_nsfw)

        if not ascii_list:
            return None

        selected = random.choice(ascii_list)
        content = self.loader.get_ascii_content(selected)

        return {
            **selected,
            'content': content
        }

    def search_and_get_ascii(self, query: str, include_nsfw: bool = False) -> List[Dict]:
        """
        Busca ASCII arts y retorna los resultados con contenido incluido
        """
        search_results = self.loader.search_ascii(query, include_nsfw)
        results_with_content = []

        for result in search_results:
            content = self.loader.get_ascii_content(result)
            results_with_content.append({
                **result,
                'content': content
            })

        return results_with_content

    def get_categories_info(self) -> List[Dict]:
        """Retorna información completa de todas las categorías"""
        categories_info = []

        for category in self.loader.get_categories():
            metadata = self.loader.load_category_metadata(category)
            if metadata:
                ascii_count = len(metadata.get('files', []))
                nsfw_count = sum(1 for f in metadata.get('files', []) if f.get('nsfw', False))

                categories_info.append({
                    'name': category,
                    'description': metadata.get('description', ''),
                    'nsfw': metadata.get('nsfw', False),
                    'total_ascii': ascii_count,
                    'nsfw_ascii': nsfw_count,
                    'safe_ascii': ascii_count - nsfw_count
                })

        return categories_info

    def get_all_tags(self, include_nsfw: bool = False) -> List[str]:
        """Retorna lista de todos los tags disponibles"""
        all_tags = set()

        for ascii_info in self.loader.get_all_ascii_info(include_nsfw):
            all_tags.update(ascii_info['tags'])

        return sorted(list(all_tags))

    def get_stats(self) -> Dict:
        """Retorna estadísticas generales del sistema"""
        all_ascii = self.loader.get_all_ascii_info(include_nsfw=True)
        safe_ascii = self.loader.get_all_ascii_info(include_nsfw=False)

        categories = self.loader.get_categories()
        all_tags = self.get_all_tags(include_nsfw=True)

        return {
            'total_categories': len(categories),
            'total_ascii': len(all_ascii),
            'safe_ascii': len(safe_ascii),
            'nsfw_ascii': len(all_ascii) - len(safe_ascii),
            'total_tags': len(all_tags),
            'categories': categories
        }

    def list_ascii_in_category(self, category: str, include_nsfw: bool = False) -> List[str]:
        """Retorna lista de nombres de ASCII arts en una categoría"""
        ascii_list = self.loader.get_category_ascii(category, include_nsfw)
        return [ascii['original_name'] for ascii in ascii_list]

    def get_ascii_by_name(self, name: str, include_nsfw: bool = False) -> Optional[Dict]:
        """Busca y retorna un ASCII art específico por nombre"""
        # Buscar por nombre exacto primero
        for ascii_info in self.loader.get_all_ascii_info(include_nsfw):
            if ascii_info['original_name'].lower() == name.lower():
                content = self.loader.get_ascii_content(ascii_info)
                return {
                    **ascii_info,
                    'content': content
                }

        # Si no se encuentra exacto, buscar por coincidencia parcial
        for ascii_info in self.loader.get_all_ascii_info(include_nsfw):
            if name.lower() in ascii_info['original_name'].lower():
                content = self.loader.get_ascii_content(ascii_info)
                return {
                    **ascii_info,
                    'content': content
                }

        return None

    def validate_system(self) -> Dict:
        """Valida el sistema completo y retorna reporte"""
        is_valid, errors = self.loader.validate_structure()
        stats = self.get_stats()

        return {
            'valid': is_valid,
            'errors': errors,
            'stats': stats,
            'categories_info': self.get_categories_info()
        }

    def reload_cache(self):
        """Recarga el cache del loader"""
        self.loader.clear_cache()

    def print_ascii(self, ascii_data: Dict):
        """Imprime un ASCII art de manera formateada"""
        if not ascii_data or not ascii_data.get('content'):
            print("❌ No ASCII art to display")
            return

        print(f"🎨 {ascii_data['original_name']} ({ascii_data['category']})")
        if ascii_data.get('tags'):
            print(f"🏷️  Tags: {', '.join(ascii_data['tags'])}")
        print("─" * 50)
        print(ascii_data['content'])
        print("─" * 50)

    def print_categories_summary(self):
        """Imprime resumen de categorías disponibles"""
        print("📁 Available Categories:")
        print("═" * 50)

        for cat_info in self.get_categories_info():
            nsfw_indicator = " 🔞" if cat_info['nsfw'] else ""
            print(f"▶ {cat_info['name']}{nsfw_indicator}")
            print(f"   {cat_info['description']}")
            print(f"   📊 {cat_info['total_ascii']} ASCII arts total")
            if cat_info['nsfw_ascii'] > 0:
                print(f"   🔞 {cat_info['nsfw_ascii']} NSFW, {cat_info['safe_ascii']} Safe")
            print()

if __name__ == "__main__":
    # Test del manager
    manager = ASCIIManager()

    print("🎮 Testing ASCII Manager...")
    print("=" * 50)

    # Mostrar estadísticas
    stats = manager.get_stats()
    print(f"📊 System Stats:")
    print(f"   Categories: {stats['total_categories']}")
    print(f"   Total ASCII: {stats['total_ascii']}")
    print(f"   Safe ASCII: {stats['safe_ascii']}")
    print(f"   NSFW ASCII: {stats['nsfw_ascii']}")
    print(f"   Tags: {stats['total_tags']}")
    print()

    # Mostrar categorías
    manager.print_categories_summary()

    # Test ASCII aleatorio
    print("🎲 Random ASCII (safe):")
    random_ascii = manager.get_random_ascii(include_nsfw=False)
    if random_ascii:
        manager.print_ascii(random_ascii)

    # Test búsqueda
    print("\n🔍 Search test (neko):")
    search_results = manager.search_and_get_ascii("neko", include_nsfw=False)
    print(f"Found {len(search_results)} results")
    if search_results:
        print(f"First result: {search_results[0]['original_name']}")

    # Validación
    validation = manager.validate_system()
    print(f"\n✅ System validation: {'PASSED' if validation['valid'] else 'FAILED'}")
    if not validation['valid']:
        print("Errors found:")
        for error in validation['errors']:
            print(f"   - {error}")