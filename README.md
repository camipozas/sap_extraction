# sap_extraction

***Spanish Version***

Bot para extracción de transacción FBL5N en SAP Fiori

Las librerías utilizadas son:
- Selenium
- Datatime
- Environs (para protección de credenciales)
- Os
- Shutil
- Pandas

En primer lugar, se definió la función *descarga()* que ingresa a la transacción de SAP, mediante selenium se realizan todos los clicks correspondientes para poder realizar el flujo completo y extraer los datos.

Cabe destacar que SAP posee frames, es decir páginas dentro de otra página por lo que hay que utilizar switch para ingresar.

Por otro lado, los archivos extraidos individualmente se alojaron en una carpeta temporal en el código en donde una vez consolidados todos los archivos estos se eliminan. El consolidado es un dataframe que convierte a excel.

Cosas a considerar, al cambiar de usuario depende de su rol y perfil dentro de la plataforma dado que su url dependerá de está y a su vez la forma de ingresar a la transacción (frames)

Por último, en teoría están mapeados todos los posibles errores de SAP de tal forma que no tenga que ejecutarse de forma supervisada.

*Nota:* Para poder realizar inspection en una scrollbar, se basó en lo siguiente:
https://twitter.com/sulco/status/1305841873945272321

***English Version***

This is a bot for the extraction in SAP Fiori transaction, exactly FBL5N. 

The libraries used are:
- Selenium
- Datatime
- Environs (for security of credentials)
- Os
- Shutil
- Pandas

Fistable, I defined the function *descarga()* that enters in the transaction in SAP by selenium I did the all scraping to do all the flow and extract the data.

Notably SAP have frames, that is websites inside another websites so we have to used switch to enterokay.

Secondly, the individually downloads files were hosted in a temporary folder in the same code, where once all the files consolidated, they are deleted. This consolidated is a dataframe that converts to excel.

Things to consider, when changing users it depends on their role and profile whithin the platform since their url will depend on this and in turn the way to enter the transaction (frames).

Finally, in theory all possible SAP errors are mapped in such away that they doesn't have to be executed in a supervised way.

*Note:* To be able to perform inspection in a scrollbar, was based on this following: https://twitter.com/sulco/status/1305841873945272321 