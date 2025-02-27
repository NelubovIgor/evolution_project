from contextlib import contextmanager

@contextmanager
def context_manager():
    try:
        yield 'ContextManager'
    except IndexError:
        print('Исключение IndexError обработано')
    
with context_manager() as manager:
    print(manager[100])
