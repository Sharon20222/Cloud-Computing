```markdown
# Week 6 Homework 2 Project: PySpark on Kubernetes

## Overview

This project involves implementing Word Count and PageRank using PySpark on Apache Spark running on Kubernetes. The steps include setting up a Kubernetes cluster on Google Kubernetes Engine (GKE), deploying Spark, and executing the data processing tasks.

## Prerequisites

- Google Cloud SDK (gcloud)
- Kubernetes CLI (kubectl)
- Docker

## Steps to Implement

### 1. Create a Cluster on GKE

First, create a cluster on GKE and verify its creation:

```sh
gcloud container clusters create spark --num-nodes=1 --machine-type=e2-highmem-2 --region=asia-southeast1
```

### 2. Create Image and Deploy Spark to Kubernetes

#### Add the Stable Helm Repository and Install the NFS Server Provisioner

```sh
helm repo add stable https://charts.helm.sh/stable
helm install nfs-server-provisioner stable/nfs-server-provisioner
```

#### Create a Persistent Disk Volume and a Pod to Use NFS

Apply the following YAML descriptor:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-volume
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /srv/nfs/kubedata
    server: <NFS_SERVER_IP>
```

#### Prepare Your Application JAR File

```sh
docker run -v /tmp:/tmp -it bitnami/spark bash -c 'find /opt/bitnami/spark/examples/jars/ -name spark-examples* -exec cp {} /tmp/my.jar \;'
```

#### Add a Test File for Word Count

Create a test file with a line of words that will be used later for the Word Count test.

#### Copy the JAR File and Test File to the PVC

```sh
kubectl cp /tmp/my.jar <your-pod>:/data/
kubectl cp /path/to/test.txt <your-pod>:/data/
```

#### Ensure the Files Are Inside the Persistent Volume

```sh
kubectl exec -it <your-pod> -- ls /data/
```

### 3. Deploy Apache Spark on Kubernetes

Deploy Apache Spark using the shared volume:

```sh
helm install spark bitnami/spark --set sparkJobNamespace=default
```

### 4. Get the External IP of the Running Pod

```sh
kubectl get svc --namespace default spark-master-svc -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### 5. Word Count on Spark

Submit a Word Count task:

```sh
kubectl run --namespace default spark-client --rm --tty -i --restart='Never' \
  --image docker.io/bitnami/spark:3.0.1-debian-10-r115 \
  -- spark-submit --master spark://<EXTERNAL_IP>:7077 \
  --deploy-mode cluster \
  --class org.apache.spark.examples.JavaWordCount \
  /data/my.jar /data/test.txt
```

Open your browser to view the output of the completed jobs.

### 6. View the Output of the Completed Jobs

Identify the worker node IP address:

```sh
kubectl get pods -o wide | grep <WORKER_NODE_IP>
```

Execute the pod and see the result:

```sh
kubectl exec -it spark-worker-1 -- bash
cd /opt/bitnami/spark/work
```

### 7. Running Python PageRank on PySpark

Execute the Spark master pods and run PageRank:

```sh
kubectl exec -it spark-master-0 -- bash
cd /opt/bitnami/spark/examples/src/main/python
spark-submit pagerank.py /opt 2
```

## Future Work

- Scale the Kubernetes cluster to handle larger datasets.
- Automate the deployment process using CI/CD pipelines.
- Experiment with other data processing algorithms.

## Conclusion

This project provided valuable hands-on experience with deploying and managing Apache Spark on Kubernetes, developing and running PySpark scripts, and troubleshooting various challenges related to cloud infrastructure and big data processing.

## References

- [GKE Cluster Setup](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl)
- [Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html)
- [Bitnami Spark Helm Chart](https://bitnami.com/stack/spark/helm)
```
