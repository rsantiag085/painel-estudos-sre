"""Carrega configurações locais sem sobrescrever variáveis do ambiente."""

from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"), override=False)
