"""Módulo de persistencia en archivos planos (.txt).

Provee funciones para serializar y deserializar el estado de la flota
de vehículos y el historial de reservas utilizando archivos de texto.
"""

from app.vehiculos import Coche, Moto, Vehiculo


def cargar_vehiculos(ruta_archivo: str) -> list[Vehiculo]:
    """Lee el archivo de vehículos y reconstruye los objetos en memoria.

    Cada línea válida debe tener el formato 'Tipo,Matricula,Modelo'.
    Las líneas vacías se ignoran automáticamente.

    Args:
        ruta_archivo: Ruta relativa o absoluta al archivo 'vehiculos.txt'.

    Returns:
        list[Vehiculo]: Lista de instancias de `Coche` y `Moto` cargadas.

    Raises:
        ValueError: Si una línea tiene formato corrupto o un tipo desconocido.
    """
    vehiculos: list[Vehiculo] = []

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue

                partes = linea_limpia.split(",", maxsplit=2)
                if len(partes) != 3:
                    raise ValueError(
                        f"Formato inválido en {ruta_archivo} (línea {numero_linea}): '{linea_limpia}'"
                    )

                tipo, matricula, modelo = partes

                if tipo == "Coche":
                    vehiculos.append(Coche(matricula, modelo))
                elif tipo == "Moto":
                    vehiculos.append(Moto(matricula, modelo))
                else:
                    raise ValueError(
                        f"Tipo de vehículo desconocido '{tipo}' en {ruta_archivo} (línea {numero_linea})."
                    )
    except FileNotFoundError:
        return []

    return vehiculos


def guardar_vehiculos(ruta_archivo: str, vehiculos: list[Vehiculo]) -> None:
    """Sobrescribe el archivo de vehículos con el estado actual de la flota.

    Args:
        ruta_archivo: Ruta relativa o absoluta al archivo 'vehiculos.txt'.
        vehiculos: Lista de objetos `Vehiculo` a persistir.
    """
    with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
        for vehiculo in vehiculos:
            archivo.write(f"{vehiculo.to_linea()}\n")


def cargar_reservas(ruta_archivo: str) -> list[dict[str, str]]:
    """Lee el archivo de reservas y devuelve una lista de registros en memoria.

    Cada línea válida debe tener el formato 'Matricula,AAAA-MM-DD'.

    Args:
        ruta_archivo: Ruta relativa o absoluta al archivo 'reservas.txt'.

    Returns:
        list[dict[str, str]]: Lista de diccionarios con claves 'matricula' y 'fecha'.

    Raises:
        ValueError: Si alguna línea no cumple con el formato esperado.
    """
    reservas: list[dict[str, str]] = []

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue

                partes = linea_limpia.split(",", maxsplit=1)
                if len(partes) != 2:
                    raise ValueError(
                        f"Formato inválido en {ruta_archivo} (línea {numero_linea}): '{linea_limpia}'"
                    )

                matricula, fecha = partes
                reservas.append({
                    "matricula": matricula.strip().upper(),
                    "fecha": fecha.strip(),
                })
    except FileNotFoundError:
        return []

    return reservas


def guardar_reservas(ruta_archivo: str, reservas: list[dict[str, str]]) -> None:
    """Sobrescribe el archivo de reservas con el historial actualizado.

    Args:
        ruta_archivo: Ruta relativa o absoluta al archivo 'reservas.txt'.
        reservas: Lista de diccionarios con las reservas registradas.
    """
    with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
        for reserva in reservas:
            archivo.write(f"{reserva['matricula']},{reserva['fecha']}\n")