MODULE = bot
PY = python3
FLAGS = -m

#colors for beauty
YELLOW = \033[33;1m
RESET = \033[0m
GREEN = \033[32;1m
MAGENTA = \033[35;1m

app:
	@docker-compose up

app-build:
	@docker-compose build

app-bash-bot:
	@docker-compose run --rm bot bash