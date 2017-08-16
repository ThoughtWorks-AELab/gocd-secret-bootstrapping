.PHONY: all run clean
all: run

run:
	./bin/start.sh

clean:
	-kubectl delete deployment gocd-server	
	-kubectl delete service gocd-server	
	-kubectl delete deployment gocd-agent
	-kubectl delete deployment vault
	-kubectl delete service vault
	-kubectl delete secret go-secrets
	-kubectl delete job vault-setup