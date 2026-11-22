"""Módulo de lógica de negocio para la gestión de flota y reservas.

Contiene la clase `GestorSistema`, encargada de coordinar el estado en memoria,
aplicar las reglas de validación de negocio y sincronizar los cambios con la
capa de persistencia.
"""

from datetime import datetime

from app.persistencia import (
    cargar_reservas,
    cargar_vehiculos,
    guardar_reservas,
    guardar_vehiculos,
)
from app.vehiculos import Coche, Moto, Vehiculo


class GestorSistema:
    """Controlador central del sistema de alquiler de vehículos.

    Administra la colección de vehículos de la flota y el registro histórico
    de reservas, garantizando la integridad de los datos y su persistencia.
    """

    def __init__(
        self,
        ruta_vehiculos: str = "vehiculos.txt",
        ruta_reservas: str = "reservas.txt",
    ) -> None:
        """Inicializa el gestor y carga el estado previo desde los archivos.

        Args:
            ruta_vehiculos: Ruta al archivo plano de vehículos.
            ruta_reservas: Ruta al archivo plano de reservas.
        """
        self.__ruta_vehiculos: str = ruta_vehiculos
        self.__ruta_reservas: str = ruta_reservas
        self.__vehiculos: list[Vehiculo] = cargar_vehiculos(self.__ruta_vehiculos)
        self.__reservas: list[dict[str, str]] = cargar_reservas(self.__ruta_reservas)

    @property
    def vehiculos(self) -> list[Vehiculo]:
        """Devuelve una copia de la lista actual de vehículos en la flota."""
        return self.__vehiculos.copy()

    @property
    def reservas(self) -> list[dict[str, str]]:
        """Devuelve una copia del historial de reservas registradas."""
        return [reserva.copy() for reserva in self.__reservas]

    def buscar_vehiculo(self, matricula: str) -> Vehiculo | None:
        """Busca un vehículo en la flota por su matrícula.

        Args:
            matricula: Matrícula del vehículo a localizar.

        Returns:
            Vehiculo | None: La instancia encontrada o `None` si no existe.
        """
        matricula_objetivo = matricula.strip().upper()
        for vehiculo in self.__vehiculos:
            if vehiculo.matricula == matricula_objetivo:
                return vehiculo
        return None

    def esta_disponible(self, matricula: str, fecha: str) -> bool:
        """Comprueba si una matrícula está libre en una fecha determinada.

        Args:
            matricula: Matrícula del vehículo.
            fecha: Fecha en formato 'AAAA-MM-DD'.

        Returns:
            bool: `True` si no existe reserva para esa matrícula y fecha;
            `False` en caso contrario.
        """
        matricula_objetivo = matricula.strip().upper()
        fecha_objetivo = fecha.strip()

        for reserva in self.__reservas:
            if (
                reserva["matricula"] == matricula_objetivo
                and reserva["fecha"] == fecha_objetivo
            ):
                return False
        return True

    def añadir_vehiculo(self, tipo: str, matricula: str, modelo: str) -> Vehiculo:
        """Crea un nuevo vehículo, lo añade a la flota y persiste el cambio.

        Args:
            tipo: Tipo de vehículo ('Coche' o 'Moto', insensible a mayúsculas).
            matricula: Código de matrícula único del vehículo.
            modelo: Marca y modelo del vehículo.

        Returns:
            Vehiculo: La instancia de `Coche` o `Moto` creada y registrada.

        Raises:
            ValueError: Si el tipo no es válido, los datos están vacíos o la
                matrícula ya está registrada en la flota.
        """
        tipo_normalizado = tipo.strip().capitalize()
        matricula_normalizada = matricula.strip().upper()

        if self.buscar_vehiculo(matricula_normalizada) is not None:
            raise ValueError(
                f"Ya existe un vehículo registrado con la matrícula '{matricula_normalizada}'."
            )

        nuevo_vehiculo: Vehiculo
        if tipo_normalizado == "Coche":
            nuevo_vehiculo = Coche(matricula_normalizada, modelo)
        elif tipo_normalizado == "Moto":
            nuevo_vehiculo = Moto(matricula_normalizada, modelo)
        else:
            raise ValueError(
                f"Tipo de vehículo inválido '{tipo}'. Debe ser 'Coche' o 'Moto'."
            )

        self.__vehiculos.append(nuevo_vehiculo)
        guardar_vehiculos(self.__ruta_vehiculos, self.__vehiculos)
        return nuevo_vehiculo

    def reservar_vehiculo(self, matricula: str, fecha: str) -> dict[str, str]:
        """Registra una reserva validando existencia y disponibilidad diaria.

        Args:
            matricula: Matrícula de un vehículo existente en la flota.
            fecha: Fecha de reserva en formato estricto 'AAAA-MM-DD'.

        Returns:
            dict[str, str]: Diccionario con la reserva confirmada.

        Raises:
            ValueError: Si el formato de fecha es inválido, la matrícula no
                existe en la flota o el vehículo ya está ocupado ese día.
        """
        matricula_normalizada = matricula.strip().upper()
        fecha_normalizada = self.__validar_formato_fecha(fecha)

        if self.buscar_vehiculo(matricula_normalizada) is None:
            raise ValueError(
                f"No existe ningún vehículo con la matrícula '{matricula_normalizada}'."
            )

        if not self.esta_disponible(matricula_normalizada, fecha_normalizada):
            raise ValueError(
                f"El vehículo '{matricula_normalizada}' ya está reservado para el {fecha_normalizada}."
            )

        nueva_reserva = {
            "matricula": matricula_normalizada,
            "fecha": fecha_normalizada,
        }
        self.__reservas.append(nueva_reserva)
        guardar_reservas(self.__ruta_reservas, self.__reservas)
        return nueva_reserva

    @staticmethod
    def __validar_formato_fecha(fecha: str) -> str:
        """Valida que la cadena cumpla el formato de fecha 'AAAA-MM-DD'.

        Args:
            fecha: Cadena de fecha introducida.

        Returns:
            str: Fecha limpia validada en formato 'AAAA-MM-DD'.

        Raises:
            ValueError: Si la cadena no respeta el formato o es una fecha irreal.
        """
        fecha_limpia = fecha.strip()
        try:
            datetime.strptime(fecha_limpia, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError(
                f"Formato de fecha inválido '{fecha}'. Usa el formato AAAA-MM-DD (ej: 2026-12-01)."
            ) from error
        return fecha_limpia