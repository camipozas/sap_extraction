## Spanish Version

Bot para extracción de transacción FBL5N en SAP Fiori.

En primer lugar, se definió la función *descarga()* que ingresa a la transacción de SAP, mediante selenium se realizan todos los clicks correspondientes para poder realizar el flujo completo y extraer los datos.

Cabe destacar que SAP posee frames, es decir páginas dentro de otra página por lo que hay que utilizar switch para ingresar.

Por otro lado, los archivos extraídos individualmente se alojaron en una carpeta temporal en el código en donde una vez consolidados todos los archivos estos se eliminan. El consolidado es un dataframe que convierte a excel.

Cosas a considerar, al cambiar de usuario depende de su rol y perfil dentro de la plataforma dado que su url dependerá de está y a su vez la forma de ingresar a la transacción (frames)

Por último, en teoría están mapeados todos los posibles errores de SAP de tal forma que no tenga que ejecutarse de forma supervisada.

> *Nota:* Para poder realizar inspection en una scrollbar, se basó en lo siguiente:
https://twitter.com/sulco/status/1305841873945272321

Para instalar chromedriver, debe buscar su versión de Chrome y luego descargarla aquí [Chrome Driver](https://chromedriver.chromium.org/downloads)

Por otro lado, la transacción descarga archivos que contienen *export.xlsx* los cuales no son tomados en consideración al momento de consolidar por lo que en la función de consolidado estos se eliminan.