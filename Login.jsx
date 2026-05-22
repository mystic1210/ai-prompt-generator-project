# Kubernetes Deployment Configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prompt-generator-backend
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prompt-generator-backend
  template:
    metadata:
      labels:
        app: prompt-generator-backend
    spec:
      containers:
      - name: backend
        image: docker.io/prompt-generator-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: secret-key
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
          limits:
            cpu: "500m"
            memory: "1Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: prompt-generator-backend
spec:
  selector:
    app: prompt-generator-backend
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prompt-generator-frontend
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: prompt-generator-frontend
  template:
    metadata:
      labels:
        app: prompt-generator-frontend
    spec:
      containers:
      - name: frontend
        image: docker.io/prompt-generator-frontend:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            cpu: "100m"
            memory: "256Mi"
          limits:
            cpu: "200m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: prompt-generator-frontend
spec:
  selector:
    app: prompt-generator-frontend
  ports:
  - protocol: TCP
    port: 3000
    targetPort: 3000
  type: LoadBalancer
