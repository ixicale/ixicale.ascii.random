#!/usr/bin/env python3
"""
ASCII Art Adder - Herramienta interactiva para agregar nuevos ASCII arts
"""
import os
import json
import argparse
import tempfile
import subprocess
from typing import List, Optional
from ascii_manager import ASCIIManager

class ASCIIAdder:
    """Herramienta para agregar nuevos ASCII arts al sistema"""

    def __init__(self, base_path: str = "ascii_arts"):
        self.base_path = base_path
        self.manager = ASCIIManager(base_path)

    def get_user_input(self, prompt: str, default: Optional[str] = None) -> str:
        """Obtiene entrada del usuario con valor por defecto opcional"""
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            while True:
                user_input = input(f"{prompt}: ").strip()
                if user_input:
                    return user_input
                print("❌ Este campo es requerido")

    def get_multiline_input(self, prompt: str) -> str:
        """Obtiene entrada multilínea del usuario"""
        print(f"{prompt}")
        print("💡 Presiona Ctrl+D (Linux/Mac) o Ctrl+Z (Windows) cuando termines")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        return '\n'.join(lines)

    def open_editor(self, initial_content: str = "") -> str:
        """Abre el editor predeterminado para ingresar ASCII art"""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write(initial_content)
            tmp_path = tmp.name

        # Abrir editor
        editor = os.environ.get('EDITOR', 'nano')
        try:
            subprocess.call([editor, tmp_path])
        except FileNotFoundError:
            print(f"❌ Editor '{editor}' no encontrado. Usando entrada multilínea...")
            os.unlink(tmp_path)
            return self.get_multiline_input("Ingresa el ASCII art")

        # Leer contenido
        try:
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
        finally:
            os.unlink(tmp_path)

        return content

    def sanitize_filename(self, name: str) -> str:
        """Convierte nombre a formato válido para archivo"""
        return name.replace(' ', '_').replace('/', '_').lower()

    def show_categories(self):
        """Muestra categorías disponibles"""
        print("\n📁 Categorías disponibles:")
        for cat_info in self.manager.get_categories_info():
            nsfw_indicator = " 🔞" if cat_info['nsfw'] else ""
            print(f"  - {cat_info['name']}{nsfw_indicator}: {cat_info['description']}")

    def show_existing_tags(self):
        """Muestra tags existentes para referencia"""
        print("\n🏷️  Tags existentes (para referencia):")
        all_tags = self.manager.get_all_tags(include_nsfw=True)

        # Agrupar tags por categorías
        tag_groups = {}
        for ascii_info in self.manager.loader.get_all_ascii_info(include_nsfw=True):
            category = ascii_info['category']
            if category not in tag_groups:
                tag_groups[category] = set()
            tag_groups[category].update(ascii_info['tags'])

        for category, tags in tag_groups.items():
            print(f"  📁 {category}: {', '.join(sorted(tags)[:8])}")
            if len(tags) > 8:
                print(f"      ... y {len(tags) - 8} más")

    def validate_ascii_content(self, content: str) -> bool:
        """Valida que el contenido sea un ASCII art válido"""
        if not content.strip():
            print("❌ El contenido no puede estar vacío")
            return False

        lines = content.split('\n')
        if len(lines) < 2:
            print("❌ El ASCII art debe tener al menos 2 líneas")
            return False

        # Verificar que tenga caracteres ASCII art comunes
        ascii_chars = set('⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿')

        has_ascii_chars = any(char in ascii_chars for line in lines for char in line)
        if not has_ascii_chars:
            print("⚠️  Advertencia: El contenido no parece contener caracteres ASCII art típicos")
            confirm = input("¿Continuar de todos modos? (s/N): ").lower()
            return confirm == 's'

        return True

    def get_next_number_for_pattern(self, category: str, base_name: str) -> int:
        """Obtiene el siguiente número para un patrón de nombres"""
        metadata = self.manager.loader.load_category_metadata(category)
        if not metadata:
            return 1

        # Buscar números existentes con el mismo patrón
        existing_numbers = []
        pattern = self.sanitize_filename(base_name)

        for file_info in metadata.get('files', []):
            filename = file_info['name']
            if filename.startswith(pattern):
                # Extraer número del final
                suffix = filename[len(pattern):].lstrip('_')
                if suffix.isdigit():
                    existing_numbers.append(int(suffix))

        return max(existing_numbers, default=0) + 1

    def add_ascii_interactive(self):
        """Proceso interactivo para agregar un nuevo ASCII art"""
        print("🎨 Herramienta para agregar ASCII Art")
        print("=" * 40)

        # Mostrar información del sistema
        stats = self.manager.get_stats()
        print(f"📊 Sistema actual: {stats['total_ascii']} ASCII arts en {stats['total_categories']} categorías")

        # Mostrar categorías
        self.show_categories()

        # Obtener información básica
        print("\n📝 Información básica:")
        name = self.get_user_input("Nombre del ASCII art (ej: 'pikachu 001')")

        # Validar si ya existe
        existing = self.manager.get_ascii_by_name(name, include_nsfw=True)
        if existing:
            print(f"⚠️  Ya existe un ASCII art con el nombre '{name}'")
            overwrite = input("¿Sobrescribir? (s/N): ").lower()
            if overwrite != 's':
                print("❌ Operación cancelada")
                return False

        # Seleccionar categoría
        print("\n📁 Selección de categoría:")
        categories = self.manager.loader.get_categories()

        while True:
            category = self.get_user_input("Categoría", "misc").lower()
            if category in categories:
                break

            print(f"❌ Categoría '{category}' no existe")
            create_new = input("¿Crear nueva categoría? (s/N): ").lower()
            if create_new == 's':
                description = self.get_user_input("Descripción de la nueva categoría")
                is_nsfw = input("¿Es categoría NSFW? (s/N): ").lower() == 's'

                # Crear directorio y metadata
                category_path = os.path.join(self.base_path, category)
                os.makedirs(category_path, exist_ok=True)

                metadata = {
                    "category": category,
                    "nsfw": is_nsfw,
                    "description": description,
                    "files": []
                }

                metadata_path = os.path.join(category_path, "metadata.json")
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                print(f"✅ Categoría '{category}' creada")
                break
            else:
                print(f"📁 Categorías disponibles: {', '.join(categories)}")

        # Configurar si es NSFW
        category_metadata = self.manager.loader.load_category_metadata(category)
        is_nsfw = category_metadata.get('nsfw', False)

        if not is_nsfw:
            is_nsfw = input("¿Es contenido NSFW? (s/N): ").lower() == 's'

        # Mostrar tags existentes
        self.show_existing_tags()

        # Obtener tags
        print(f"\n🏷️  Tags para '{name}':")
        print("💡 Ingresa tags separados por comas (ej: cute,cat,kawaii)")
        tags_input = self.get_user_input("Tags", category)
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        # Obtener contenido ASCII
        print(f"\n🎨 Contenido ASCII para '{name}':")
        print("Opciones:")
        print("1. Escribir en el editor de texto")
        print("2. Pegar directamente aquí")

        choice = input("Selecciona opción (1/2): ").strip()

        if choice == '1':
            content = self.open_editor()
        else:
            content = self.get_multiline_input("Pega el ASCII art aquí")

        # Validar contenido
        if not self.validate_ascii_content(content):
            return False

        # Mostrar preview
        print("\n👀 Vista previa:")
        print("─" * 40)
        print(content)
        print("─" * 40)

        # Confirmación final
        print(f"\n📋 Resumen:")
        print(f"   Nombre: {name}")
        print(f"   Categoría: {category}")
        print(f"   NSFW: {'Sí' if is_nsfw else 'No'}")
        print(f"   Tags: {', '.join(tags)}")
        print(f"   Líneas: {len(content.split())}")

        confirm = input("\n¿Confirmar creación? (S/n): ").lower()
        if confirm == 'n':
            print("❌ Operación cancelada")
            return False

        # Guardar ASCII art
        return self.save_ascii_art(name, category, content, tags, is_nsfw)

    def save_ascii_art(self, name: str, category: str, content: str, tags: List[str], is_nsfw: bool = False) -> bool:
        """Guarda un nuevo ASCII art en el sistema"""
        try:
            # Generar filename único
            base_name = name.rsplit(' ', 1)[0]  # Remover número si lo hay
            filename = self.sanitize_filename(name)

            # Si no tiene número, generar uno automáticamente
            if not any(char.isdigit() for char in filename[-3:]):
                number = self.get_next_number_for_pattern(category, base_name)
                filename = f"{self.sanitize_filename(base_name)}_{number:03d}"
                name = f"{base_name} {number:03d}"

            # Rutas de archivos
            category_path = os.path.join(self.base_path, category)
            ascii_path = os.path.join(category_path, f"{filename}.txt")
            metadata_path = os.path.join(category_path, "metadata.json")

            # Crear directorio si no existe
            os.makedirs(category_path, exist_ok=True)

            # Guardar archivo ASCII
            with open(ascii_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Actualizar metadata
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                metadata = {
                    "category": category,
                    "nsfw": is_nsfw,
                    "description": f"ASCII arts in {category} category",
                    "files": []
                }

            # Agregar nueva entrada
            new_entry = {
                "name": filename,
                "original_name": name,
                "tags": tags,
                "nsfw": is_nsfw
            }

            # Verificar si ya existe y actualizar o agregar
            existing_index = None
            for i, file_info in enumerate(metadata['files']):
                if file_info['name'] == filename:
                    existing_index = i
                    break

            if existing_index is not None:
                metadata['files'][existing_index] = new_entry
                print(f"✅ ASCII art '{name}' actualizado")
            else:
                metadata['files'].append(new_entry)
                print(f"✅ ASCII art '{name}' agregado")

            # Guardar metadata
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"📁 Guardado en: {ascii_path}")
            print(f"🎯 Nombre del archivo: {filename}")

            # Limpiar cache
            self.manager.reload_cache()

            return True

        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            return False

    def add_ascii_from_file(self, file_path: str, name: Optional[str] = None,
                           category: str = "misc", tags: Optional[List[str]] = None,
                           is_nsfw: bool = False) -> bool:
        """Agrega ASCII art desde un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {file_path}")
            return False

        if not name:
            name = os.path.splitext(os.path.basename(file_path))[0]

        if not tags:
            tags = [category]

        return self.save_ascii_art(name, category, content, tags, is_nsfw)

def main():
    parser = argparse.ArgumentParser(description="ASCII Art Adder - Agregar nuevos ASCII arts")

    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Modo interactivo (default)')
    parser.add_argument('--file', '-f', type=str,
                       help='Cargar ASCII art desde archivo')
    parser.add_argument('--name', '-n', type=str,
                       help='Nombre del ASCII art')
    parser.add_argument('--category', '-c', type=str, default='misc',
                       help='Categoría del ASCII art')
    parser.add_argument('--tags', '-t', type=str,
                       help='Tags separados por comas')
    parser.add_argument('--nsfw', action='store_true',
                       help='Marcar como NSFW')
    parser.add_argument('--list-categories', '-l', action='store_true',
                       help='Listar categorías disponibles')

    args = parser.parse_args()

    adder = ASCIIAdder()

    try:
        if args.list_categories:
            adder.show_categories()
        elif args.file:
            tags = args.tags.split(',') if args.tags else None
            success = adder.add_ascii_from_file(
                args.file, args.name, args.category, tags, args.nsfw
            )
            if success:
                print("✅ ASCII art agregado exitosamente")
            else:
                print("❌ Error al agregar ASCII art")
        else:
            # Modo interactivo (default)
            adder.add_ascii_interactive()

    except KeyboardInterrupt:
        print("\n👋 Operación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()