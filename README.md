# 🚀 Cloud-Native Task Manager

A full-stack task management application deployed on AWS EKS with complete CI/CD automation using Terraform and GitHub Actions.

![Architecture](docs/architecture.png)

## 📐 Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                          Internet/Users                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Application Load     │
              │  Balancer (ALB)       │
              └──────────┬───────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌───────────────┐                ┌────────────────┐
│  Frontend     │                │   Backend      │
│  (Nginx)      │                │   (Flask)      │
│  Pods × 2     │───────────────▶│   Pods × 3     │
└───────────────┘                └────────┬───────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │  RDS MySQL   │
                                   │  (Database)  │
                                   └──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AWS EKS Cluster                               │
│  • Auto-scaling (HPA)                                            │
│  • Self-healing                                                  │
│  • Rolling updates                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      CI/CD Pipeline                              │
│  GitHub → Actions → ECR → EKS Deployment                         │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### **Frontend**
- HTML/CSS/JavaScript
- Nginx (Alpine)
- Docker containerized

### **Backend**
- Python Flask
- RESTful API
- Health checks & probes
- Docker containerized

### **Infrastructure**
- **Cloud Provider**: AWS
- **Container Orchestration**: Kubernetes (EKS)
- **IaC**: Terraform
- **Container Registry**: AWS ECR
- **Networking**: VPC, Subnets, NAT Gateway, Internet Gateway
- **Load Balancing**: AWS Application Load Balancer (ALB)
- **Auto-scaling**: Horizontal Pod Autoscaler (HPA)

### **DevOps**
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git

## 📂 Project Structure
```
cloud-native-task-manager/
├── backend/
│   ├── app.py              # Flask API
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── index.html          # UI
│   ├── app.js              # Frontend logic
│   ├── styles.css          # Styling
│   └── Dockerfile          # Frontend container
├── terraform/
│   ├── main.tf             # Provider config
│   ├── variables.tf        # Input variables
│   ├── vpc.tf              # Network infrastructure
│   ├── eks.tf              # Kubernetes cluster
│   ├── ecr.tf              # Container registry
│   └── outputs.tf          # Output values
├── k8s/
│   ├── backend-deployment.yaml   # Backend K8s resources
│   ├── frontend-deployment.yaml  # Frontend K8s resources
│   ├── ingress.yaml             # Load balancer config
│   └── hpa.yaml                 # Auto-scaling config
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline
├── docker-compose.yml       # Local development
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- AWS CLI configured
- Terraform >= 1.0
- kubectl
- GitHub account

### Local Development

1. **Clone the repository**
```bash
   git clone https://github.com/SantiagoAlbi/cloud-native-task-manager.git
   cd cloud-native-task-manager
```

2. **Run with Docker Compose**
```bash
   docker-compose up --build
```

3. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000
   - Health check: http://localhost:5000/health

### AWS Deployment

#### 1. Configure AWS Credentials
```bash
aws configure
```

#### 2. Deploy Infrastructure with Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

This will create:
- VPC with public/private subnets
- EKS Cluster
- ECR repositories
- Security groups
- IAM roles

#### 3. Configure kubectl
```bash
aws eks update-kubeconfig --name task-manager-cluster --region us-east-1
```

#### 4. Build and Push Docker Images
```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
cd backend
docker build -t task-manager-backend .
docker tag task-manager-backend:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/task-manager-backend:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/task-manager-backend:latest

# Build and push frontend
cd ../frontend
docker build -t task-manager-frontend .
docker tag task-manager-frontend:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/task-manager-frontend:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/task-manager-frontend:latest
```

#### 5. Deploy to Kubernetes
```bash
cd ../k8s
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml
```

#### 6. Verify Deployment
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Build**: Creates Docker images on push to main
2. **Test**: Runs health checks
3. **Push**: Uploads images to ECR
4. **Deploy**: Updates EKS deployments
5. **Verify**: Confirms rollout success

### Setup GitHub Secrets

Add these secrets to your repository (Settings → Secrets):

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## 📊 Features

✅ **RESTful API** with CRUD operations  
✅ **Containerized** microservices architecture  
✅ **Auto-scaling** based on CPU usage  
✅ **Self-healing** with Kubernetes  
✅ **Zero-downtime deployments** with rolling updates  
✅ **Health checks** and readiness probes  
✅ **Infrastructure as Code** with Terraform  
✅ **Automated CI/CD** with GitHub Actions  
✅ **Production-ready** security practices  

## 💰 AWS Cost Estimation

| Resource | Monthly Cost (approx) |
|----------|----------------------|
| EKS Cluster | $73 |
| EC2 Nodes (2× t3.small) | $30 |
| NAT Gateway | $32 |
| ALB | $16 |
| **Total** | **~$151/month** |

**Note**: Costs can be reduced by:
- Using spot instances
- Reducing node count
- Destroying resources when not in use

## 🧹 Cleanup

To avoid AWS charges:
```bash
# Delete Kubernetes resources
kubectl delete -f k8s/

# Destroy infrastructure
cd terraform
terraform destroy
```

## 🔮 Future Enhancements

- [ ] Add RDS MySQL for data persistence
- [ ] Implement authentication (JWT)
- [ ] Add monitoring with Prometheus/Grafana
- [ ] Implement logging with ELK stack
- [ ] Add unit and integration tests
- [ ] Implement secrets management with AWS Secrets Manager
- [ ] Add CDN with CloudFront
- [ ] Multi-region deployment

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| POST | `/tasks` | Create new task |
| GET | `/tasks/:id` | Get task by ID |
| PUT | `/tasks/:id` | Update task |
| DELETE | `/tasks/:id` | Delete task |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Santiago Albisetti**

- LinkedIn: [linkedin.com/in/santiagoalbisetti](https://linkedin.com/in/santiagoalbisetti)
- GitHub: [@SantiagoAlbi](https://github.com/SantiagoAlbi)

## 🙏 Acknowledgments

- Built as a portfolio project to demonstrate cloud engineering skills
- Part of my journey transitioning to Cloud Engineering role
- Focus: AWS, Terraform, Docker, Kubernetes, DevOps

---

⭐ If you found this project helpful, please give it a star!
