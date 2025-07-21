### Mala Lingo Frontend

Vue3
Composition API

### Architecture
```
src/
├── components/
│   ├── ui/                    # Reusable UI components
│   │   ├── Button.vue         # Enhanced button with variants
│   │   ├── LoadingSpinner.vue # Configurable loading states
│   │   ├── ErrorMessage.vue   # Error handling with retry
│   │   └── GameHeader.vue     # Game titles and instructions
│   ├── game/                  # Game-specific components
│   │   ├── GameStatus.vue     # Score tracking and actions
│   │   ├── FlipCard.vue       # 3D flip card animations
│   │   └── WordCard.vue       # Interactive word selection
│   └── layout/                # Layout components
│       └── AppNavigation.vue  # Main navigation
├── composables/               # Shared reactive logic
│   ├── useWordData.js         # API data management
│   └── useGameState.js        # Game state management
├── utils/                     # Constants and helpers
│   └── constants.js           # App-wide constants
├── views/                     # Page components
│   ├── Home.vue               # Landing page with typing animation
│   ├── MatchingWords.vue      # Word matching game
│   └── FlipTest.vue           # Flashcard game
├── stores/                    # Pinia state management
│   └── auth.js                # Authentication store
└── router/                    # Vue Router configuration
    └── index.js               # Route definitions
```

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Game Components

### Word Matching Game
- **Component**: `MatchingWords.vue`
- **Logic**: `useMatchingGame()` composable
- **Features**: 
  - Word matching
  - Real-time score tracking
  - Completion celebration
  - Reset functionality

### Flip Card Test
- **Component**: `FlipTest.vue`
- **Logic**: `useFlipCardGame()` composable
- **Features**:
  - Progress tracking
  - New cards generation
  - Reset all cards
