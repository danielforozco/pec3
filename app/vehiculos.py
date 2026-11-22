"""Módulo de dominio para el modelado de vehículos de la flota.

Define la clase base abstracta conceptual `Vehiculo` y sus especializaciones
`Coche` y `Moto`, aplicando encapsulamiento mediante atributos privados y
propiedades de solo lectura.
"""


class Vehiculo:
    """Clase base que representa un vehículo genérico dentro de la flota.

    Attributes:
        matricula (str): Identificador único del vehículo (solo lectura).
        modelo (str): Marca y modelo comercial del vehículo (solo lectura).
        tipo (str): Categoría del vehículo (solo lectura).
    """

    def __init__(self, matricula: str, modelo: str) -> None:
        """Inicializa una instancia de Vehiculo validando sus datos básicos.

        Args:
            matricula: Código de matrícula del vehículo.
            modelo: Nombre o descripción del modelo del vehículo.

        Raises:
            ValueError: Si la matrícula o el modelo están vacíos.
        """
        matricula_limpia = matricula.strip().upper()
        modelo_limpio = modelo.strip()

        if not matricula_limpia:
            raise ValueError("La matrícula del vehículo no puede estar vacía.")
        if not modelo_limpio:
            raise ValueError("El modelo del vehículo no puede estar vacío.")

        self.__matricula: str = matricula_limpia
        self.__modelo: str = modelo_limpio

    @property
    def matricula(self) -> str:
        """Devuelve la matrícula normalizada del vehículo."""
        return self.__matricula

    @property
    def modelo(self) -> str:
        """Devuelve el modelo del vehículo."""
        return self.__modelo

    @property
    def tipo(self) -> str:
        """Devuelve el tipo de vehículo según el nombre de su clase."""
        return self.__class__.__name__

    def to_linea(self) -> str:
        """Serializa el vehículo a una línea de texto separada por comas.

        Returns:
            str: Cadena con formato 'Tipo,Matricula,Modelo'.
        """
        return f"{self.tipo},{self.matricula},{self.modelo}"

    def __str__(self) -> str:
        """Devuelve una representación legible del vehículo para el usuario."""
        return f"[{self.tipo}] Matrícula: {self.matricula} | Modelo: {self.modelo}"

    def __repr__(self) -> str:
        """Devuelve una representación técnica del objeto para depuración."""
        return f"{self.tipo}(matricula={self.matricula!r}, modelo={self.modelo!r})"


class Coche(Vehiculo):
    """Subclase que representa un vehículo de tipo Coche."""

    def __init__(self, matricula: str, modelo: str) -> None:
        """Inicializa un Coche delegando la validación a la clase base.

        Args:
            matricula: Código de matrícula del coche.
            modelo: Marca y modelo del coche.
        """
        super().__init__(matricula, modelo)


class Moto(Vehiculo):
    """Subclase que representa un vehículo de tipo Moto."""

    def __init__(self, matricula: str, modelo: str) -> None:
        """Inicializa una Moto delegando la validación a la clase base.

        Args:
            matricula: Código de matrícula de la moto.
            modelo: Marca y modelo de la moto.
        """
        super().__init__(matricula, modelo)