from repositories.account_repository import AccountRepository


class TransactionService:

    @staticmethod
    def transfer(origin, destiny, amount):

        db = AccountRepository.load_accounts()

        if origin not in db or destiny not in db:
            return {"error": "Cuentas no encontradas"}, 404

        if db[origin]["estado"] != "ACTIVA":
            return {"error": "Cuenta de origen no disponible"}, 403

        if db[origin]["saldo"] < amount:
            return {"error": "Fondos insuficientes"}, 400

        db[origin]["saldo"] -= amount
        db[destiny]["saldo"] += amount

        db[origin]["historial"].append({
            "tipo": "DEBITO",
            "monto": amount,
            "target": destiny
        })

        db[destiny]["historial"].append({
            "tipo": "CREDITO",
            "monto": amount,
            "target": origin
        })

        AccountRepository.save_accounts(db)

        return {
            "status": "SUCCESS",
            "message": "Transferencia procesada"
        }, 200