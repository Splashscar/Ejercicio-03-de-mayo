from repositories.account_repository import AccountRepository
import threading

transaction_lock = threading.Lock()


class TransactionService:

    @staticmethod
    def transfer(origin, destiny, amount):

        db = AccountRepository.load_accounts()

        if origin not in db or destiny not in db:
            return {"error": "Cuentas no encontradas"}, 404

        # Validación de tipo
        if not isinstance(amount, (int, float)):
            return {"error": "Monto invalido"}, 422

        # Validación de monto positivo
        if amount <= 0:
            return {"error": "El monto debe ser mayor a cero"}, 422

        # Validación de cuenta origen
        if db[origin]["estado"] != "ACTIVA":
            return {"error": "Cuenta de origen no disponible"}, 403

        # Validación de cuenta destino
        if db[destiny]["estado"] != "ACTIVA":
            return {"error": "Cuenta destino no disponible"}, 403

        if db[origin]["saldo"] < amount:
            return {"error": "Fondos insuficientes"}, 400

        with transaction_lock:

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