from setuptools import setup, find_packages


install_requires = [
    'asyncpg',
    'pydantic',
    'fastapi',
    'uvicorn',
    'sqlalchemy[asyncio]',
    'gunicorn'
]

setup(
    name='TimeManager',
    version="0.0.3.dev1",
    description='Lyceum API',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'init_models = TimeManager.db.base:run_init_models',
            'init_db = TimeManager.db.create:run_init_db',
        ]
    }
)

