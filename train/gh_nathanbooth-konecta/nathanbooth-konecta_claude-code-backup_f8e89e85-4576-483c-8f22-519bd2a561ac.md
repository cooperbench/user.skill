> DEVELOPER

can you give me a least priviledge list of permissions needed to successfully run the terraform script

> AGENT

Let me examine the Terraform configurations to identify all resources and determine the minimum permissions needed.

> AGENT

Here's the least-privilege permissions breakdown for running this Terraform, organized by project and resource type.

---

## GKE Project (`kd-ix-eur-{env}-gke`)

### Service Accounts
```
iam.serviceAccounts.create
iam.serviceAccounts.get
iam.serviceAccounts.delete
iam.serviceAccounts.update
iam.serviceAccounts.getIamPolicy
iam.serviceAccounts.setIamPolicy
```

### GCS Buckets + HMAC Keys
```
storage.buckets.create
storage.buckets.get
storage.buckets.update
storage.buckets.delete
storage.buckets.getIamPolicy
storage.buckets.setIamPolicy
storage.hmacKeys.create
storage.hmacKeys.get
storage.hmacKeys.delete
storage.hmacKeys.list
storage.hmacKeys.update
```

### Secret Manager
```
secretmanager.secrets.create
secretmanager.secrets.get
secretmanager.secrets.delete
secretmanager.secrets.update
secretmanager.secrets.getIamPolicy
secretmanager.secrets.setIamPolicy
secretmanager.versions.add
secretmanager.versions.get
secretmanager.versions.access
secretmanager.versions.destroy
```

### Artifact Registry
```
artifactregistry.repositories.create
artifactregistry.repositories.get
artifactregistry.repositories.delete
artifactregistry.repositories.update
artifactregistry.repositories.getIamPolicy
artifactregistry.repositories.setIamPolicy
```

### GKE Cluster Access
```
container.clusters.get
container.clusters.getCredentials
```

### Project Metadata
```
resourcemanager.projects.get
resourcemanager.projects.getIamPolicy
```

---

## Platform Data Project (`kd-ix-eur-{env}-platform-data`)

### Cloud SQL
```
cloudsql.databases.create
cloudsql.databases.get
cloudsql.databases.delete
cloudsql.databases.update
cloudsql.databases.list
cloudsql.instances.get
cloudsql.instances.list
cloudsql.users.create
cloudsql.users.get
cloudsql.users.delete
cloudsql.users.update
cloudsql.users.list
```

### Project IAM (for cross-project role bindings)
```
resourcemanager.projects.get
resourcemanager.projects.getIamPolicy
resourcemanager.projects.setIamPolicy
```

---

## Terraform State Bucket (`kd-tfstate-{env}`)

```
storage.buckets.get
storage.objects.create
storage.objects.get
storage.objects.delete
storage.objects.update
storage.objects.list
```

---

## Kubernetes RBAC (on the GKE cluster)

```yaml
# Core resources (namespaces, secrets, service accounts, quotas)
apiGroups: [""]
resources: [namespaces, secrets, serviceaccounts, resourcequotas, limitranges]
verbs: [create, get, list, update, delete, patch]

# RBAC
apiGroups: ["rbac.authorization.k8s.io"]
resources: [roles, rolebindings, clusterroles, clusterrolebindings]
verbs: [create, get, list, update, delete, patch]

# Network policies
apiGroups: ["networking.k8s.io"]
resources: [networkpolicies]
verbs: [create, get, list, update, delete, patch]
```

---

## Predefined Role Equivalent

If you prefer predefined roles over a custom role, the closest mapping is:

| Project | Role |
|---------|------|
| GKE project | `roles/iam.serviceAccountAdmin` |
| GKE project | `roles/storage.admin` |
| GKE project | `roles/secretmanager.admin` |
| GKE project | `roles/artifactregistry.admin` |
| GKE project | `roles/container.developer` |
| Platform Data project | `roles/cloudsql.admin` |
| Platform Data project | `roles/resourcemanager.projectIamAdmin` |
| State bucket | `roles/storage.objectAdmin` (scoped to bucket) |
| GKE cluster | `cluster-admin` ClusterRoleBinding |

The custom role approach (using only the individual permissions listed above) is tighter but requires more setup. The predefined roles are broader than strictly necessary but simpler to manage.
