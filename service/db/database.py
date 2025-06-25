import aiomysql

class MySQLPool:
    def __init__(self):
        self.pool = None

    async def init(self, host, port, user, password, db, minsize=5, maxsize=20):
        self.pool = await aiomysql.create_pool(
            host=host, port=port, user=user, password=password, db=db,
            minsize=minsize, maxsize=maxsize, autocommit=True
        )

    async def call_procedure(self, proc_name: str, params: tuple = ()): 
        if self.pool is None:
            raise RuntimeError("MySQLPool is not initialized. Call init() first.")
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.callproc(proc_name, params)
                result = await cur.fetchall()
                await cur.close()
                return result

    async def execute(self, query: str, params: tuple = ()): 
        if self.pool is None:
            raise RuntimeError("MySQLPool is not initialized. Call init() first.")
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                if query.strip().lower().startswith("select"):
                    return await cur.fetchall()
                return cur.lastrowid 