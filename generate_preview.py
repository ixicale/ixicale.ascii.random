#!/usr/bin/env python3
"""
ASCII Preview Generator - Genera documentación actualizada usando el nuevo sistema modular
"""
import os
import argparse
from ascii_manager import ASCIIManager

class PreviewGenerator:
    """Generador de documentación y previews para ASCII arts"""

    def __init__(self, base_path: str = "ascii_arts", output_dir: str = "ascii preview"):
        self.manager = ASCIIManager(base_path)
        self.output_dir = output_dir

    def generate_markdown_preview(self, include_nsfw: bool = False, category_filter: str = None) -> str:
        """Genera documentación completa en formato Markdown"""

        # Obtener estadísticas
        stats = self.manager.get_stats()

        # Encabezado
        md_content = ["# ASCII Art Collection Preview"]
        md_content.append("")
        md_content.append(f"**Generated automatically from the modular ASCII art system**")
        md_content.append("")

        # Estadísticas
        md_content.append("## 📊 Collection Statistics")
        md_content.append("")
        md_content.append(f"- **Total Categories:** {stats['total_categories']}")
        md_content.append(f"- **Total ASCII Arts:** {stats['total_ascii']}")
        md_content.append(f"- **Safe ASCII Arts:** {stats['safe_ascii']}")
        if stats['nsfw_ascii'] > 0:
            md_content.append(f"- **NSFW ASCII Arts:** {stats['nsfw_ascii']}")
        md_content.append(f"- **Total Tags:** {stats['total_tags']}")
        md_content.append("")

        # Índice de categorías
        categories_info = self.manager.get_categories_info()

        if category_filter:
            categories_info = [cat for cat in categories_info if cat['name'] == category_filter]

        md_content.append("## 📁 Categories Index")
        md_content.append("")

        for cat_info in categories_info:
            if not include_nsfw and cat_info['nsfw']:
                continue

            nsfw_badge = " 🔞" if cat_info['nsfw'] else ""
            md_content.append(f"- **[{cat_info['name']}{nsfw_badge}](#{cat_info['name'].lower()})** - {cat_info['description']} ({cat_info['total_ascii']} items)")

        md_content.append("")

        # Tags más populares
        all_tags = self.manager.get_all_tags(include_nsfw=include_nsfw)
        md_content.append("## 🏷️ Popular Tags")
        md_content.append("")

        # Contar frecuencia de tags
        tag_counts = {}
        for ascii_info in self.manager.loader.get_all_ascii_info(include_nsfw=include_nsfw):
            for tag in ascii_info['tags']:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Top 20 tags
        popular_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        tag_lines = []
        for i, (tag, count) in enumerate(popular_tags):
            tag_lines.append(f"`{tag}` ({count})")
            if (i + 1) % 5 == 0:  # Nueva línea cada 5 tags
                md_content.append(" | ".join(tag_lines))
                tag_lines = []

        if tag_lines:  # Agregar tags restantes
            md_content.append(" | ".join(tag_lines))

        md_content.append("")

        # Contenido por categorías
        md_content.append("---")
        md_content.append("")

        for cat_info in categories_info:
            if not include_nsfw and cat_info['nsfw']:
                continue

            category = cat_info['name']
            md_content.append(f"## {category.title()}")

            nsfw_badge = " 🔞" if cat_info['nsfw'] else ""
            md_content.append(f"**Category:** {category}{nsfw_badge}")
            md_content.append(f"**Description:** {cat_info['description']}")
            md_content.append(f"**Total ASCII Arts:** {cat_info['total_ascii']}")
            md_content.append("")

            # Obtener ASCII arts de la categoría
            ascii_list = self.manager.loader.get_category_ascii(category, include_nsfw=include_nsfw)

            for ascii_info in ascii_list:
                if not include_nsfw and ascii_info.get('nsfw', False):
                    continue

                content = self.manager.loader.get_ascii_content(ascii_info)
                if content:
                    nsfw_indicator = " 🔞" if ascii_info.get('nsfw', False) else ""
                    md_content.append(f"### {ascii_info['original_name']}{nsfw_indicator}")

                    if ascii_info.get('tags'):
                        tag_badges = " ".join([f"`{tag}`" for tag in ascii_info['tags']])
                        md_content.append(f"**Tags:** {tag_badges}")

                    md_content.append("")
                    md_content.append("```")
                    md_content.append(content)
                    md_content.append("```")
                    md_content.append("")

        return "\n".join(md_content)

    def generate_category_preview(self, category: str, include_nsfw: bool = False) -> str:
        """Genera preview específico para una categoría"""

        md_content = [f"# {category.title()} ASCII Arts"]
        md_content.append("")

        # Info de la categoría
        metadata = self.manager.loader.load_category_metadata(category)
        if metadata:
            md_content.append(f"**Description:** {metadata.get('description', 'No description')}")
            nsfw_badge = " 🔞" if metadata.get('nsfw', False) else ""
            md_content.append(f"**Category:** {category}{nsfw_badge}")
            md_content.append("")

        # ASCII arts
        ascii_list = self.manager.loader.get_category_ascii(category, include_nsfw=include_nsfw)

        for ascii_info in ascii_list:
            if not include_nsfw and ascii_info.get('nsfw', False):
                continue

            content = self.manager.loader.get_ascii_content(ascii_info)
            if content:
                nsfw_indicator = " 🔞" if ascii_info.get('nsfw', False) else ""
                md_content.append(f"## {ascii_info['original_name']}{nsfw_indicator}")

                if ascii_info.get('tags'):
                    tag_badges = " ".join([f"`{tag}`" for tag in ascii_info['tags']])
                    md_content.append(f"**Tags:** {tag_badges}")

                md_content.append("")
                md_content.append("```")
                md_content.append(content)
                md_content.append("```")
                md_content.append("")

        return "\n".join(md_content)

    def generate_tag_index(self, include_nsfw: bool = False) -> str:
        """Genera índice organizado por tags"""

        md_content = ["# ASCII Arts by Tags"]
        md_content.append("")

        # Organizar por tags
        tag_index = {}
        for ascii_info in self.manager.loader.get_all_ascii_info(include_nsfw=include_nsfw):
            if not include_nsfw and ascii_info.get('nsfw', False):
                continue

            for tag in ascii_info['tags']:
                if tag not in tag_index:
                    tag_index[tag] = []
                tag_index[tag].append(ascii_info)

        # Generar contenido por tag
        for tag in sorted(tag_index.keys()):
            md_content.append(f"## Tag: `{tag}`")
            md_content.append("")

            ascii_list = tag_index[tag]
            md_content.append(f"**ASCII Arts with this tag:** {len(ascii_list)}")
            md_content.append("")

            for ascii_info in ascii_list:
                nsfw_indicator = " 🔞" if ascii_info.get('nsfw', False) else ""
                md_content.append(f"- **{ascii_info['original_name']}** ({ascii_info['category']}){nsfw_indicator}")

            md_content.append("")

        return "\n".join(md_content)

    def save_to_file(self, content: str, filename: str):
        """Guarda contenido a archivo"""
        os.makedirs(self.output_dir, exist_ok=True)

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Generated: {filepath}")

    def generate_all_previews(self, include_nsfw: bool = False):
        """Genera todos los previews disponibles"""

        print("🔄 Generating ASCII Art documentation...")

        # Preview completo
        full_preview = self.generate_markdown_preview(include_nsfw=include_nsfw)
        self.save_to_file(full_preview, "README.md")

        # Preview por categorías
        categories = self.manager.loader.get_categories()
        for category in categories:
            category_preview = self.generate_category_preview(category, include_nsfw=include_nsfw)
            self.save_to_file(category_preview, f"{category}.md")

        # Índice de tags
        tag_index = self.generate_tag_index(include_nsfw=include_nsfw)
        self.save_to_file(tag_index, "tags_index.md")

        # Estadísticas del sistema
        stats = self.manager.get_stats()

        print(f"\n📊 Documentation generated:")
        print(f"   - Main README: README.md")
        print(f"   - Category files: {len(categories)} files")
        print(f"   - Tag index: tags_index.md")
        print(f"   - Total ASCII arts documented: {stats['total_ascii']}")
        if not include_nsfw:
            print(f"   - NSFW content excluded ({stats['nsfw_ascii']} items)")

def main():
    parser = argparse.ArgumentParser(description="ASCII Preview Generator")

    parser.add_argument('--output', '-o', type=str, default="ascii preview",
                       help='Output directory for generated files')
    parser.add_argument('--include-nsfw', action='store_true',
                       help='Include NSFW content in generated documentation')
    parser.add_argument('--category', '-c', type=str,
                       help='Generate preview for specific category only')
    parser.add_argument('--tags-only', action='store_true',
                       help='Generate only tag index')
    parser.add_argument('--full-only', action='store_true',
                       help='Generate only full README')

    args = parser.parse_args()

    generator = PreviewGenerator(output_dir=args.output)

    try:
        if args.tags_only:
            tag_index = generator.generate_tag_index(include_nsfw=args.include_nsfw)
            generator.save_to_file(tag_index, "tags_index.md")
        elif args.full_only:
            full_preview = generator.generate_markdown_preview(include_nsfw=args.include_nsfw)
            generator.save_to_file(full_preview, "README.md")
        elif args.category:
            category_preview = generator.generate_category_preview(args.category, include_nsfw=args.include_nsfw)
            generator.save_to_file(category_preview, f"{args.category}.md")
        else:
            generator.generate_all_previews(include_nsfw=args.include_nsfw)

    except Exception as e:
        print(f"❌ Error generating documentation: {e}")

if __name__ == "__main__":
    main()