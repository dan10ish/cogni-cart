# AI Chat Frontend

A modern chat interface built with Next.js, TypeScript, and Shadcn UI that connects to the FastAPI backend for AI-powered conversations.

## Features

- **Next.js 15**: Latest React framework with App Router
- **TypeScript**: Full type safety
- **Shadcn UI**: Beautiful, accessible UI components
- **Tailwind CSS**: Utility-first CSS framework
- **Real-time Chat**: Interactive chat interface with loading states
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Graceful error handling with user feedback

## Prerequisites

- Node.js 18+
- npm or yarn
- Running backend server (see backend README)

## Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

## Running the Application

### Development Mode
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

The application will be available at `http://localhost:3000`

## Features Overview

### Chat Interface
- Clean, modern chat UI with message bubbles
- User messages appear on the right (blue)
- AI responses appear on the left (gray)
- Loading indicator with animated dots
- Auto-scroll to latest messages

### Input Controls
- Large textarea for message input
- Send button with loading states
- Keyboard shortcut: Press Enter to send (Shift+Enter for new line)
- Input validation and disabled states

### Error Handling
- Connection error messages
- Backend availability checks
- User-friendly error notifications

## UI Components

This project uses [Shadcn UI](https://ui.shadcn.com/) components:

- **Button**: Interactive buttons with various states
- **Card**: Container components for the chat interface
- **Textarea**: Multi-line text input
- **Input**: Single-line text input (available for future use)

## Project Structure

```
frontend/
├── app/
│   ├── globals.css      # Global styles and Shadcn theming
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Main chat interface
├── components/
│   └── ui/              # Shadcn UI components
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       └── textarea.tsx
├── lib/
│   └── utils.ts         # Utility functions
├── components.json      # Shadcn configuration
├── next.config.ts       # Next.js configuration
├── tailwind.config.ts   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies and scripts
```

## Configuration

### Backend Connection
The frontend is configured to connect to the backend at `http://localhost:8000`. If your backend runs on a different port, update the fetch URL in `app/page.tsx`:

```typescript
const response = await fetch("http://localhost:8000/generate", {
  // ... rest of the configuration
});
```

### Styling
The application uses a neutral color scheme from Shadcn UI. To customize:

1. **Colors**: Modify CSS variables in `app/globals.css`
2. **Components**: Customize Shadcn components in `components/ui/`
3. **Layout**: Adjust responsive breakpoints in Tailwind classes

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint

## Dependencies

### Core
- `next`: React framework
- `react`: React library
- `typescript`: Type safety

### UI & Styling
- `@tailwindcss/postcss`: CSS processing
- `tailwindcss`: Utility-first CSS
- `class-variance-authority`: Component variants
- `clsx`: Conditional classes
- `tailwind-merge`: Tailwind class merging

### Shadcn UI
- `@radix-ui/*`: Headless UI primitives
- `lucide-react`: Icon library

## Customization

### Adding New Shadcn Components
```bash
npx shadcn@latest add [component-name]
```

### Modifying the Chat Interface
The main chat logic is in `app/page.tsx`. Key areas to customize:

- **Message rendering**: Modify the `messages.map()` section
- **API calls**: Update the `sendMessage()` function
- **Styling**: Adjust Tailwind classes
- **Error handling**: Enhance the try/catch blocks

### Responsive Design
The interface is designed mobile-first with responsive breakpoints:

- **Mobile**: Default styles
- **Tablet**: `sm:` prefix
- **Desktop**: `md:` and `lg:` prefixes

## Troubleshooting

### Backend Connection Issues
1. Ensure the backend is running on port 8000
2. Check for CORS errors in browser console
3. Verify the backend URL in the fetch request

### UI Issues
1. Clear Next.js cache: `rm -rf .next`
2. Reinstall dependencies: `rm -rf node_modules && npm install`
3. Check for TypeScript errors: `npm run build`

### Development Issues
1. Check browser console for errors
2. Verify environment variables
3. Ensure Node.js version compatibility
