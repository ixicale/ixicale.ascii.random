#!/usr/bin/env python3
"""
System Validator - Valida la integridad del sistema de ASCII arts
"""
from ascii_manager import ASCIIManager

def main():
    print("🔍 Validating ASCII Art System...")
    print("=" * 50)

    manager = ASCIIManager()
    validation = manager.validate_system()

    print(f"✅ System Status: {'VALID' if validation['valid'] else 'INVALID'}")
    print()

    # Mostrar estadísticas
    stats = validation['stats']
    print("📊 System Statistics:")
    print(f"   Categories: {stats['total_categories']}")
    print(f"   Total ASCII Arts: {stats['total_ascii']}")
    print(f"   Safe ASCII Arts: {stats['safe_ascii']}")
    print(f"   NSFW ASCII Arts: {stats['nsfw_ascii']}")
    print(f"   Total Tags: {stats['total_tags']}")
    print()

    # Información de categorías
    print("📁 Categories:")
    for cat_info in validation['categories_info']:
        nsfw_badge = " 🔞" if cat_info['nsfw'] else ""
        print(f"   - {cat_info['name']}{nsfw_badge}: {cat_info['total_ascii']} items")

    # Mostrar errores si los hay
    if validation['errors']:
        print("\n❌ Errors found:")
        for error in validation['errors']:
            print(f"   - {error}")
    else:
        print("\n✅ No errors found - system is healthy!")

    print(f"\n🎯 System ready with {stats['total_ascii']} ASCII arts!")

if __name__ == "__main__":
    main()