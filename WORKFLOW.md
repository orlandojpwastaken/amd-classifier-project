# Azure Deployment Workflow

## Prerequisites

- Azure for Students account (free $100-200 credits)
- Azure CLI installed
- Docker images built locally

## Step 1: Setup Azure

```bash
# install azure cli (windows)
winget install Microsoft.AzureCLI

# login
az login

# verify subscription
az account show
```

## Step 2: Create Azure Container Registry

```bash
# create resource group
az group create --name amd-detection-rg --location eastus

# create container registry
az acr create --resource-group amd-detection-rg --name amddetectionacr --sku Basic

# login to acr
az acr login --name amddetectionacr
```

## Step 3: Push Docker Images

```bash
# tag images
docker tag dsfinalproject-backend amddetectionacr.azurecr.io/amd-backend:latest
docker tag dsfinalproject-frontend amddetectionacr.azurecr.io/amd-frontend:latest

# push to acr
docker push amddetectionacr.azurecr.io/amd-backend:latest
docker push amddetectionacr.azurecr.io/amd-frontend:latest
```

## Step 4: Create AKS Cluster

```bash
# create aks cluster (2 nodes)
az aks create \
  --resource-group amd-detection-rg \
  --name amd-cluster \
  --node-count 2 \
  --enable-managed-identity \
  --attach-acr amddetectionacr

# get credentials
az aks get-credentials --resource-group amd-detection-rg --name amd-cluster
```

## Step 5: Update Kubernetes Manifests

Edit `kubernetes/backend-deployment.yaml` and `kubernetes/frontend-deployment.yaml`:

```yaml
# change image paths to:
image: amddetectionacr.azurecr.io/amd-backend:latest
image: amddetectionacr.azurecr.io/amd-frontend:latest
```

## Step 6: Deploy to AKS

```bash
# apply all manifests
kubectl apply -f kubernetes/

# check status
kubectl get pods
kubectl get services

# get external ip (wait for EXTERNAL-IP to appear)
kubectl get service amd-frontend-service --watch
```

## Step 7: Access Application

Once external IP is assigned:
```
http://<EXTERNAL-IP>
```

## Useful Commands

```bash
# view logs
kubectl logs <pod-name>

# describe pod
kubectl describe pod <pod-name>

# restart deployment
kubectl rollout restart deployment amd-backend
kubectl rollout restart deployment amd-frontend

# delete everything
kubectl delete -f kubernetes/

# delete azure resources
az group delete --name amd-detection-rg
```