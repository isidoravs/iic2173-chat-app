# Chat app

IIC2173 - Entrega Final Arquitectura de Sistemas de Software

## Integrantes

| Nombre               | Número de alumno |
| -------------------- | ---------------- |
| Tomás Alvarez        | 1563700J         |
| Francisco Larach     | 15634957         |
| Miguel Ramírez       | 15633438         |
| Florencia Valladares | 1463614J         |
| Isidora Vizcaya      | 15633144         |

## Desafíos

### (1) Make my life serverless


### (3) Local NSA
1. Los __logs__ se encuentran conectados a través del servicio `awslogs`. La configuración de los logs se encuentra en el archivo `/var/awslogs/etc/awslogs.conf`. Actualmente se muestran los de sistema, deploy y de acceso a la aplicación en CloudWatch. En la siguiente imágen se muestran los logs de acceso a la aplicación.
![alt text](images/access-logs.png "Access Logs")
Se realizó la configuración siguiendo este [tutorial](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/QuickStartEC2Instance.html)

2. Para instalar __NewRelic__ se generó el archivo `newrelic.ini` en el servidor (ver archivo en __branch__ `server`) que permite hacer la conexión con el __dashboard__. Para asociar la aplicación al archivo de agregó en el archivo `/etc/supervisor/conf.d/` lo siguiente:
```python
command=/home/ubuntu/.local/bin/newrelic-admin run-program /home/ubuntu/iic2173-chat-app/venv/bin/gunicorn -k eventlet -w 1 main:app 
environment=PATH="/home/ubuntu/iic2173-chat-app/venv/bin/",NEW_RELIC_CONFIG_FILE="/home/ubuntu/iic2173-chat-app/newrelic.ini"
```
Así siempre al iniciar el servidor se va a montar la aplicación y su estado estará conectado con __New Relic__.
![alt text](images/newrelic-dashboard.png "New Relic")


### (5) Beyond Travis

1. Archivos `buildspec.yml` y `appspec.yml` en repositorio
2. Build y deploys exitosos
![alt text](images/build-deploy-success.png "Build and Deploy Success")
3. Pipeline contra push a master del repositorio
![alt text](images/pipeline.png "CodePipeline")
4. Deploy logs a CloudWatch
![alt text](images/deploy-logs-1.png "CloudWatch Console")
![alt text](images/deploy-logs-2.png "Deploy Logs")

### (6) Load Balancer

1. Esta es la configuración de cómo se ven las instancias corriendo en nuestro EC2. Respecto a lo solicitado en este punto se puede apreciar que hay 2 instancias autogeneradas por ASG (Auto-Scaling-Group), las cuales se pueden acceder desde los link en los detalles.
![alt text](images/6.1.png "Build and Deploy Success")
2. En este paso se puede ver como efectivamente se llevó a cabo la configuración del Load Balancer, el cual mantiene las 2 instancias corriendo, proveyendo de los servicios a los clientes.![alt text](images/6.2.png "Build and Deploy Success")
3. Aquí se ve la configuración del Auto Scaling Group, el cual mantiene un óptimo y mínimo de 2 instancias corriendo y 5 máximo. Así, al usar más de un 50% de su capacidad agrega una instancia y si tiene menos del 10% remueve una.![alt text](images/6.3.png "Build and Deploy Success")
4. Aquí se muestran las configuraciones de lanzamiento de las instancias a través del ASG, con la configuración de la AMI dada por una instancia que queremos “replicar”.
![alt text](images/6.4.png "Build and Deploy Success")
5. Finalmente, podemos ver la configuración del CDN en Cloudfront, que permite ingresar a la información mediante el link dado en los detalles. 
Además de tener un link de “logs”, como se señala en la última línea.
![alt text](images/6.5.png "Build and Deploy Success")

Detalles: 
Link de Load Balancer: http://lb-2-2032493292.us-west-1.elb.amazonaws.com/

Link de CDN: http://d19tniwbjvzank.cloudfront.net/

Supuesto LogBucket Link [XML]: http://elasticbeanstalk-us-west-1-478789511478.s3.amazonaws.com/