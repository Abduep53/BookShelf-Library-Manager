# 🚀 Automated Render Deployment Helper Script
# This script opens necessary pages and provides step-by-step guidance

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🚀 BOOKSHELF - AUTOMATED RENDER DEPLOYMENT HELPER" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if logged in
Write-Host "📋 STEP 1: Opening Render Blueprint Dashboard..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "https://dashboard.render.com/blueprints"

Write-Host ""
Write-Host "   ✓ Render dashboard opened in browser" -ForegroundColor Green
Write-Host ""
Write-Host "   🔐 If not logged in:" -ForegroundColor Cyan
Write-Host "      1. Sign in to your Render account" -ForegroundColor White
Write-Host "      2. Or create a free account at render.com" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter when logged in..." -ForegroundColor Yellow
Read-Host

# Step 2: Connect Repository
Write-Host ""
Write-Host "📋 STEP 2: Connect Your GitHub Repository" -ForegroundColor Yellow
Write-Host ""
Write-Host "   In the Render Dashboard:" -ForegroundColor Cyan
Write-Host "   1. Click 'New +' button → 'Blueprint'" -ForegroundColor White
Write-Host "   2. Connect your GitHub account (if not connected)" -ForegroundColor White
Write-Host "   3. Search for: BookShelf-Library-Manager" -ForegroundColor White
Write-Host "   4. Select the repository" -ForegroundColor White
Write-Host "   5. Click 'Connect'" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter when repository is connected..." -ForegroundColor Yellow
Read-Host

# Step 3: Configure Blueprint
Write-Host ""
Write-Host "📋 STEP 3: Apply Blueprint Configuration" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Render will automatically detect render.yaml:" -ForegroundColor Cyan
Write-Host "   ✓ Web Service: bookshelf-app (Python)" -ForegroundColor Green
Write-Host "   ✓ Database: bookshelf-db (PostgreSQL)" -ForegroundColor Green
Write-Host "   ✓ Auto-deploy: Enabled" -ForegroundColor Green
Write-Host ""
Write-Host "   Click 'Apply' to create services" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter after clicking Apply..." -ForegroundColor Yellow
Read-Host

# Step 4: Set Environment Variable
Write-Host ""
Write-Host "📋 STEP 4: Configure OpenAI API Key" -ForegroundColor Yellow
Start-Sleep -Seconds 1

Write-Host ""
Write-Host "   Opening service environment settings..." -ForegroundColor Cyan
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "   In the Render Dashboard:" -ForegroundColor Cyan
Write-Host "   1. Go to 'bookshelf-app' service" -ForegroundColor White
Write-Host "   2. Navigate to 'Environment' tab" -ForegroundColor White
Write-Host "   3. Add new environment variable:" -ForegroundColor White
Write-Host "      - Key: OPENAI_API_KEY" -ForegroundColor Yellow
Write-Host "      - Value: your-openai-api-key" -ForegroundColor Yellow
Write-Host "   4. Click 'Save Changes'" -ForegroundColor White
Write-Host ""
Write-Host "   📝 Other variables are auto-configured:" -ForegroundColor Cyan
Write-Host "      ✓ SECRET_KEY (auto-generated)" -ForegroundColor Green
Write-Host "      ✓ DEBUG=False" -ForegroundColor Green
Write-Host "      ✓ DATABASE_URL (auto-connected)" -ForegroundColor Green
Write-Host ""
Write-Host "Press Enter after saving environment variables..." -ForegroundColor Yellow
Read-Host

# Step 5: Monitor Deployment
Write-Host ""
Write-Host "📋 STEP 5: Monitor Deployment" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Build process started automatically!" -ForegroundColor Cyan
Write-Host "   Expected time: 5-10 minutes" -ForegroundColor White
Write-Host ""
Write-Host "   Build steps:" -ForegroundColor Cyan
Write-Host "   1. ⏳ Installing dependencies..." -ForegroundColor White
Write-Host "   2. ⏳ Collecting static files..." -ForegroundColor White
Write-Host "   3. ⏳ Running database migrations..." -ForegroundColor White
Write-Host "   4. ⏳ Starting Gunicorn server..." -ForegroundColor White
Write-Host ""
Write-Host "   Monitor logs in: Dashboard → bookshelf-app → Logs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Enter when deployment is complete (status: 'Live')..." -ForegroundColor Yellow
Read-Host

# Step 6: Success!
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "   🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "   Your BookShelf app is now live! 🚀" -ForegroundColor Cyan
Write-Host ""
Write-Host "   📊 Service URL:" -ForegroundColor Yellow
Write-Host "   https://bookshelf-app.onrender.com" -ForegroundColor White
Write-Host ""
Write-Host "   (Check your Render dashboard for the exact URL)" -ForegroundColor Gray
Write-Host ""
Write-Host "   ✅ Features Available:" -ForegroundColor Cyan
Write-Host "      - User Authentication and Dashboard" -ForegroundColor White
Write-Host "      - Book Library Management" -ForegroundColor White
Write-Host "      - AI Book Summarizer" -ForegroundColor White
Write-Host "      - AI Book Recommender" -ForegroundColor White
Write-Host "      - AI Quiz Generator" -ForegroundColor White
Write-Host ""
Write-Host "   🔄 Auto-Deployment Enabled:" -ForegroundColor Cyan
Write-Host "      Every push to 'master' branch triggers new deployment" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host ""
Write-Host "Press Enter to open your live site..." -ForegroundColor Yellow
Read-Host

Start-Process "https://bookshelf-app.onrender.com"

Write-Host ""
Write-Host "Thank you for using the automated deployment helper! 🎉" -ForegroundColor Green
Write-Host ""

