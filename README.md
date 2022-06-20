
# BioHub

## Qué es?

BioHub es una librería escrita en Python para el manejo de datos bioinformáticos. Actualmente se encuentra centrada en análisis de bacterias. BioHub está diseñada para tener un funcionamiento similar a una API, pero no conectada con un servicio en la nube o un servicio online. Los procesos facilitados por parte de BioHub son:

* **Gestión de ficheros asociados a un individuo.** El sistema es capaz de reconocer que ficheros están asociados con el sujeto, facilitando el control de los ficheros de entrada y salida de cualquier proceso realizado. Esto mantiene un registro del papel que desempeña el fichero en el análisis, además de mantener un control exhaustivo del mismo.
* **Ejecución de procesos bioinformáticos.** Proporciona un método automatizado y sencillo de ejecutar ciertas tareas bioinformáticas escribiendo el código en Python.
* **Control de individuos.** Los dos puntos anteriores unidos, proporciona un control estricto del resultado de los sujetos y sí el proceso se ha realizado con éxito. Esto permite relanzar procesos fallidos de forma sencilla sin tener que escribir excepeciones de que individuos si pueden entrar en el proceso y cuales no.