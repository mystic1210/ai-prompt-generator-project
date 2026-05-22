# Kubernetes Production Deployment & Security - Professional Guide

**Target Audience:** DevOps Engineers & IT Professionals (3-5+ Years Experience)  
**Skill Level:** Advanced  
**Topic:** Kubernetes Deployment, Scaling, Security, and Best Practices  
**Formats Included:** Technical Guide + YAML Examples + Security Checklist + Performance Optimization + Architecture  
**Created:** April 2026

---

## PART 1: PRODUCTION ARCHITECTURE

### High-Availability Kubernetes Cluster Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LOAD BALANC (CloudFlare/AWS ELB)            │
└────────────────────────┬────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ K8s     │      │ K8s     │      │ K8s     │  (Control Plane HA)
    │Master-1 │      │Master-2 │      │Master-3 │
    └────┬────┘      └────┬────┘      └────┬────┘
         │ etcd           │ etcd           │ etcd
         └────────┬───────┴───────┬───────┘
                  │               │
        ┌─────────────────────────────────┐  (Distributed Database)
        │  etcd Cluster (3 instances)     │
        └─────────────────────────────────┘
                  │ API Server (3 instances)
                  │ Controller Manager (3 instances)
                  │ Scheduler (3 instances)
                  │
    ┌─────────────┼──────────────────────────────────┐
    │             │                                  │
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Worker-1 │  │ Worker-2 │  │ Worker-3 │  │ Worker-N │
│ Kubelet  │  │ Kubelet  │  │ Kubelet  │  │ Kubelet  │
│ Runtime  │  │ Runtime  │  │ Runtime  │  │ Runtime  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │
 ┌───────┐     ┌───────┐     ┌───────┐     ┌───────┐
 │ Pods  │     │ Pods  │     │ Pods  │     │ Pods  │
 └───────┘     └───────┘     └───────┘     └───────┘

Add-ons:
- kube-proxy (networking on each node)
- DNS cluster (CoreDNS)
- Metrics Server (monitoring)
- Network Plugin (Flannel/Calico)
- Storage Classes (PersistentVolumes)
```

---

## PART 2: PRODUCTION-READY DEPLOYMENT MANIFESTS

### 1. Namespace & RBAC Setup

**File: 01-namespace-rbac.yaml**

```yaml
# Create namespace
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: prod

---

# ServiceAccount for deployment
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-deployer
  namespace: production

---

# Role for limited permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-deployment-role
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets"]
  verbs: ["get", "list", "watch", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]

---

# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-deployer-binding
  namespace: production
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-deployment-role
subjects:
- kind: ServiceAccount
  name: app-deployer
  namespace: production
```

---

### 2. ConfigMap & Secrets

**File: 02-config-secrets.yaml**

```yaml
# ConfigMap for non-sensitive configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  CACHE_TTL: "3600"
  API_TIMEOUT: "30"
  # Large config files can be included
  nginx.conf: |
    upstream backend {
      server backend-service:8080;
    }
    server {
      listen 80;
      location / {
        proxy_pass http://backend;
      }
    }

---

# Secret for sensitive data (use External Secrets in production)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
stringData:  # Use stringData for clarity, automatically base64 encoded
  DATABASE_PASSWORD: "your-secure-password"
  API_KEY: "your-api-key"
  JWT_SECRET: "your-jwt-secret"

---

# Docker Registry Secret (for private images)
apiVersion: v1
kind: Secret
metadata:
  name: docker-registry
  namespace: production
type: kubernetes.io/dockercfg
data:
  .dockercfg: <base64-encoded-registry-credentials>
```

**Best Practice:** Use tools like HashiCorp Vault or AWS Secrets Manager instead of Kubernetes Secrets for production.

---

### 3. Deployment with Advanced Configuration

**File: 03-deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-api
  namespace: production
  labels:
    app: api
    version: v1
spec:
  replicas: 3  # High availability
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero downtime deployments
  
  selector:
    matchLabels:
      app: api
  
  template:
    metadata:
      labels:
        app: api
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    
    spec:
      serviceAccountName: app-deployer
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      
      # Pod disruption budget (for maintenance)
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: api
      
      containers:
      - name: api
        image: myregistry.azurecr.io/app-api:1.2.3  # Specific version tag
        imagePullPolicy: IfNotPresent
        
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP
        
        # Environment variables
        env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_ENV
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_PASSWORD
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        
        # Resource requests & limits (CRITICAL for production)
        resources:
          requests:
            cpu: 250m        # Guaranteed minimum
            memory: 256Mi
          limits:
            cpu: 1000m       # Maximum allowed
            memory: 1024Mi
        
        # Health checks
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        
        # Startup probe (for slow-starting apps)
        startupProbe:
          httpGet:
            path: /health/startup
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 10
          failureThreshold: 30
        
        # Volume mounts
        volumeMounts:
        - name: config
          mountPath: /etc/config
          readOnly: true
        - name: logs
          mountPath: /var/log
        - name: cache
          mountPath: /tmp/cache
        
        # Security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
      
      # Init container (runs before app)
      initContainers:
      - name: migrations
        image: myregistry.azurecr.io/app-api:1.2.3
        command: ["./manage.py", "migrate"]
        env:
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_PASSWORD
      
      # Volumes
      volumes:
      - name: config
        configMap:
          name: app-config
      - name: logs
        emptyDir: {}
      - name: cache
        emptyDir:
          sizeLimit: 1Gi
      
      # Node affinity (schedule on specific nodes)
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: workload
                operator: In
                values:
                - production
        
        # Pod anti-affinity (spread across nodes)
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - api
              topologyKey: kubernetes.io/hostname
      
      # DNS policy
      dnsPolicy: ClusterFirst
      
      # Termination grace period
      terminationGracePeriodSeconds: 30
      
      # Image pull secrets
      imagePullSecrets:
      - name: docker-registry
```

---

### 4. Service & Ingress

**File: 04-service-ingress.yaml**

```yaml
# Service (internal networking)
apiVersion: v1
kind: Service
metadata:
  name: app-api
  namespace: production
  labels:
    app: api
spec:
  type: ClusterIP
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  selector:
    app: api

---

# Ingress (external access with TLS)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.example.com
    secretName: app-api-tls
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-api
            port:
              number: 80
```

---

### 5. Horizontal Pod Autoscaler

**File: 05-hpa.yaml**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-api
  
  minReplicas: 3
  maxReplicas: 10
  
  metrics:
  # CPU-based scaling
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  
  # Memory-based scaling
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 30
      selectPolicy: Max
```

---

## PART 3: SECURITY BEST PRACTICES CHECKLIST

### Network Security

- [ ] **Network Policies configured**
  ```yaml
  # Default deny all ingress
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: default-deny-ingress
  spec:
    podSelector: {}
    policyTypes:
    - Ingress
  ```

- [ ] **Pod Security Policy enabled** (or Pod Security Standards)
- [ ] **Service mesh (Istio) for mTLS** between pods
- [ ] **Ingress Controller with TLS**
- [ ] **VPC with private subnets** for cluster

### Container Security

- [ ] **Non-root user** in all containers
- [ ] **Read-only root filesystem**
- [ ] **No privileged containers**
- [ ] **Resource limits** set
- [ ] **Security context** applied
- [ ] **Image scanning** for vulnerabilities
- [ ] **Signed images** from trusted registry

### Access Control

- [ ] **RBAC** enabled and configured
- [ ] **Service accounts** with least privilege
- [ ] **API audit logging** enabled
- [ ] **kubectl access** restricted with role-based access
- [ ] **Secrets encrypted at rest** (etcd encryption)

### Data Protection

- [ ] **PersistentVolumes encrypted**
- [ ] **Database passwords in Vault**
- [ ] **TLS for all communications**
- [ ] **Backup strategy** implemented
- [ ] **Disaster recovery plan** in place

---

## PART 4: MONITORING & OBSERVABILITY

### Prometheus Metrics

```yaml
# ServiceMonitor cr Prometheus scraping
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-api
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  endpoints:
  - port: metrics
    interval: 30s
```

### Common Metrics to Monitor

```
- Container CPU usage
- Container memory usage
- Pod restart count
- Network I/O bytes
- HTTP request latency
- HTTP error rate
- Database connection pool usage
- Queue depth (if using queues)
```

---

## PART 5: PERFORMANCE OPTIMIZATION GUIDE

### Optimization Techniques

1. **Resource Requests/Limits**
   - Set accurate requests (for scheduling)
   - Set limits (for protection)

2. **Pod Disruption Budgets**
   ```yaml
   minAvailable: 2  # Always keep 2 pods running
   ```

3. **Node Affinity**
   - Use specific node pools for different workloads
   - Separate compute-heavy from I/O-heavy apps

4. **Vertical Pod Autoscaling**
   ```bash
   kubectl autoscale deployment app-api --min=3 --max=10
   ```

5. **Image Optimization**
   - Use distroless base images
   - Multi-stage builds
   - Keep image size < 200MB

---

## PART 6: COMMON ISSUES & SOLUTIONS

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| **Pods not scheduling** | `kubectl describe pod` | Check node resources, affinity rules |
| **Slow pod startup** | Long startup time | Add startup probe, optimize init container |
| **OOMKilled pods** | Memory limit too low | Increase memory limit, check for leaks |
| **Connection timeouts** | Network policy issues | Check NetworkPolicy rules |
| **Secrets not mounted** | Volume not mounted | Check volumeMounts, secret names |
| **Images not pulling** | ImagePullBackOff | Check registry credentials |

---

## PART 7: DEPLOYMENT CHECKLIST

- [ ] All YAML files validated with `kubeval`
- [ ] Resource requests/limits set
- [ ] Security context applied
- [ ] Health checks configured
- [ ] Network policies in place
- [ ] Secrets encrypted
- [ ] RBAC configured
- [ ] Monitoring enabled
- [ ] Logging configured
- [ ] Backup tested
- [ ] Runbook created
- [ ] Load testing completed
- [ ] Chaos engineering tests passed

---

## NEXT STEPS

1. Configure your cluster
2. Deploy manifests in order (01 → 05)
3. Monitor with Prometheus/Grafana
4. Implement GitOps (ArgoCD/Flux)
5. Plan for multi-region setup

---

*Production Enterprise-Grade Guide | Advanced | Ready for Production Deployment*  
*Created: April 2026 | Security-Focused | Best Practices Included*
