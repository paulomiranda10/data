	docker rm -f rank; \
	docker run \
		--name rank \
		-d -it \
		-v /home/spark/rankhotsite/:/home/rank/ \
		rank; \

# linha que vai no main.sh para rodar localmente Dev
#		-v /home/paulo/Centauro/discovery/rankhotsite/:/home/rank/ \

# linha que vai no main.sh para rodar no servidor de DS
#		-v /home/spark/rankhotsite/:/home/rank/ \
		