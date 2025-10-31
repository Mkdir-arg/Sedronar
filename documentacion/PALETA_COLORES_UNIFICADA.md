# Paleta de Colores Unificada - SEDRONAR

## Descripción General

Se ha implementado una paleta de colores unificada y formal para todo el sistema SEDRONAR, reemplazando las múltiples paletas inconsistentes que existían anteriormente.

## Paleta Principal

### Colores Primarios (Azul Institucional)
- **Primario**: `#1e3a8a` - Azul institucional principal
- **Primario Claro**: `#3b82f6` - Azul primario claro
- **Primario Oscuro**: `#1e40af` - Azul primario oscuro

### Colores Secundarios (Gris Azulado Profesional)
- **Secundario**: `#475569` - Gris azulado profesional
- **Secundario Claro**: `#64748b` - Gris azulado claro
- **Secundario Oscuro**: `#334155` - Gris azulado oscuro

### Colores de Acento (Verde Azulado Formal)
- **Acento**: `#0f766e` - Verde azulado formal
- **Acento Claro**: `#14b8a6` - Verde azulado claro
- **Acento Oscuro**: `#0d9488` - Verde azulado oscuro

### Colores de Estado
- **Éxito**: `#059669` (Verde)
- **Advertencia**: `#d97706` (Naranja)
- **Error**: `#dc2626` (Rojo)
- **Información**: `#2563eb` (Azul)

## Variables CSS Disponibles

### Colores Base
```css
--color-primario: #1e3a8a
--color-primario-claro: #3b82f6
--color-primario-oscuro: #1e40af
--color-secundario: #475569
--color-acento: #0f766e
--color-acento-claro: #14b8a6
```

### Fondos
```css
--fondo-principal: #f8fafc
--fondo-secundario: #ffffff
--fondo-sidebar: linear-gradient(135deg, var(--color-primario) 0%, var(--color-primario-oscuro) 100%)
--fondo-header: var(--color-primario)
```

### Textos
```css
--texto-primario: var(--color-gris-900)
--texto-secundario: var(--color-gris-600)
--texto-blanco: var(--color-blanco)
```

## Clases Utilitarias

### Fondos
- `.bg-primario` - Fondo azul institucional
- `.bg-secundario` - Fondo gris profesional
- `.bg-acento` - Fondo verde azulado
- `.bg-exito` - Fondo verde éxito
- `.bg-advertencia` - Fondo naranja advertencia
- `.bg-error` - Fondo rojo error

### Textos
- `.text-primario` - Texto azul institucional
- `.text-secundario` - Texto gris profesional
- `.text-acento` - Texto verde azulado

### Componentes
- `.btn-primario` - Botón con estilo primario
- `.card-unificada` - Tarjeta con estilo unificado
- `.alert-exito` - Alerta de éxito
- `.badge-primario` - Badge con color primario

## Archivos Actualizados

1. **`paleta-unificada.css`** - Archivo principal con todas las variables y clases
2. **`base.html`** - Configuración de Tailwind actualizada
3. **`main.css`** - Sidebar, header y footer actualizados
4. **`login.html`** - Página de login completamente actualizada
5. **`navbar.html`** - Barra de navegación actualizada
6. **`sidebar/base.html`** - Sidebar actualizado
7. **`dashboard.css`** - Cards del dashboard actualizadas
8. **`custom.css`** - Badges y alertas actualizadas

## Beneficios de la Unificación

### Consistencia Visual
- Todos los componentes usan la misma paleta
- Experiencia de usuario coherente
- Aspecto más profesional y formal

### Mantenibilidad
- Variables CSS centralizadas
- Fácil cambio de colores en toda la aplicación
- Menos código duplicado

### Accesibilidad
- Colores con buen contraste
- Cumple estándares de accesibilidad web
- Legibilidad mejorada

## Uso Recomendado

### Para Desarrolladores
1. Usar siempre las variables CSS en lugar de colores hardcodeados
2. Utilizar las clases utilitarias cuando sea posible
3. Mantener la consistencia en nuevos componentes

### Ejemplo de Uso
```css
/* ❌ Incorrecto */
.mi-componente {
    background-color: #1e3a8a;
    color: #ffffff;
}

/* ✅ Correcto */
.mi-componente {
    background-color: var(--color-primario);
    color: var(--color-blanco);
}
```

```html
<!-- ❌ Incorrecto -->
<button class="bg-blue-600 text-white">Botón</button>

<!-- ✅ Correcto -->
<button class="btn-primario">Botón</button>
```

## Compatibilidad

- ✅ Compatible con Tailwind CSS
- ✅ Compatible con Bootstrap (si se usa)
- ✅ Soporte para modo oscuro
- ✅ Responsive design

## Próximos Pasos

1. Revisar componentes restantes que puedan necesitar actualización
2. Crear guía de estilo visual completa
3. Implementar modo oscuro completo si es necesario
4. Documentar patrones de diseño específicos del sistema