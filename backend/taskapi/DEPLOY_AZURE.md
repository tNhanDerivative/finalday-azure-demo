# Deploy Django DRF to Azure App Service (Linux)

## 1) Prerequisites
- Azure CLI installed (`az --version`)
- Logged in Azure account
- Run commands from project root: `taskapi/taskapi`

## 2) Files prepared in this repo
- `requirements.txt`
- `startup.sh`
- `.env.example`
- Production-friendly settings in `taskapi/settings.py`

## 3) Set variables
```bash
RG="rg-taskapi"
LOCATION="southeastasia"
PLAN="asp-taskapi-dev"
APP="taskapi-demo"
RUNTIME="PYTHON:3.11"

SECRET_KEY_VALUE="replace-with-a-strong-secret"
FRONTEND_ORIGIN="https://your-frontend-domain.com"
PGHOST="<server-name>.postgres.database.azure.com"
PGDATABASE="<database-name>"
PGUSER="<db-user>"
PGPASSWORD="<db-password>"
```

## 4) Login and select subscription
```bash
az login
az account list -o table
az account set --subscription "<SUBSCRIPTION_ID_OR_NAME>"
```

## 5) Create resource group and App Service
```bash
az group create --name "$RG" --location "$LOCATION"

az appservice plan create \
  --name "$PLAN" \
  --resource-group "$RG" \
  --is-linux \
  --sku B1

az webapp create \
  --resource-group "$RG" \
  --plan "$PLAN" \
  --name "$APP" \
  --runtime "$RUNTIME"
```

## 6) Configure startup command and app settings
```bash
az webapp config set \
  --resource-group "$RG" \
  --name "$APP" \
  --startup-file "bash startup.sh"

az webapp config appsettings set \
  --resource-group "$RG" \
  --name "$APP" \
  --settings \
    DJANGO_ENV="production" \
    SECRET_KEY="$SECRET_KEY_VALUE" \
    ALLOWED_HOSTS="$APP.azurewebsites.net" \
    CORS_ALLOW_ALL_ORIGINS="False" \
    CORS_ALLOWED_ORIGINS="$FRONTEND_ORIGIN" \
    CSRF_TRUSTED_ORIGINS="$FRONTEND_ORIGIN,https://$APP.azurewebsites.net" \
    POSTGRES_HOST="$PGHOST" \
    POSTGRES_PORT="5432" \
    POSTGRES_DB="$PGDATABASE" \
    POSTGRES_USER="$PGUSER" \
    POSTGRES_PASSWORD="$PGPASSWORD" \
    POSTGRES_SSLMODE="require"
```

## 7) Deploy code from terminal (zip deploy)
```bash
zip -r app.zip . -x ".venv/*" "__pycache__/*" "*.pyc" "db.sqlite3" "staticfiles/*" ".git/*"

az webapp deploy \
  --resource-group "$RG" \
  --name "$APP" \
  --src-path app.zip \
  --type zip
```

## 8) Verify deployment
```bash
az webapp show --resource-group "$RG" --name "$APP" --query defaultHostName -o tsv
# open https://<output-hostname>/tasks
```

## 9) View logs when troubleshooting
```bash
az webapp log config \
  --resource-group "$RG" \
  --name "$APP" \
  --application-logging filesystem \
  --level information

az webapp log tail --resource-group "$RG" --name "$APP"
```

## 10) Optional: deploy in one command (`az webapp up`)
```bash
az webapp up \
  --name "$APP" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --runtime "$RUNTIME" \
  --sku B1
```

After `az webapp up`, still run section 6 to set startup file and app settings.
