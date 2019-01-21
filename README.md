# partyou-desafio
Desafio Partyou - Python Backend

Aplicação disponível em https://partyoudesafio.herokuapp.com/


[![codecov](https://codecov.io/gh/alisonamerico/partyou-desafio/branch/master/graph/badge.svg)](https://codecov.io/gh/alisonamerico/partyou-desafio)
[![Build Status](https://travis-ci.org/alisonamerico/partyou-desafio.svg?branch=master)](https://travis-ci.org/alisonamerico/partyou-desafio)
[![Updates](https://pyup.io/repos/github/alisonamerico/partyou-desafio/shield.svg)](https://pyup.io/repos/github/alisonamerico/partyou-desafio/)
[![Python 3](https://pyup.io/repos/github/alisonamerico/partyou-desafio/python-3-shield.svg)](https://pyup.io/repos/github/alisonamerico/partyou-desafio/)

Processos utilizados no desevolvimento do projeto:

Entrega Contínua:

 - Integração com Pipenv Travis e Pyup
 
 - Deploy Automático
 
 - Pytest: Para configurar e construir testes automatizados para o Django.
 
 - Codecov: Para cobertura de testes
 
 - python-decouple: Para desacoplar as configurações de instância da aplicação.

 - CDN da Amazon (S3): Para poder enviar e acessar os arquivos na nuvem.   

 - Agendamento de Backup do Postgresql 
 
 - Sentry: para monitoramento de erros em tempo real.

Como instalar localmente (supondo que você tenha git e python> = 3.7 instalado):
```console
git clone https://github.com/alisonamerico/partyou-desafio.git
cd partyou-desafio
cp contrib/env-sample .env
pipenv install
```
Se você quiser usar o SQLite no seu ambiente de desenvolvimento, remova DATABASE_URL do arquivo .env. Caso contrário, preencha este valor com suas credenciais de banco de dados.

Você pode fazer várias migrações para gerar o esquema do banco de dados:
```console
python manage.py migrate
``` 
Você também pode criar um usuário:
```console
python manage.py createsuperuser
```
Para executar o servidor localmente (com virtualenv ativado):
```console
python manager.py runserver
```
Para executar os testes:
```console
pytest partyou --cov=partyou
```
