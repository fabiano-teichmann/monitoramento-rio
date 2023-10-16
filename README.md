# Monitoramento Rio Itajaí-Içu
Esse projeto é a curiosidade para entender a evolução do rio Itajaí Içu,
pegando dados do Alerta Blu eu armazendo o histórico do nível do rio

## Deploy
Primeiramente é necessário  dar o build na imagem docker

    docker build -t alertablu:last .

Usando kubernetes entre no dir infra e rode os seguintes comandos

Criando o volume para persistir os dados

    kubectl apply -f db-persistent-volume.yaml


Criando o PVC

    kubectl apply -f db-volume-claim.yaml

Passando as variáveis de ambiente, que são a conexão com o banco de dados
e url do Alerta Blu

    kubectl apply -f configmap.yaml

Criando o deploy

    kubectl apply -f deployment.yaml

Expondo o serviço
    
    kubectl apply -f service.yaml
    
Verificando 

     kubectl get all    