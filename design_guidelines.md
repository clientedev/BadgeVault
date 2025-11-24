# Design Guidelines: Controle de Badges

## Design Approach
**Selected System:** Material Design 3 approach with focus on data visualization and dashboard patterns
**Justification:** Information-dense application requiring clear hierarchy, structured data display, and productivity-focused interactions. Material's card-based systems and emphasis on data presentation align perfectly with badge collection and metrics tracking.

## Typography Hierarchy

**Font Family:** 
- Primary: Inter (Google Fonts) - clean, readable for data
- Monospace: JetBrains Mono - for URLs and technical information

**Scale:**
- Page Title (h1): text-3xl font-bold (Controle de Badges)
- Section Headers (h2): text-2xl font-semibold (Métricas Gerais, Alunos)
- Card Titles: text-lg font-medium (student names)
- Body Text: text-base font-normal (descriptions, counts)
- Labels/Metadata: text-sm font-medium (badge counts, links)
- Input Labels: text-sm font-medium

## Layout System

**Spacing Units:** Tailwind units of 3, 4, 6, 8, 12 for consistent rhythm
- Component padding: p-6
- Card spacing: gap-6
- Section margins: mb-8 to mb-12
- Input groups: space-y-4

**Container Structure:**
- Main container: max-w-7xl mx-auto px-4 sm:px-6 lg:px-8
- Content sections: py-8
- Cards: max-w-sm for individual student cards

## Component Library

### 1. Input Form Section
**Layout:** Single column, centered, max-w-2xl
- Large text input field with placeholder "Cole o link do perfil aqui..."
- Height: h-12 with rounded-lg borders
- Submit button: Full-width on mobile, inline on desktop
- Helper text below input explaining supported platforms (Google Cloud Skills, Credly)
- Visual feedback area for processing state

### 2. Metrics Dashboard
**Layout:** Grid layout - grid-cols-1 md:grid-cols-3 gap-6
Three metric cards displaying:
- Total de Badges (aggregate count)
- Total de Alunos (student count)
- Média por Aluno (average calculation)

Each metric card structure:
- Large numeric display: text-4xl font-bold
- Label below: text-sm text-muted
- Icon accent (trophy, users, chart icons from Heroicons)
- Padding: p-6
- Elevated appearance with subtle shadow

### 3. Student Cards Grid
**Layout:** grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6

Individual student card:
- Clickable entire card (cursor-pointer with hover elevation)
- Card padding: p-6
- Top section: Student name (text-lg font-semibold)
- Badge count display: Large number (text-3xl font-bold) with "badges" label
- Platform indicator: Small chip showing "Google Cloud" or "Credly"
- External link icon in top-right corner
- Bottom: Truncated URL display (text-xs, monospace, text-muted)
- Hover state: Subtle transform and shadow increase

### 4. Empty State
When no students added yet:
- Centered illustration placeholder area
- Friendly message: "Adicione o primeiro aluno"
- Instructions pointing to input form above

### 5. Navigation/Header
**Layout:** Sticky header, full-width
- Left: App title "Controle de Badges" with small badge icon
- Right: User indicators showing "Gabriel e Johnny"
- Height: h-16
- Border bottom for visual separation

## Page Structure (Top to Bottom)

1. **Header** (h-16, sticky top-0)
2. **Input Section** (py-8, bg-subtle for visual separation)
3. **Metrics Dashboard** (py-12)
4. **Students Grid** (py-8, min-h-screen for content)

## Icons
**Library:** Heroicons (outline style)
- Trophy icon for badges
- Users icon for students
- Chart-bar icon for metrics
- External-link icon for card links
- Plus icon for add actions
- Check-circle for success states

## Component Behavior

**Card Interactions:**
- Entire card is clickable link wrapper
- Opens profile in new tab (target="_blank")
- Smooth hover transition (transition-all duration-200)
- Hover: Slight scale (scale-105) and shadow increase

**Form Interaction:**
- Input validation for URL format
- Loading state during scraping process
- Success/error toast notifications positioned top-right
- Disabled state for button during processing

**Responsive Behavior:**
- Mobile: Single column stacking
- Tablet: 2-column grid for students
- Desktop: 3-column grid for students, inline form button

## Accessibility
- All interactive elements have focus states (focus:ring-2)
- Proper heading hierarchy (h1 → h2 structure)
- Form labels associated with inputs
- Aria-labels for icon-only buttons
- Sufficient color contrast for all text
- Keyboard navigation for all interactions