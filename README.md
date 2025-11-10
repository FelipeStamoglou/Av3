Cliente (ab / navegador)
        ↓
     [ NGINX ]
  ┌──────────────┬──────────────┬──────────────┐
  │   web1:5000  │   web2:5000  │   web3:5000  │
  └──────────────┴──────────────┴──────────────┘

Tecnologias utilizadas:

. Docker e Docker Compose
. Nginx (proxy reverso / balanceador)
. Flask (backends)
. Apache Benchmark (ab) (testes de carga)
. Python (Pandas + Matplotlib) (análise e geração de gráficos)

Subir o ambiente
Crie e suba os containers:

docker-compose up -d --build

Acesse no navegador:
http://localhost:8080/
Cada atualização retornará o nome de um dos servidores (web1, web2, web3).

Rotina de Testes e Coleta de Logs
. Essa sequência executa os três modos de balanceamento, coleta os logs e analisa os resultados.

Etapa 1 — Round Robin

docker logs proxy --since 1h --details > /dev/null
ab -n 1000 -c 50 http://localhost:8080/
docker logs proxy > logs_roundrobin.txt

Etapa 2 — Least Connections
. Altere o nginx.conf:

upstream web_upstream {
    least_conn;
    server web1:5000;
    server web2:5000;
    server web3:5000;
}

Recarregue o Nginx e repita o teste:

docker exec -it proxy nginx -s reload
ab -n 1000 -c 50 http://localhost:8080/
docker logs proxy > logs_leastconn.txt

Etapa 3 — IP Hash
.Altere o nginx.conf novamente:

upstream web_upstream {
    ip_hash;
    server web1:5000;
    server web2:5000;
    server web3:5000;
}

Recarregue novamente o nginx e repita o teste:

docker exec -it proxy nginx -s reload
ab -n 1000 -c 50 http://localhost:8080/
docker logs proxy > logs_iphash.txt

Análise dos Resultados
. Após gerar os logs, ative seu ambiente virtual e execute o script de análise:

source venv/bin/activate
python3 analisar_logs.py

O script:
. Lê os logs (logs_roundrobin.txt, logs_leastconn.txt, logs_iphash.txt);
. Extrai upstream_addr (servidor que atendeu) e request_time;
. Gera gráficos com:
. Tempo médio por servidor
. Distribuição de requisições por servidor

Os gráficos são salvos na pasta Gráficos, dentro do escopo do projeto.

Interpretação dos Resultados
Algoritmo	                Comportamento esperado
Round Robin	              Distribui requisições igualmente entre os três servidores.
Least Connections	        Prioriza servidores com menos conexões ativas, otimizando desempenho sob carga desigual.
IP Hash	                  Garante que o mesmo cliente seja atendido sempre pelo mesmo servidor (útil para sessões persistentes).

Simulação de Falhas

Para testar tolerância a falhas:

docker stop web2
ab -n 500 -c 30 http://localhost:8080/

Mesmo para web1 e web3, apenas atentar-se para estar algum em funcionamento.

Conclusão 
O experimento permitiu observar:

. A eficiência do balanceamento de carga no Nginx;
. A diferença de comportamento entre os algoritmos;
. A resiliência do sistema quando um backend fica indisponível.
. Os resultados obtidos confirmam a importância do uso de balanceadores de carga para garantir desempenho, disponibilidade e escalabilidade em sistemas distribuídos.


Ação	                                    Comando
Ver status dos containers	                docker ps
Parar todos os serviços	                  docker-compose down
Recarregar configuração Nginx	            docker exec -it proxy nginx -s reload
Ver logs ao vivo	                        docker logs -f proxy
Copiar logs para o host	                  docker logs proxy > logs.txt



