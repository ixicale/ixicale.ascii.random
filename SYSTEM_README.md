# ASCII Art Random Generator - Modular System

Un generador de ASCII art aleatorio completamente refactorizado con un sistema modular que facilita la gestión y expansión de la colección.

## 🚀 Nuevo Sistema Modular

### Estructura de Archivos

```
ascii_arts/
├── animals/
│   ├── metadata.json          # Información de la categoría
│   ├── neko_001.txt           # ASCII art individual
│   ├── neko_002.txt
│   └── ...
├── emotions/
│   ├── metadata.json
│   ├── smile_001.txt
│   └── ...
└── ...
```

### Características Principales

- ✅ **Modular**: ASCII arts separados en archivos individuales
- ✅ **Organizado**: Categorías claras con metadatos estructurados
- ✅ **Extensible**: Fácil agregar nuevos ASCII arts sin tocar código
- ✅ **Buscable**: Sistema de tags y búsqueda avanzada
- ✅ **Validado**: Verificación automática de integridad
- ✅ **Retrocompatible**: Funciona con la API original

## 📋 Comandos Disponibles

### Uso Principal (run.py)

```bash
# ASCII aleatorio (comportamiento original)
python run.py

# ASCII aleatorio de una categoría específica
python run.py --category animals

# Buscar ASCII arts
python run.py --search "neko"

# ASCII por tags
python run.py --random --tags "cat,cute"

# Listar todas las categorías
python run.py --categories

# Estadísticas del sistema
python run.py --stats

# Ver todos los nombres disponibles
python run.py --list

# Obtener ASCII específico por nombre
python run.py --name "neko 001"
```

### Agregar Nuevos ASCII Arts

```bash
# Modo interactivo (recomendado)
python add_ascii.py

# Ver categorías disponibles
python add_ascii.py --list-categories

# Desde archivo
python add_ascii.py --file mi_ascii.txt --name "nuevo ascii" --category misc --tags "tag1,tag2"
```

### Generar Documentación

```bash
# Generar toda la documentación
python generate_preview.py

# Solo README principal
python generate_preview.py --full-only

# Solo una categoría
python generate_preview.py --category animals

# Incluir contenido NSFW
python generate_preview.py --include-nsfw
```

### Validación del Sistema

```bash
# Verificar integridad del sistema
python validate_system.py
```

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **ascii_loader.py**: Carga ASCII arts desde archivos
2. **ascii_manager.py**: Gestor principal con funcionalidades avanzadas
3. **run.py**: Interfaz de línea de comandos refactorizada
4. **add_ascii.py**: Herramienta para agregar nuevos ASCII arts
5. **generate_preview.py**: Generador de documentación
6. **validate_system.py**: Validador del sistema

### Formato de Metadatos

Cada categoría tiene un archivo `metadata.json`:

```json
{
  "category": "animals",
  "nsfw": false,
  "description": "Cute and adorable animal ASCII arts",
  "files": [
    {
      "name": "neko_001",
      "original_name": "neko 001",
      "tags": ["cat", "kawaii", "animals", "cute"],
      "nsfw": false
    }
  ]
}
```

## 📊 Estadísticas Actuales

- **Categorías**: 5 (animals, emotions, misc, nsfw, people)
- **ASCII Arts Totales**: 52
- **ASCII Arts Seguros**: 47
- **ASCII Arts NSFW**: 5
- **Tags Únicos**: 59

## 🔧 Para Desarrolladores

### Agregar Nueva Funcionalidad

1. Usar `ASCIIManager` como interfaz principal
2. Extender `ASCIILoader` para nuevas fuentes de datos
3. Mantener compatibilidad con formato de metadatos

### Ejemplo de Uso Programático

```python
from ascii_manager import ASCIIManager

manager = ASCIIManager()

# Obtener ASCII aleatorio
ascii_data = manager.get_random_ascii(category="animals")
print(ascii_data['content'])

# Buscar ASCII arts
results = manager.search_and_get_ascii("neko")
for result in results:
    print(f"Found: {result['original_name']}")
```

## 🚀 Migración desde Sistema Anterior

- El archivo `run_legacy.py` contiene el sistema original
- `migrate_ascii.py` realiza la migración automática
- El nuevo sistema es 100% retrocompatible con comandos básicos

## 🤝 Contribuir

1. Usar `python add_ascii.py` para agregar nuevos ASCII arts
2. Seguir las convenciones de nomenclatura existentes
3. Validar con `python validate_system.py`
4. Generar documentación con `python generate_preview.py`

## 📝 Changelog

### v2.0 - Sistema Modular
- ✨ Arquitectura modular completa
- ✨ Sistema de categorías y tags
- ✨ Herramientas de gestión automatizadas
- ✨ Búsqueda y filtrado avanzado
- ✨ Generación automática de documentación
- ✨ Validación de integridad del sistema

### v1.0 - Sistema Original
- 🎨 Generador básico de ASCII art aleatorio
- 📝 ASCII arts hardcodeados en diccionario
- 🔞 Filtro NSFW básico

---

**¡El nuevo sistema está listo! 🎉**

Ahora es más fácil que nunca agregar, gestionar y explorar ASCII arts.