# Frontend Setup Guide - Enhanced UI Version

## Prerequisites

- **Node.js**: v16.14.0 or higher
- **npm**: v7.0.0 or higher (or yarn/pnpm)
- **Git**: For version control

Check your versions:
```bash
node --version
npm --version
```

---

## Installation Steps

### Step 1: Install Dependencies

Navigate to the frontend directory:
```bash
cd frontend
```

Install all npm packages including new UI libraries:
```bash
npm install
```

This installs:
- React 18 and Vite
- Framer Motion (animations)
- Lucide React (icons)
- Radix UI primitives
- TailwindCSS and utilities
- All other dependencies

**Expected Installation Time**: 2-5 minutes

### Step 2: Verify Installation

Check that all dependencies installed correctly:
```bash
npm ls
```

You should see:
```
├── framer-motion@10.16.0
├── lucide-react@0.292.0
├── @radix-ui/* (multiple packages)
├── react@18.x.x
├── vite@*
└── tailwindcss@3.x.x
```

---

## Environment Configuration

### Step 1: Create .env.local File

In the `frontend` directory, create `.env.local`:
```bash
touch .env.local
```

### Step 2: Add Environment Variables

Add the following content to `.env.local`:
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AI Prompt Generator
```

**Development Values**:
- `VITE_API_URL`: Backend API endpoint (local dev: http://localhost:8000/api)
- `VITE_APP_NAME`: Application display name

**Production Values** (when deploying):
```env
VITE_API_URL=https://api.yourdomain.com/api
VITE_APP_NAME=AI Prompt Generator
```

---

## Development Server

### Start the Development Server

```bash
npm run dev
```

**Expected Output**:
```
VITE v5.0.0  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Press h to show help
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should see:
- **Login page** if not authenticated
- **Navigation bar** with gradient background
- **Smooth animations** on page load
- **Lucide icons** throughout

---

## Development Tips

### Hot Module Replacement (HMR)

Vite automatically reloads your browser when you save files. No manual refresh needed!

```bash
# File changes automatically detected
# Components re-render instantly
# State is preserved (when possible)
```

### Console Debugging

Open DevTools (F12) to:
- Check for console errors
- Inspect animations in Performance tab
- Verify API calls in Network tab
- Use React DevTools extension

### File Structure Reference

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # UI components
│   │   ├── Navigation.jsx (Enhanced)
│   │   └── ProtectedRoute.jsx
│   ├── pages/          # Page components
│   │   ├── Login.jsx (Enhanced)
│   │   ├── PromptCreate.jsx (Enhanced)
│   │   ├── PromptList.jsx (Enhanced)
│   │   └── Dashboard.jsx (Enhanced)
│   ├── store/          # Zustand state
│   │   └── authStore.js
│   ├── api/            # API client
│   │   └── client.js
│   ├── App.jsx         # Main router
│   └── main.jsx        # Entry point
├── package.json        # Dependencies (v2.0.0)
├── vite.config.js      # Vite configuration
└── tailwind.config.js  # Tailwind config
```

---

## Building for Production

### Step 1: Build the Application

```bash
npm run build
```

**What happens**:
- React code compiled to optimized bundle
- TailwindCSS purged (unused styles removed)
- Framer Motion optimized for production
- Output written to `dist/` folder

**Expected Output**:
```
dist/index.html              2.5 kB │ gzip:  1.2 kB
dist/assets/main.js      150.2 kB │ gzip: 45.3 kB
dist/assets/style.css     85.4 kB │ gzip: 12.1 kB
```

### Step 2: Preview Production Build

Test the production build locally:
```bash
npm run preview
```

Opens a local server to preview the built application.

### Step 3: Deploy to Production

The `dist/` folder contains everything needed for deployment:

**Option 1: Vercel**
```bash
npm install -g vercel
vercel
```

**Option 2: Netlify**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

**Option 3: Docker**
See `deployment/Dockerfile.frontend`

**Option 4: Traditional Hosting**
Upload `dist/` folder to any static host (AWS S3, GitHub Pages, etc.)

---

## Troubleshooting

### Issue: "Cannot find module 'lucide-react'"

**Solution**:
```bash
npm install lucide-react --save
npm run dev
```

### Issue: "Framer Motion animations not working"

**Solution**:
```bash
# Clear node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Restart dev server
npm run dev
```

### Issue: "Tailwind styles not applying"

**Solution**:
1. Check `tailwind.config.js` includes correct paths
2. Ensure `src/index.css` imports Tailwind directives
3. Restart dev server

### Issue: "Port 5173 already in use"

**Solution**:
```bash
# Use different port
npm run dev -- --port 3100

# Or kill process using port 5173
# On Windows: netstat -ano | findstr :5173
# On Mac/Linux: lsof -i :5173
```

### Issue: "API calls fail with CORS error"

**Solution**:
1. Ensure backend is running on `http://localhost:8000`
2. Check backend CORS settings in `backend/main.py`
3. Verify `VITE_API_URL` in `.env.local` matches backend URL

### Issue: "Authentication state not persisting"

**Solution**:
1. Check browser localStorage (DevTools > Application > Local Storage)
2. Verify JWT token is being stored
3. Clear browser cookies/cache and retry login

---

## Performance Optimization

### Bundle Size Analysis

Check what's in your bundle:
```bash
npm run build -- --analyze
```

Or use online tools:
- [Bundle Analyzer](https://bundlephobia.com)
- [Webpack Bundle Analyzer](https://github.com/webpack-bundle-analyzer/webpack-bundle-analyzer)

### Lighthouse Audit

Test performance in Chrome DevTools:
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Click "Analyze page load"
4. Review performance score and recommendations

**Target Scores**:
- Performance: > 90
- Accessibility: > 95
- Best Practices: > 90
- SEO: > 90

---

## Testing Your Installation

### Quick Verification Steps

1. **Start dev server**:
   ```bash
   npm run dev
   ```

2. **Open browser**:
   ```
   http://localhost:5173
   ```

3. **Check for**:
   - [ ] Gradient login page loads
   - [ ] Logo and navigation visible
   - [ ] Smooth animations on hover
   - [ ] Lucide icons display correctly
   - [ ] No console errors (F12)

4. **Test key features**:
   - [ ] Can type in form fields
   - [ ] Submit button works
   - [ ] Animations trigger on interaction
   - [ ] Mobile responsive (resize browser)

5. **Backend connectivity**:
   - [ ] Check Network tab (F12)
   - [ ] Verify API calls to `http://localhost:8000/api`
   - [ ] Look for 200 OK responses

---

## Code Quality Tools

### Linting (Optional Setup)

Install ESLint:
```bash
npm install -D eslint @typescript-eslint/parser
npm run lint
```

### Code Formatting (Optional Setup)

Install Prettier:
```bash
npm install -D prettier
npm run format
```

---

## Environment Variables Reference

### Available Variables

```env
# API Configuration
VITE_API_URL=http://localhost:8000/api     # Backend API endpoint
VITE_API_TIMEOUT=30000                     # Request timeout (ms)

# App Configuration
VITE_APP_NAME=AI Prompt Generator           # Display name
VITE_APP_VERSION=2.0.0                      # App version

# Feature Flags
VITE_ENABLE_ANALYTICS=false                 # Google Analytics
VITE_ENABLE_DARK_MODE=true                  # Dark mode support
VITE_LOG_LEVEL=info                         # Console log level
```

### Development vs Production

**Development (.env.local)**:
```env
VITE_API_URL=http://localhost:8000/api
VITE_LOG_LEVEL=debug
```

**Production (.env.production)**:
```env
VITE_API_URL=https://api.yourdomain.com/api
VITE_LOG_LEVEL=warn
```

---

## Common Commands

```bash
# Development
npm run dev              # Start dev server
npm run dev -- --open   # Start and auto-open browser

# Building
npm run build            # Build for production
npm run preview          # Preview production build
npm run build -- --analyze  # Analyze bundle size

# Code Quality
npm run lint             # Run ESLint
npm run format           # Format code with Prettier
npm run type-check       # Check TypeScript types

# Utilities
npm list                 # List all dependencies
npm update               # Update all dependencies
npm prune                # Remove unused packages
```

---

## Docker Setup (Optional)

Build and run in Docker:

```bash
# Build image
docker build -f deployment/Dockerfile.frontend -t ai-prompt-frontend:latest .

# Run container
docker run -p 3000:80 ai-prompt-frontend:latest

# Access at: http://localhost:3000
```

---

## Next Steps

After completing setup:

1. [OK] **Verify Installation**: Run through verification steps above
2. [INFO] **Explore Components**: Open each page and interact with UI
3. [DESIGN] **Test Animations**: Hover over buttons, navigate between pages
4. [LINK] **Connect Backend**: Ensure API calls work (check Network tab)
5. [MOBILE] **Test Responsive**: Resize browser, test on mobile
6. [DEPLOY] **Deploy**: Build and deploy to your hosting platform

---

## Support Resources

- **Framer Motion Docs**: https://www.framer.com/motion/
- **Lucide Icons**: https://lucide.dev
- **TailwindCSS**: https://tailwindcss.com/docs
- **React Docs**: https://react.dev
- **Vite Guide**: https://vitejs.dev/guide/

---

## Deployment Checklist

Before deploying to production:

- [ ] Run `npm run build` without errors
- [ ] Test production build locally with `npm run preview`
- [ ] Update `.env` variables for production
- [ ] Verify all API endpoints work
- [ ] Test on target devices/browsers
- [ ] Run Lighthouse audit (target >90 scores)
- [ ] Clear browser cache
- [ ] Upload `dist/` folder to hosting

---

## Version Information

**Current Frontend Version**: 2.0.0

**Key Upgrades in v2.0.0**:
- Shadcn/ui component library
- Framer Motion animations
- Lucide Icons integration
- Enhanced gradient styling
- Optimized performance
- Improved responsive design
- Better accessibility

---

**Setup complete! Start developing with:**
```bash
npm run dev
```

Happy coding!
