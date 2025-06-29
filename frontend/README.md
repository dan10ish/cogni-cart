# CogniCart Frontend

A minimal ChatGPT-style interface with **real-time streaming** built with Next.js, TypeScript, and Shadcn UI that connects to the AI-powered shopping assistant backend.

## ✨ Latest Features (Updated)

### 🚀 Real-Time Streaming
- **Live Process Steps**: Shows actual backend processing steps in real-time
- **Server-Sent Events (SSE)**: Streams data from backend as it processes
- **Typing Animation**: Shows live progress while AI analyzes products
- **Process Visualization**: Displays steps like "🎯 Understanding query", "🚀 Searching database", "📊 Analyzing products"

### 🎨 Enhanced Interface
- **Sticky Header**: Header stays fixed during scroll with branding and links
- **Personal Links**: Quick access to portfolio (dan10ish.github.io) and GitHub repo
- **Sticky Avatars**: Chat avatars stick to top during long conversations
- **Improved Input**: Better responsive input area that stays at bottom
- **Dark Mode**: Consistent dark theme throughout the application

### 🛒 Working Product Links
- **Real URLs**: Each product links to actual Amazon India pages
- **Click to Buy**: "View" buttons open actual product pages
- **Fallback Search**: If no URL available, falls back to Google search
- **External Link Indicators**: Clear icons showing external navigation

### 💰 Indian Market Focus
- **Rupee Currency (₹)**: All prices displayed in Indian Rupees
- **Indian Formatting**: Proper number formatting for Indian locale
- **Amazon India**: Direct links to Amazon.in product pages
- **Localized Content**: Pricing and availability for Indian market

## Features

- **ChatGPT-style Interface**: Clean, conversational UI with minimal design
- **Real-Time Streaming**: Live updates showing backend AI processing steps
- **Dark Mode**: Default dark theme for better user experience
- **Process Visualization**: Real-time display of backend processing steps
- **Product Results**: Minimal product cards with working Amazon links
- **Responsive Design**: Optimized for desktop and mobile
- **Bold Text Formatting**: Proper rendering of bold text from AI responses
- **Sticky Elements**: Header and input area remain accessible during scroll

## Recent Major Updates

### Complete Streaming Implementation
- Added Server-Sent Events (SSE) support for real-time updates
- Backend now streams process steps as they happen
- Frontend displays live progress with animated indicators
- Shows actual backend logs: "Understanding query", "Found X products", "Analyzing product 1", etc.

### UI/UX Improvements
- **Sticky Header**: Fixed header with CogniCart branding and tagline
- **Personal Links**: Added portfolio and GitHub links with appropriate icons
- **Better Avatars**: Chat avatars now stick to visible area during scroll
- **Enhanced Input**: Improved bottom input area with better styling
- **Product Cards**: Clickable cards with working Amazon India links

### Working Product Integration
- **Real URLs**: Products now have working links to Amazon India
- **Fixed View Buttons**: Each product's "View" button opens the actual product page
- **Better Error Handling**: Shows appropriate fallbacks when links unavailable
- **External Link Safety**: Opens links in new tabs with security measures

### Backend Streaming Support
- **New Endpoint**: `/search-stream` for real-time updates
- **Process Broadcasting**: Backend broadcasts each processing step
- **Better Error Handling**: Streams errors and recovery steps
- **Maintains Compatibility**: Original `/search` endpoint still works

## Project Structure

```
frontend/
├── app/
│   ├── globals.css      # Global styles with dark mode theme
│   ├── layout.tsx       # Root layout with dark mode enabled
│   └── page.tsx         # Main streaming ChatGPT-style interface
├── components/
│   ├── process-step.tsx # Real-time backend process visualization
│   ├── product-result.tsx # Product cards with working Amazon links
│   └── ui/              # Shadcn UI components
├── components.json      # Shadcn configuration
├── next.config.ts       # Next.js configuration
├── tailwind.config.ts   # Tailwind CSS configuration
└── package.json         # Dependencies and scripts
```

## Key Technical Features

### Streaming Implementation
- **EventSource Alternative**: Custom SSE handling with fetch streams
- **Real-Time Updates**: Live process steps as backend executes
- **Buffer Management**: Proper handling of streamed data chunks
- **Error Recovery**: Graceful handling of connection issues

### UI Components
- **ProcessStep Component**: Shows current and previous processing steps
- **ProductResult Component**: Enhanced product cards with working links
- **Sticky Elements**: Header and input area with backdrop blur effects
- **Responsive Design**: Mobile-first with proper breakpoints

### Product Integration
- **Amazon Integration**: Direct links to Amazon India product pages
- **URL Validation**: Checks for valid product URLs before linking
- **Fallback Mechanism**: Google search fallback for missing URLs
- **External Link Handling**: Secure external link opening

## Configuration

### Backend Connection
The frontend connects to both streaming and standard endpoints:

```typescript
// Streaming endpoint for real-time updates
const response = await fetch("http://localhost:8000/search-stream", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: inputQuery }),
});

// Standard endpoint (fallback)
const response = await fetch("http://localhost:8000/search", {
  // ... configuration
});
```

### Personal Links
Update the header links in `app/page.tsx`:

```typescript
// Portfolio link
onClick={() => window.open("https://dan10ish.github.io", "_blank")}

// GitHub repository link  
onClick={() => window.open("https://github.com/dan10ish/cogni-cart", "_blank")}
```

### Customization
- **Colors**: Modify CSS variables in `app/globals.css`
- **Process Steps**: Backend streams actual process steps
- **Product Layout**: Customize `components/product-result.tsx`
- **Header Content**: Update branding and links in main page component

## Available Scripts

- `npm run dev`: Start development server with hot reload
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint

## Dependencies

### Core
- `next`: React framework with App Router
- `react`: React library with hooks
- `typescript`: Type safety and better development experience

### UI & Styling
- `tailwindcss`: Utility-first CSS framework
- `@radix-ui/*`: Headless UI primitives for accessibility
- `lucide-react`: Icon library (includes IndianRupee, Github, User icons)
- `class-variance-authority`: Component variants

## Usage Guide

### Basic Search
1. Type your shopping query in the input field
2. Press Enter or click Send button
3. Watch real-time process steps as AI works
4. View AI response with formatted text
5. Click "View" on any product to open Amazon page

### Streaming Features
- **Live Updates**: See each processing step as it happens
- **Progress Tracking**: Visual indicators show current and completed steps
- **Error Handling**: Real-time error reporting with recovery suggestions
- **Rich Formatting**: Bold text, proper currency formatting, line breaks

### Navigation
- **Portfolio Link**: Click user icon in header to visit dan10ish.github.io
- **GitHub Repo**: Click GitHub icon to view project repository
- **Product Links**: Click "View" button on products to open Amazon India pages
- **Sticky Elements**: Header and input remain accessible during scroll

## Troubleshooting

### Streaming Issues
- **Connection Errors**: Check if backend is running on port 8000
- **SSE Problems**: Verify CORS headers in backend configuration
- **Process Steps Not Showing**: Ensure `/search-stream` endpoint is available

### Product Link Issues
- **Amazon Links Not Working**: Products should have valid `url` field
- **View Button Not Responding**: Check browser console for errors
- **External Links Blocked**: Ensure popup blocker allows new tabs

### UI/Performance Issues
- **Sticky Elements Not Working**: Verify CSS backdrop-blur support
- **Dark Mode Issues**: Check CSS variables in globals.css
- **Mobile Responsiveness**: Test responsive breakpoints

## Development Notes

### Backend Requirements
- Backend must implement `/search-stream` endpoint
- Proper CORS configuration for streaming
- SSE format: `data: {JSON}\n\n`

### Browser Compatibility
- **Modern Browsers**: Requires EventSource/Stream support
- **Mobile Browsers**: Full responsive design included
- **Accessibility**: Uses Radix UI primitives for better a11y

This frontend provides a modern, responsive, and feature-rich interface for the CogniCart AI shopping assistant with real-time streaming capabilities and working product integration.
