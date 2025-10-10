# Vercel Deployment Guide - Static Files Fix

## Problems Identified & Fixed

### Issue 1: Static Files Routing Conflict

**Problem:** The `vercel.json` was trying to redirect `/static/` URLs to `/staticfiles/`, which interfered with WhiteNoise's ability to serve static files through the WSGI application.

**Solution:** Simplified the routing to pass ALL requests through the WSGI application, letting WhiteNoise handle static files properly.

### Issue 2: WhiteNoise Development Settings in Production

**Problem:** WhiteNoise was configured with development settings (`WHITENOISE_USE_FINDERS = True` and `WHITENOISE_AUTOREFRESH = True`) which don't work well on Vercel.

**Solution:** Updated WhiteNoise settings to production-appropriate values.

### Issue 3: Missing Build Command

**Problem:** Vercel wasn't collecting static files during build.

**Solution:** Added explicit `buildCommand` to `vercel.json` to ensure static files are collected.

## Changes Made

### 1. Updated `vercel.json`

- Simplified routing to let WhiteNoise handle all static files
- Added `buildCommand` to collect static files during deployment
- Removed conflicting static file routes

### 2. Updated `config/settings.py`

- Changed `WHITENOISE_USE_FINDERS` to `False` (production setting)
- Changed `WHITENOISE_AUTOREFRESH` to `False` (production setting)

### 3. Created `.vercelignore`

- Added file to exclude unnecessary files from deployment
- Reduces deployment size and improves performance

## How to Deploy to Vercel

### Step 1: Commit Your Changes

```bash
git add .
git commit -m "Fix static files configuration for Vercel deployment"
git push origin main
```

### Step 2: Deploy to Vercel

If you're using Vercel CLI:

```bash
vercel --prod
```

Or if you're using Vercel Dashboard:

1. Go to your project on Vercel
2. Go to Settings → Git
3. Click "Redeploy" for the latest commit

### Step 3: Set Environment Variables

Make sure these environment variables are set in your Vercel project:

**Required:**

- `SECRET_KEY` - Your Django secret key
- `DATABASE_URL` - Your PostgreSQL database URL (if using Postgres)
- `ALLOWED_HOSTS` - Your Vercel domain (e.g., `your-project.vercel.app`)

**Optional (for email):**

- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`

**For Debug (set to False in production):**

- `DEBUG` - Set to `False` for production

To set environment variables in Vercel:

1. Go to your project on Vercel
2. Go to Settings → Environment Variables
3. Add each variable with its value
4. Redeploy after adding variables

### Step 4: Verify Deployment

After deployment, check:

1. **Admin Panel**: Visit `https://your-project.vercel.app/admin/`

   - The admin panel should have proper styling
   - Django JET theme should load correctly

2. **Static Files**: Check browser console (F12)

   - No 404 errors for CSS/JS files
   - Static files should load from `/static/` URLs

3. **Images**: Verify that images are displaying correctly on your pages

## Troubleshooting

### Admin Panel Still Not Styled?

1. Check Vercel build logs to ensure `collectstatic` ran successfully
2. Verify `SECRET_KEY` is set in environment variables
3. Check browser console for any 404 errors on static files

### Static Files 404 Errors?

1. Run locally: `python manage.py collectstatic --noinput
2. Verify `staticfiles` directory is created with files
3. Check that `whitenoise` is in your `requirements.txt`

### Database Errors?

1. Ensure `DATABASE_URL` is set correctly
2. Check that migrations ran during build
3. Verify PostgreSQL database is accessible from Vercel

### Images Not Loading?

**Note:** User-uploaded images (media files) won't persist on Vercel because it's a serverless platform. For user uploads, you need to use cloud storage like:

- AWS S3
- Cloudinary
- Google Cloud Storage

Static images (in `base/static/base/images/`) should work fine.

## Testing Locally Before Deploy

To test the production configuration locally:

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn (similar to production)
pip install gunicorn
gunicorn config.wsgi:app

# Or use the Django development server
python manage.py runserver
```

Then visit:

- http://localhost:8000/admin/ - Check admin styling
- http://localhost:8000/ - Check your site

## Additional Notes

- **StaticFiles Storage**: Using `CompressedManifestStaticFilesStorage` which compresses files and creates hashed versions for cache busting
- **WhiteNoise**: Serves static files efficiently in production without needing a separate web server
- **Media Files**: If you need persistent media file storage, integrate with a cloud storage service

## Quick Reference - Common Vercel Commands

```bash
# Install Vercel CLI globally
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to preview (test deployment)
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# Open project in browser
vercel --open
```

## Support

If you still face issues:

1. Check Vercel build logs: Project → Deployments → [Latest] → Build Logs
2. Check runtime logs: Project → Deployments → [Latest] → Functions
3. Verify all environment variables are set correctly
