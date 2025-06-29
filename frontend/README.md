# CogniCart Frontend

A minimal ChatGPT-style interface built with Next.js, TypeScript, and Shadcn UI that connects to the AI-powered shopping assistant backend.

## Features

- **ChatGPT-style Interface**: Clean, conversational UI with minimal design
- **Dark Mode**: Default dark theme for better user experience
- **Process Visualization**: Real-time display of backend processing steps
- **Product Results**: Minimal product cards with Indian Rupee currency
- **Responsive Design**: Optimized for desktop and mobile
- **Real-time Loading**: Animated process steps during search
- **Bold Text Formatting**: Proper rendering of bold text from AI responses

## Recent Changes

### Complete Frontend Redesign
- Replaced complex card-based layout with ChatGPT-style conversation interface
- Implemented dark mode as default theme
- Added real-time process step visualization
- Simplified product display with minimal cards
- Changed currency from USD ($) to Indian Rupee (₹)
- Removed unnecessary components and modals for cleaner experience
- Added proper bold text formatting (** markdown to HTML bold)

### Removed Components
- `search-interface.tsx` - Replaced with inline search input
- `product-card.tsx` - Replaced with `product-result.tsx`
- `product-details-modal.tsx` - Simplified to inline display

### New Components
- `process-step.tsx` - Shows backend processing with animated steps
- `product-result.tsx` - Minimal product display with rupee symbols

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

## Interface Overview

### Main Layout
- **Header**: Simple branding with CogniCart logo
- **Chat Area**: Scrollable conversation view with user/assistant messages
- **Input Area**: Fixed bottom input with send button

### Message Types
- **User Messages**: Right-aligned with user avatar
- **Assistant Messages**: Left-aligned with bot avatar
- **Process Steps**: Animated loading indicators showing backend progress
- **Product Results**: Minimal cards showing product information

### Process Visualization
The interface shows real-time backend processing steps:
- Understanding your query...
- Searching product database...
- Analyzing products...
- Generating recommendations...

### Product Display
Products are shown with:
- Product title and brand
- Star ratings and review counts
- Key features (first 3 displayed)
- Indian Rupee pricing with proper formatting
- Review summaries when available
- Deal information if applicable

## Project Structure

```
frontend/
├── app/
│   ├── globals.css      # Global styles with dark mode theme
│   ├── layout.tsx       # Root layout with dark mode enabled
│   └── page.tsx         # Main ChatGPT-style interface
├── components/
│   ├── process-step.tsx # Backend process visualization
│   ├── product-result.tsx # Minimal product display
│   └── ui/              # Shadcn UI components
├── components.json      # Shadcn configuration
├── next.config.ts       # Next.js configuration
├── tailwind.config.ts   # Tailwind CSS configuration
└── package.json         # Dependencies and scripts
```

## Key Features

### Dark Mode
- Enabled by default in layout.tsx
- Uses Shadcn UI dark theme variables
- Consistent across all components

### Currency Formatting
- All prices display in Indian Rupees (₹)
- Proper number formatting with Indian locale
- Rupee icon from Lucide React

### Text Formatting
- Markdown-style ** bold ** converted to HTML <strong>
- Line breaks preserved in AI responses
- Clean typography with proper spacing

### Process Steps
- 4-step animated process during searches
- Icons change every second during loading
- Provides user feedback for backend processing

## Configuration

### Backend Connection
Update the backend URL in `app/page.tsx` if needed:

```typescript
const response = await fetch("http://localhost:8000/search", {
  // ... configuration
});
```

### Customization
- **Colors**: Modify CSS variables in `app/globals.css`
- **Process Steps**: Update steps array in `components/process-step.tsx`
- **Product Layout**: Customize `components/product-result.tsx`

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
- `tailwindcss`: Utility-first CSS
- `@radix-ui/*`: Headless UI primitives
- `lucide-react`: Icon library (includes IndianRupee icon)
- `class-variance-authority`: Component variants

## Usage

1. Type your shopping query in the input field
2. Press Enter or click Send button
3. Watch the animated process steps
4. View AI response and product results
5. Click "View" on products for more details

## Troubleshooting

### Backend Connection
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify API endpoints are accessible

### UI Issues
- Clear browser cache if styles don't load
- Check that dark mode is properly applied
- Verify all components are properly imported
