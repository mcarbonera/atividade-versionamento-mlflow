.PHONY : build, end, clear_all

build:
	@echo "Build the services..."
	@docker-compose up --build -d

end:
	@echo "Finish the services..."
	@docker-compose kill

clear_all:
	@echo "Removing all Docker containers..."
	@docker rm -f $$(docker ps -a -q) || true