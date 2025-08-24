# Render Deployment Guide for Django Shopping Website

## Prerequisites
- Render account (sign up at https://render.com)
- GitHub account with the project repository

## Deployment Steps

### 1. Prepare Your Repository
- Push your code to a GitHub repository
- Ensure all files are committed

### 2. Create a Render Web Service
1. Go to https://dashboard.render.com/
2. Click "New +" and select "Web Service"
3. Connect your GitHub account and select your repository
4. Configure the service:
   - **Name**: shoppingproject
   - **Environment**: Python
   - **Region**: Choose the closest region to your users
   - **Branch**: main (or your preferred branch)
   - **Root Directory**: (leave empty if root)
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn shoppingproject.wsgi:application`

### 3. Set Environment Variables
In the Render dashboard, go to your service → Environment → Add Environment Variables:

- `SECRET_KEY`: Generate a strong secret key
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `.onrender.com`
- `RAZORPAY_KEY_ID`: Your Razorpay key ID
- `RAZORPAY_KEY_SECRET`: Your Razorpay key secret
- `PYTHON_VERSION`: `3.11.0`

### 4. Database Configuration (Optional)
For production, consider using:
- Render PostgreSQL (free tier available)
- Or configure your MySQL database connection

Update `DATABASES` in `settings.py` for your production database.

### 5. Deploy
- Render will automatically deploy when you push to the connected branch
- Monitor the build logs in the Render dashboard

### 6. Post-Deployment
- Test your application at the provided Render URL
- Set up custom domain if needed
- Configure SSL certificate

## Important Notes
- Static files are served from `staticfiles/` directory
- Media files may need cloud storage (S3, etc.) for production
- Monitor application logs in the Render dashboard
- Set up automatic deployments from your main branch

## Troubleshooting
- Check build logs for any errors
- Ensure all environment variables are set correctly
- Verify database connections if using external database
