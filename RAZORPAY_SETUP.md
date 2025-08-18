# Razorpay Setup Guide

## Issue: Razorpay Authenticate Key Missing

This guide will help you properly configure Razorpay payment integration in your Django shopping application.

## Prerequisites

1. **Razorpay Account**: You need a Razorpay account. Sign up at [https://razorpay.com](https://razorpay.com)
2. **API Keys**: Get your API keys from the Razorpay Dashboard

## Step 1: Get Your Razorpay API Keys

1. Login to your Razorpay Dashboard: https://dashboard.razorpay.com
2. Navigate to Settings → API Keys
3. Copy your **Key ID** and **Key Secret**
4. For testing, use the **Test Mode** keys (they start with `rzp_test_`)

## Step 2: Configure Environment Variables

### Option 1: Using .env file (Recommended)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Razorpay keys:
   ```bash
   RAZORPAY_KEY_ID=your_actual_key_id_here
   RAZORPAY_KEY_SECRET=your_actual_key_secret_here
   ```

### Option 2: Using System Environment Variables

Set the environment variables in your terminal:

**Windows (Command Prompt):**
```cmd
set RAZORPAY_KEY_ID=your_actual_key_id_here
set RAZORPAY_KEY_SECRET=your_actual_key_secret_here
```

**Windows (PowerShell):**
```powershell
$env:RAZORPAY_KEY_ID="your_actual_key_id_here"
$env:RAZORPAY_KEY_SECRET="your_actual_key_secret_here"
```

**Linux/Mac:**
```bash
export RAZORPAY_KEY_ID=your_actual_key_id_here
export RAZORPAY_KEY_SECRET=your_actual_key_secret_here
```

## Step 3: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

## Step 4: Verify Configuration

1. **Check if keys are loaded**:
   ```python
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.RAZORPAY_KEY_ID)
   >>> print(settings.RAZORPAY_KEY_SECRET)
   ```

2. **Test Razorpay client initialization**:
   ```python
   >>> import razorpay
   >>> from django.conf import settings
   >>> client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
   >>> client.order.all()
   ```

## Step 5: Common Issues and Solutions

### Issue 1: "Razorpay credentials are missing"
**Solution**: Ensure your `.env` file exists and contains valid keys.

### Issue 2: "Invalid API Key"
**Solution**: 
- Check if you're using test keys for test mode
- Verify the keys are correctly copied from the Razorpay dashboard
- Ensure there are no extra spaces or characters

### Issue 3: "KeyError: 'RAZORPAY_KEY_ID'"
**Solution**: Install python-decouple:
```bash
pip install python-decouple
```

## Step 6: Testing the Integration

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Test the payment flow**:
   - Add items to cart
   - Go to checkout
   - Use Razorpay test card: `4111 1111 1111 1111`
   - Use any future expiry date and any 3-digit CVV

## Test Cards for Razorpay

Use these test card numbers:
- **Success**: 4111 1111 1111 1111
- **Failure**: 4000 0000 0000 0002
- **OTP Failure**: 4000 0000 0000 0119

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Use test keys** during development
4. **Switch to live keys** only in production
5. **Regularly rotate keys** for security

## Production Deployment

When deploying to production:

1. Switch to **Live Mode** keys
2. Update the Razorpay webhook URL
3. Ensure HTTPS is enabled
4. Set up proper error handling and logging

## Support

If you encounter issues:
1. Check Razorpay documentation: https://razorpay.com/docs/
2. Verify your API keys
3. Check server logs for detailed error messages
4. Test with Razorpay's test environment first
