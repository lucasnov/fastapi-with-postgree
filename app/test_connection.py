# #!/usr/bin/env python3
# import os
# import socket
# import time
# import sys
# from urllib.parse import urlparse

# def test_dns_resolution(hostname):
#     """Testa resolução DNS"""
#     try:
#         ip = socket.gethostbyname(hostname)
#         print(f"✅ DNS OK: {hostname} -> {ip}")
#         return True
#     except socket.gaierror as e:
#         print(f"❌ Erro DNS: {hostname} - {e}")
#         return False

# def test_port_connection(hostname, port):
#     """Testa conexão TCP na porta"""
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(10)
#         result = sock.connect_ex((hostname, port))
#         sock.close()
        
#         if result == 0:
#             print(f"✅ Porta OK: {hostname}:{port}")
#             return True
#         else:
#             print(f"❌ Porta fechada: {hostname}:{port}")
#             return False
#     except Exception as e:
#         print(f"❌ Erro conexão: {hostname}:{port} - {e}")
#         return False

# def test_database_connection():
#     """Testa conexão com banco usando SQLAlchemy"""
#     try:
#         from sqlalchemy import create_engine, text
        
#         database_url = os.getenv(
#             "DATABASE_URL",
#             f"postgresql+psycopg://{os.getenv('POSTGRES_USER', 'projeto')}:"
#             f"{os.getenv('POSTGRES_PASSWORD', 'projeto')}@db:5432/"
#             f"{os.getenv('POSTGRES_DB', 'projeto')}"
#         )
        
#         if not database_url:
#             print("❌ DATABASE_URL não encontrada!")
#             return False
            
#         print(f"🔗 Testando: {database_url}")
        
#         engine = create_engine(database_url)
#         with engine.connect() as conn:
#             result = conn.execute(text("SELECT version()"))
#             version = result.fetchone()[0]
#             print(f"✅ Banco OK: {version}")
#             return True
            
#     except Exception as e:
#         print(f"❌ Erro SQLAlchemy: {e}")
#         return False

# def main():
#     print("🔍 DIAGNÓSTICO DE CONECTIVIDADE")
#     print("=" * 50)
    
#     # 1. Verificar variáveis de ambiente
#     print("\n📋 VARIÁVEIS DE AMBIENTE:")
#     env_vars = ['DATABASE_URL', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']
#     for var in env_vars:
#         value = os.getenv(var, 'NÃO DEFINIDA')
#         if 'PASSWORD' in var and value != 'NÃO DEFINIDA':
#             value = '*' * len(value)
#         print(f"   {var}: {value}")
    
#     # 2. Parse da DATABASE_URL
#     database_url = os.getenv('DATABASE_URL')
#     if database_url:
#         parsed = urlparse(database_url)
#         hostname = parsed.hostname
#         port = parsed.port or 5432
#         print(f"\n🎯 TARGET: {hostname}:{port}")
#     else:
#         hostname = os.getenv('DB_HOST', 'db')
#         port = int(os.getenv('DB_PORT', '5432'))
#         print(f"\n🎯 TARGET: {hostname}:{port}")
    
#     # 3. Testes de rede
#     print(f"\n🌐 TESTES DE REDE:")
#     dns_ok = test_dns_resolution(hostname)
#     port_ok = test_port_connection(hostname, port) if dns_ok else False
    
#     # 4. Teste de banco
#     print(f"\n🗄️ TESTE DE BANCO:")
#     if dns_ok and port_ok:
#         db_ok = test_database_connection()
#     else:
#         print("❌ Pulando teste de banco (rede com problema)")
#         db_ok = False
    
#     # 5. Resumo
#     print(f"\n📊 RESUMO:")
#     print(f"   DNS: {'✅' if dns_ok else '❌'}")
#     print(f"   Porta: {'✅' if port_ok else '❌'}")
#     print(f"   Banco: {'✅' if db_ok else '❌'}")
    
#     if not dns_ok:
#         print(f"\n💡 DICA: Verifique se o serviço '{hostname}' está rodando")
#         print(f"   Execute: docker-compose ps")
    
#     return dns_ok and port_ok and db_ok

# if __name__ == "__main__":
#     success = main()
#     sys.exit(0 if success else 1)