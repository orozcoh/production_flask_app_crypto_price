[This repo was made following this guide] (https://ianlondon.github.io/blog/deploy-flask-docker-nginx/)

---------Using python3 for development-------------

1) Create virtual environment 

	virutualenv venv

2) activate venv

	source venv/bin/activate

----------------Using Docker------------------------
 
1) Build container

	docker build -t docker_app .

2) Run container

	docker run -p 80:80 -t docker_app
