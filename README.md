# teste_texoit
## API RESTful para possibilitar a leitura da lista de indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.

___
### Rquirements
- [python 3.8+](https://www.python.org/downloads/)

### Instalação Linux, OSX
___
clone o repositorio:
```
$ git clone https://github.com/Semicheche/teste_texoit.git
```
Crie um ambiente virtual para o projeto
```
python -m venv textoit_env
```
Ative o ambiente
```
$ source textoit_env/bin/activate
```
o ambiente ativo ficara dessa forma no terminal
```
(texoit_env) ➜  workspace$
```
instale as dependencias no arquino `requirements.txt`

```
$ pip install -r requirements.txt
```

acesse o projeto
```
$ cd gra_app
```

e agora rode a aplicação
```
$ uvicorn main:app --reload
```

Agora acesse via Browser o endereço `localhost:8000`

|HTTP | URL|
|-----|----|
|GET| `/best-producers`|