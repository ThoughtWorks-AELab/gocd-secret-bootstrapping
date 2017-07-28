.PHONY: all run clean
all: run

run:
	kubectl create -f ./kubernetes/go-cd-server.yml
	kubectl create -f ./kubernetes//go-cd-agent.yml
	minikube service list

clean:
	-kubectl delete deployment gocd-server	
	-kubectl delete service gocd-server	
	-kubectl delete deployment gocd-agent