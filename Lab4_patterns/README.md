# Міні-СКБД: мінімальне логування + pytest

Патерни: Singleton, Builder, Factory Method. Логи лише короткі INFO:
- Table ready: <name>
- Query <table>: N rows
- Join <l>.<key>=<r>.<key>: N rows
- TX begin / TX commit / TX rollback

## Запуск
```
pytest -q
python demo.py
```
