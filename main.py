"""Punto de entrada e interfaz de consola para el Sistema de Gestión de Flota y Reservas.

Provee un menú interactivo en terminal con salida coloreada mediante `colorama`
y registro de actividad en archivo mediante `logging`.
"""

import logging

from colorama import Fore, Style, init

from app.gestor import GestorSistema

# Inicialización de Colorama (restablece el color tras cada print)
init(autoreset=True)

# Inicialización del logger
logging.basicConfig(
    filename="gestor.log",
    encoding="utf-8",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def mostrar_menu() -> None:
    """Imprime en pantalla las opciones disponibles del menú principal."""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}" + "=" * 48)
    print(f"{Fore.YELLOW}{Style.BRIGHT}   SISTEMA DE GESTIÓN DE FLOTA Y RESERVAS")
    print(f"{Fore.YELLOW}{Style.BRIGHT}" + "=" * 48)
    print(f"{Fore.YELLOW}1.{Fore.WHITE} Ver flota completa (Coches y Motos)")
    print(f"{Fore.YELLOW}2.{Fore.WHITE} Añadir nuevo vehículo a la flota")
    print(f"{Fore.YELLOW}3.{Fore.WHITE} Realizar una reserva")
    print(f"{Fore.YELLOW}4.{Fore.WHITE} Consultar historial de reservas")
    print(f"{Fore.YELLOW}5.{Fore.WHITE} Salir")
    print(f"{Fore.YELLOW}" + "-" * 48)


def opcion_ver_flota(gestor: GestorSistema) -> None:
    """Muestra todos los vehículos registrados diferenciados por categoría y color.

    Args:
        gestor: Instancia activa de `GestorSistema`.
    """
    flota = gestor.vehiculos
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- FLOTA DE VEHÍCULOS ---")

    if not flota:
        print(f"{Fore.YELLOW}No hay vehículos registrados en la flota actualmente.")
        return

    coches = [v for v in flota if v.tipo == "Coche"]
    motos = [v for v in flota if v.tipo == "Moto"]

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Coches ({len(coches)}):")
    if coches:
        for coche in coches:
            print(
                f"{Fore.CYAN}  - Matrícula: {Style.BRIGHT}{coche.matricula}"
                f"{Style.NORMAL}{Fore.CYAN} | Modelo: {coche.modelo}"
            )
    else:
        print(f"{Fore.CYAN}  (Sin coches registrados)")

    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Motos ({len(motos)}):")
    if motos:
        for moto in motos:
            print(
                f"{Fore.MAGENTA}  - Matrícula: {Style.BRIGHT}{moto.matricula}"
                f"{Style.NORMAL}{Fore.MAGENTA} | Modelo: {moto.modelo}"
            )
    else:
        print(f"{Fore.MAGENTA}  (Sin motos registradas)")


def opcion_añadir_vehiculo(gestor: GestorSistema) -> None:
    """Solicita los datos por consola y registra un nuevo vehículo en el sistema.

    Args:
        gestor: Instancia activa de `GestorSistema`.
    """
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- AÑADIR NUEVO VEHÍCULO ---")
    tipo = input(f"{Fore.WHITE}Tipo de vehículo (Coche / Moto): ")
    matricula = input(f"{Fore.WHITE}Matrícula (ej: 1234ABC): ")
    modelo = input(f"{Fore.WHITE}Modelo (ej: Seat Leon): ")

    try:
        vehiculo = gestor.añadir_vehiculo(tipo, matricula, modelo)
        color_vehiculo = Fore.CYAN if vehiculo.tipo == "Coche" else Fore.MAGENTA
        print(
            f"\n{Fore.GREEN}{Style.BRIGHT}[OK] Vehículo registrado correctamente: "
            f"{color_vehiculo}{vehiculo}"
        )
        logging.info(
            f"Vehículo añadido -> Tipo: {vehiculo.tipo} | "
            f"Matrícula: {vehiculo.matricula} | Modelo: {vehiculo.modelo}"
        )
    except ValueError as error:
        print(f"\n{Fore.RED}{Style.BRIGHT}[ERROR] No se pudo añadir el vehículo: {error}")
        logging.warning(
            f"Fallo al añadir vehículo (tipo='{tipo.strip()}', "
            f"matrícula='{matricula.strip()}'): {error}"
        )


def opcion_reservar_vehiculo(gestor: GestorSistema) -> None:
    """Solicita matrícula y fecha para registrar una nueva reserva diaria.

    Args:
        gestor: Instancia activa de `GestorSistema`.
    """
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- REALIZAR RESERVA ---")
    matricula = input(f"{Fore.WHITE}Matrícula del vehículo a reservar: ")
    fecha = input(f"{Fore.WHITE}Fecha de reserva (AAAA-MM-DD): ")

    try:
        reserva = gestor.reservar_vehiculo(matricula, fecha)
        print(
            f"\n{Fore.GREEN}{Style.BRIGHT}[OK] Reserva confirmada: "
            f"{Fore.LIGHTBLUE_EX}Vehículo '{reserva['matricula']}' "
            f"para la fecha {reserva['fecha']}."
        )
        logging.info(
            f"Reserva confirmada -> Matrícula: {reserva['matricula']} | "
            f"Fecha: {reserva['fecha']}"
        )
    except ValueError as error:
        print(f"\n{Fore.RED}{Style.BRIGHT}[ERROR] No se pudo completar la reserva: {error}")
        logging.warning(
            f"Fallo al reservar (matrícula='{matricula.strip()}', "
            f"fecha='{fecha.strip()}'): {error}"
        )


def opcion_ver_reservas(gestor: GestorSistema) -> None:
    """Lista el historial completo de reservas almacenadas en el sistema.

    Args:
        gestor: Instancia activa de `GestorSistema`.
    """
    reservas = gestor.reservas
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- HISTORIAL DE RESERVAS ---")

    if not reservas:
        print(f"{Fore.LIGHTBLUE_EX}No hay reservas registradas todavía.")
        return

    for indice, reserva in enumerate(reservas, start=1):
        vehiculo = gestor.buscar_vehiculo(reserva["matricula"])
        if vehiculo is not None:
            color_tipo = Fore.CYAN if vehiculo.tipo == "Coche" else Fore.MAGENTA
            detalle_vehiculo = f"{color_tipo}{vehiculo.tipo} - {vehiculo.modelo}"
        else:
            detalle_vehiculo = f"{Fore.RED}Vehículo no disponible en flota actual"

        print(
            f"{Fore.LIGHTBLUE_EX}{indice}. Fecha: {Style.BRIGHT}{reserva['fecha']}"
            f"{Style.NORMAL}{Fore.LIGHTBLUE_EX} | Matrícula: {reserva['matricula']} "
            f"{Fore.WHITE}({detalle_vehiculo}{Fore.WHITE})"
        )


def ejecutar_aplicacion() -> None:
    """Inicializa el gestor del sistema y ejecuta el bucle principal de la CLI."""
    try:
        gestor = GestorSistema()
        logging.info(
            f"Sistema iniciado. Cargados {len(gestor.vehiculos)} vehículos "
            f"y {len(gestor.reservas)} reservas."
        )
    except ValueError as error:
        print(
            f"{Fore.RED}{Style.BRIGHT}[ERROR CRÍTICO] "
            f"Fallo al cargar los archivos de datos: {error}"
        )
        logging.critical(f"Error crítico al inicializar el sistema: {error}")
        return

    while True:
        mostrar_menu()
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-5): {Fore.WHITE}").strip()

        if opcion == "1":
            opcion_ver_flota(gestor)
        elif opcion == "2":
            opcion_añadir_vehiculo(gestor)
        elif opcion == "3":
            opcion_reservar_vehiculo(gestor)
        elif opcion == "4":
            opcion_ver_reservas(gestor)
        elif opcion == "5":
            print(f"\n{Fore.GREEN}Cerrando el sistema. ¡Hasta pronto!")
            logging.info("Sistema cerrado correctamente por el usuario.")
            break
        else:
            print(
                f"\n{Fore.YELLOW}[AVISO] Opción no válida. "
                "Introduce un número del 1 al 5."
            )


if __name__ == "__main__":
    try:
        ejecutar_aplicacion()
    except KeyboardInterrupt:
        print(
            f"\n\n{Fore.YELLOW}Ejecución interrumpida por el usuario. "
            "Cerrando el sistema."
        )
        logging.info("Ejecución interrumpida manualmente (KeyboardInterrupt).")