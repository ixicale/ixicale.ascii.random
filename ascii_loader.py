#!/usr/bin/env python3
"""
ASCII Loader - Sistema de carga dinámico para ASCII arts
"""
import os
import json
from typing import Dict, List, Optional, Tuple

class ASCIILoader:
    """Clase para cargar ASCII arts desde archivos organizados"""

    def __init__(self, base_path: str = "ascii_arts"):
        self.base_path = base_path
        self._metadata_cache = {}
        self._ascii_cache = {}

    def get_categories(self) -> List[str]:
        """Retorna lista de categorías disponibles"""
        categories = []
        if os.path.exists(self.base_path):
            for item in os.listdir(self.base_path):
                category_path = os.path.join(self.base_path, item)
                if os.path.isdir(category_path):
                    metadata_path = os.path.join(category_path, "metadata.json")
                    if os.path.exists(metadata_path):
                        categories.append(item)
        return sorted(categories)

    def load_category_metadata(self, category: str) -> Optional[Dict]:
        """Carga metadatos de una categoría específica"""
        if category in self._metadata_cache:
            return self._metadata_cache[category]

        metadata_path = os.path.join(self.base_path, category, "metadata.json")
        if not os.path.exists(metadata_path):
            return None

        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                self._metadata_cache[category] = metadata
                return metadata
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    def load_ascii_art(self, category: str, filename: str) -> Optional[str]:
        """Carga un ASCII art específico"""
        cache_key = f"{category}/{filename}"

        if cache_key in self._ascii_cache:
            return self._ascii_cache[cache_key]

        ascii_path = os.path.join(self.base_path, category, f"{filename}.txt")
        if not os.path.exists(ascii_path):
            return None

        try:
            with open(ascii_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self._ascii_cache[cache_key] = content
                return content
        except FileNotFoundError:
            return None

    def get_all_ascii_info(self, include_nsfw: bool = False) -> List[Dict]:
        """Retorna información de todos los ASCII arts disponibles"""
        all_ascii = []

        for category in self.get_categories():
            metadata = self.load_category_metadata(category)
            if not metadata:
                continue

            # Filtrar NSFW si es necesario
            if not include_nsfw and metadata.get('nsfw', False):
                continue

            for file_info in metadata.get('files', []):
                if not include_nsfw and file_info.get('nsfw', False):
                    continue

                all_ascii.append({
                    'category': category,
                    'filename': file_info['name'],
                    'original_name': file_info.get('original_name', file_info['name']),
                    'tags': file_info.get('tags', []),
                    'nsfw': file_info.get('nsfw', False)
                })

        return all_ascii

    def search_ascii(self, query: str, include_nsfw: bool = False) -> List[Dict]:
        """Busca ASCII arts que coincidan con la consulta"""
        query_lower = query.lower()
        results = []

        for ascii_info in self.get_all_ascii_info(include_nsfw):
            # Buscar en nombre original
            if query_lower in ascii_info['original_name'].lower():
                results.append(ascii_info)
                continue

            # Buscar en tags
            if any(query_lower in tag.lower() for tag in ascii_info['tags']):
                results.append(ascii_info)
                continue

            # Buscar en categoría
            if query_lower in ascii_info['category'].lower():
                results.append(ascii_info)

        return results

    def get_ascii_by_tags(self, tags: List[str], include_nsfw: bool = False) -> List[Dict]:
        """Retorna ASCII arts que tengan al menos uno de los tags especificados"""
        tags_lower = [tag.lower() for tag in tags]
        results = []

        for ascii_info in self.get_all_ascii_info(include_nsfw):
            ascii_tags_lower = [tag.lower() for tag in ascii_info['tags']]
            if any(tag in ascii_tags_lower for tag in tags_lower):
                results.append(ascii_info)

        return results

    def get_category_ascii(self, category: str, include_nsfw: bool = False) -> List[Dict]:
        """Retorna todos los ASCII arts de una categoría específica"""
        metadata = self.load_category_metadata(category)
        if not metadata:
            return []

        # Filtrar NSFW si es necesario
        if not include_nsfw and metadata.get('nsfw', False):
            return []

        results = []
        for file_info in metadata.get('files', []):
            if not include_nsfw and file_info.get('nsfw', False):
                continue

            results.append({
                'category': category,
                'filename': file_info['name'],
                'original_name': file_info.get('original_name', file_info['name']),
                'tags': file_info.get('tags', []),
                'nsfw': file_info.get('nsfw', False)
            })

        return results

    def get_ascii_content(self, ascii_info: Dict) -> Optional[str]:
        """Carga el contenido de un ASCII art dado su información"""
        return self.load_ascii_art(ascii_info['category'], ascii_info['filename'])

    def clear_cache(self):
        """Limpia el cache interno"""
        self._metadata_cache.clear()
        self._ascii_cache.clear()

    def validate_structure(self) -> Tuple[bool, List[str]]:
        """Valida la estructura de directorios y archivos"""
        errors = []

        if not os.path.exists(self.base_path):
            errors.append(f"Base path '{self.base_path}' does not exist")
            return False, errors

        categories = self.get_categories()
        if not categories:
            errors.append("No valid categories found")
            return False, errors

        for category in categories:
            metadata = self.load_category_metadata(category)
            if not metadata:
                errors.append(f"Invalid metadata for category '{category}'")
                continue

            for file_info in metadata.get('files', []):
                filename = file_info['name']
                ascii_path = os.path.join(self.base_path, category, f"{filename}.txt")
                if not os.path.exists(ascii_path):
                    errors.append(f"Missing ASCII file: {ascii_path}")

        return len(errors) == 0, errors

if __name__ == "__main__":
    # Test básico
    loader = ASCIILoader()

    print("🔍 Testing ASCII Loader...")

    # Test de categorías
    categories = loader.get_categories()
    print(f"📁 Categories found: {categories}")

    # Test de validación
    is_valid, errors = loader.validate_structure()
    print(f"✅ Structure valid: {is_valid}")
    if errors:
        print("❌ Errors found:")
        for error in errors:
            print(f"   - {error}")

    # Test de carga de ASCII
    if categories:
        ascii_list = loader.get_category_ascii(categories[0])
        if ascii_list:
            first_ascii = ascii_list[0]
            content = loader.get_ascii_content(first_ascii)
            print(f"🎨 Loaded ASCII '{first_ascii['original_name']}' from '{first_ascii['category']}'")
            print(f"   Content preview: {content[:50] if content else 'None'}...")