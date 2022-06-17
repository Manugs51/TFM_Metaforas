# TFM_Metaforas
 
Funcionando en python 3.8.6

Es necesario tener un archivo secrets.py conteniendo:

```python
secrets = {
    'babel_net_key': <clave_propia_para_babel_net>
}
```

Dependencias:
- requests==2.25.1
- flask==1.1.2
- spacy==3.3.1
- python -m spacy download es_core_news_lg