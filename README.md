# Anansi

Limite-limite version HE-Arc. 

Projet réalisé dans le cadre du cours de développement web de troisième année à l'HE-Arc.

Plus d'informations quant au développement sont disponibles dans le [wiki](https://github.com/HE-Arc/anansi/wiki).

## Basic setup for dev

### API Django

Install dependencies using pip environment :

```sh
cd api/
pipenv shell
pipenv install -r requirements.txt
```

Configuration : use and adapt the `.env.example` file :

```sh
cp .env.example .env
```

Redis database setup using Docker :

```sh
docker run -p 6379:6379 -d redis:5
```

Apply database migrations :

```sh
python manage.py migrate
```

Run dev server :

```sh
python manage.py runserver
```

### Frontend

Install dependencies :

```sh
cd frontend/
npm install
```

Configuration : use and adapt the `.env.example` file :

```sh
cp .env.example .env
```

Run dev server :

```sh
quasar run dev
```

Build the project for prod :

```sh
quasar build
```
